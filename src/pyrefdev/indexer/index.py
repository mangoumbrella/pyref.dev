import dataclasses
import json
import re
import random
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Literal, overload
from urllib import error, request

from packaging import version
from cyclopts import Parameter

from pyrefdev import __version__
from pyrefdev.config import Package, console


_RTD_URL_PATTERN = re.compile(r"https?://([^\s/]+\.readthedocs\.io)\b")


def urlopen(url: str):
    req = request.Request(
        url,
        method="GET",
        headers={"User-Agent": f"pyrefdev/{__version__} (+https://pyref.dev)"},
    )
    backoffs = [1, 2, 5, 15, 30, 60]
    while True:
        try:
            return request.urlopen(req, timeout=60)
        except error.HTTPError as e:
            if e.code == 429:  # Too Many Request
                if not backoffs:
                    raise
                backoff = backoffs.pop(0) * (0.9 + random.random() / 5.0)
                time.sleep(backoff)
            else:
                raise
        except (TimeoutError, error.URLError) as e:
            if isinstance(e, error.URLError) and not isinstance(
                e.reason, (TimeoutError, OSError)
            ):
                raise
            if not backoffs:
                raise
            backoff = backoffs.pop(0) * (0.9 + random.random() / 5.0)
            time.sleep(backoff)


@dataclasses.dataclass
class IndexState:
    package_version: str
    file_to_urls: dict[str, str]
    # url -> error_code (e.g. "http-404", or "" for unknown)
    failed_urls: dict[str, str]

    @classmethod
    def loads(cls, content: str) -> "IndexState":
        return cls(**json.loads(content))

    def dumps(self) -> str:
        return json.dumps(dataclasses.asdict(self))


def _get_default_api_docs_directory() -> Path:
    cwd = Path(__file__).parent
    git_root = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True
    ).strip()
    git_remote = subprocess.check_output(
        ["git", "remote", "get-url", "origin"], cwd=git_root, text=True
    ).strip()
    if "/pyref.dev" in git_remote:
        return Path(git_root) / "api-docs"
    else:
        directory = Path(tempfile.mkdtemp(prefix="pyref.dev."))
        console.print(f"Using temporary directory for API docs: {directory}")
        return directory


@Parameter(name="*")
@dataclasses.dataclass
class Index:
    docs_directory: Path = dataclasses.field(
        default_factory=_get_default_api_docs_directory
    )

    def _ensure_directory(self) -> None:
        self.docs_directory.mkdir(parents=True, exist_ok=True)
        (self.docs_directory / "__pypi__").mkdir(parents=True, exist_ok=True)

    def load_crawl_state(self, package: str) -> IndexState | None:
        self._ensure_directory()
        crawl_state_file = self.docs_directory / f"{package}.json"
        if not crawl_state_file.exists():
            return None
        return IndexState.loads(crawl_state_file.read_text())

    def save_crawl_state(self, package: str, crawl_state: IndexState) -> None:
        self._ensure_directory()
        crawl_state_file = self.docs_directory / f"{package}.json"
        crawl_state_file.write_text(crawl_state.dumps())

    def fetch_pypi_data(self, package: str, *, refresh: bool) -> bytes:
        pypi_data_file = self.docs_directory / "__pypi__" / f"{package}.json"
        if not refresh and pypi_data_file.exists():
            return pypi_data_file.read_bytes()
        with urlopen(f"https://pypi.org/pypi/{package}/json") as f:
            data = f.read()
        self._ensure_directory()
        pypi_data_file.write_bytes(data)
        return data

    def get_pypi_packages(self) -> list[str]:
        return list(f.stem for f in self.docs_directory.glob("__pypi__/*.json"))

    def fetch_package_version(self, package: Package) -> version.Version | None:
        if package.is_cpython():
            return _fetch_latest_cpython_version()
        try:
            data = self.fetch_pypi_data(package.pypi, refresh=True)
            pypi_info = json.loads(data)
            return version.parse(pypi_info["info"]["version"])
        except error.URLError as e:
            console.warning(
                f"Failed to fetch pypi version for {package.pypi}, error: {e}"
            )
            return None

    @overload
    def guess_index_url(
        self, package: str, *, should_die_if_not_found: Literal[True]
    ) -> str: ...
    def guess_index_url(
        self, package: str, *, should_die_if_not_found: bool
    ) -> str | None:
        data = self.fetch_pypi_data(package, refresh=False)
        pypi_info = json.loads(data).get("info", {})
        candidates = list((pypi_info.get("project_urls") or {}).values())
        candidates.append(pypi_info.get("description", ""))

        readthedocs_urls = set()

        for url in candidates:
            for match in _RTD_URL_PATTERN.findall(url):
                readthedocs_urls.add(f"https://{match}")

        if len(readthedocs_urls) == 1:
            url = next(iter(readthedocs_urls))
            try:
                with urlopen(url) as f:
                    url = f.url  # Maybe redirected URL.
                return url
            except error.URLError as e:
                console.warning(f"Failed to fetch {url}, error: {e}")
                readthedocs_urls = []

        msg_fn = console.fatal if should_die_if_not_found else console.warning
        if len(readthedocs_urls) == 0:
            msg_fn(f"No readthedocs.io URLs found for package: {package}")
        else:
            msg_fn(
                f"Multiple readthedocs.io URLs found for package: {package}. URLs:\n"
                + "\n".join(readthedocs_urls)
            )


def _fetch_latest_cpython_version() -> version.Version | None:
    try:
        with urlopen("https://endoflife.date/api/python.json") as f:
            content = f.read().decode("utf-8")
        latest_version = version.parse("3.13.5")  # Known version as of 2025-06-28
        cycles = json.loads(content)
        for cycle in cycles:
            if (latest := version.parse(cycle["latest"])) > latest_version:
                latest_version = latest
        return latest_version
    except error.URLError as e:
        console.warning(f"Failed to fetch latest CPython version, error: {e}")
        return None
