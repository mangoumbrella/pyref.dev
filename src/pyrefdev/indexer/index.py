import dataclasses
import datetime
import json
import re
import random
import subprocess
import tempfile
import threading
import time
from email import utils as email_utils
from pathlib import Path
from typing import Literal, overload
from urllib import error, request

from packaging import version
from cyclopts import Parameter

from pyrefdev import __version__
from pyrefdev.config import Package, console


_RTD_URL_PATTERN = re.compile(r"https?://([^\s/]+\.readthedocs\.io)\b")
_BACKOFF_SECONDS = [1, 2, 5, 15, 30, 60, 120, 300, 600, 1800, 3600]
# A 5xx surviving a few retries is a broken page, not a transient blip.
_SERVER_ERROR_BACKOFF_SECONDS = [1, 5, 15]
_MAX_RETRY_AFTER_SECONDS = 300


def _retry_after_seconds(e: error.HTTPError) -> float | None:
    """Delay requested by a Retry-After header, which may be seconds or a date."""
    value = e.headers.get("Retry-After") if e.headers else None
    if not value:
        return None
    if value.strip().isdigit():
        return float(value)
    try:
        retry_at = email_utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if retry_at.tzinfo is None:
        retry_at = retry_at.replace(tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    return max((retry_at - now).total_seconds(), 0.0)


def urlopen(url: str, *, stop: threading.Event | None = None):
    req = request.Request(
        url,
        method="GET",
        headers={"User-Agent": f"pyrefdev/{__version__} (+https://pyref.dev)"},
    )
    attempt = 0

    while True:
        try:
            return request.urlopen(req, timeout=60)
        except error.HTTPError as e:
            if e.code == 429:  # Too Many Requests
                backoffs = _BACKOFF_SECONDS
            elif 500 <= e.code < 600:
                backoffs = _SERVER_ERROR_BACKOFF_SECONDS
            else:
                raise
            last_error = e
            reason = f"HTTP {e.code} ({e.reason})"
        except (TimeoutError, error.URLError) as e:
            if isinstance(e, error.URLError) and not isinstance(
                e.reason, (TimeoutError, OSError)
            ):
                raise
            backoffs = _BACKOFF_SECONDS
            last_error = e
            reason = "Timeout/Network error"

        if attempt >= len(backoffs):
            console.warning(
                f"{reason} for {url}. Giving up after {attempt + 1} attempts."
            )
            raise last_error
        backoff = backoffs[attempt] * (0.9 + random.random() / 5.0)
        if isinstance(last_error, error.HTTPError):
            retry_after = _retry_after_seconds(last_error)
            if retry_after is not None:
                # Obey the server's pacing, but never let it stall the crawl.
                backoff = min(max(retry_after, backoff), _MAX_RETRY_AFTER_SECONDS)
        attempt += 1
        console.warning(
            f"{reason} for {url}. Retrying in {backoff:.1f}s (attempt {attempt})..."
        )
        if stop is None:
            time.sleep(backoff)
        elif stop.wait(backoff):
            # The ladder runs for hours, so a stopped crawl must not sit through it.
            raise last_error


@dataclasses.dataclass
class IndexState:
    package_version: str
    # file -> the URL the content actually came from, so that the file's path is
    # always what save_path() derives from that URL. Relative links inside the
    # file resolve against it correctly.
    file_to_urls: dict[str, str]
    # url -> error_code (e.g. "http-404", or "" for unknown)
    failed_urls: dict[str, str]
    # requested url -> url it redirected to. Kept so a resumed crawl knows the
    # requested URL was already visited even though the file records the target.
    redirects: dict[str, str] = dataclasses.field(default_factory=dict)
    # URLs that were discovered but never fetched, i.e. the frontier a stopped
    # crawl has to resume from. Empty for a crawl that ran to exhaustion.
    pending_urls: list[str] = dataclasses.field(default_factory=list)
    # Defaults to False so that state written before this field existed is
    # resumed rather than mistaken for a finished crawl.
    completed: bool = False

    def recorded_nothing(self) -> bool:
        """Whether no URL in this state ever reached a terminal outcome.

        Saving a page, failing to fetch one, and following a redirect out of the
        docs all leave a trace, so a state with none of them never observed the
        site at all. Resuming one finds an empty frontier and would declare the
        crawl finished without making a single request.
        """
        return not (self.file_to_urls or self.failed_urls or self.redirects)

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
        (self.docs_directory / "__metadata__").mkdir(parents=True, exist_ok=True)

    def load_last_updated_package(self) -> str | None:
        self._ensure_directory()
        metadata_file = (
            self.docs_directory / "__metadata__" / "last_updated_package.txt"
        )
        if not metadata_file.exists():
            return None
        return metadata_file.read_text().strip()

    def save_last_updated_package(self, package: str) -> None:
        self._ensure_directory()
        metadata_file = (
            self.docs_directory / "__metadata__" / "last_updated_package.txt"
        )
        metadata_file.write_text(package)

    def load_crawl_state(self, package: str) -> IndexState | None:
        self._ensure_directory()
        crawl_state_file = self.docs_directory / f"{package}.json"
        if not crawl_state_file.exists():
            return None
        try:
            return IndexState.loads(crawl_state_file.read_text(encoding="utf-8"))
        except (ValueError, TypeError) as e:
            # A truncated or outdated state file should re-crawl, not crash.
            console.warning(f"Ignoring unreadable crawl state for {package}: {e}")
            return None

    def save_crawl_state(self, package: str, crawl_state: IndexState) -> None:
        self._ensure_directory()
        crawl_state_file = self.docs_directory / f"{package}.json"
        # Write atomically so an interrupt cannot truncate the previous state.
        tmp_file = crawl_state_file.with_suffix(".json.tmp")
        tmp_file.write_text(crawl_state.dumps(), encoding="utf-8")
        tmp_file.replace(crawl_state_file)

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
        # URLError is an OSError; InvalidVersion/JSONDecodeError are ValueErrors.
        except (OSError, ValueError, KeyError, TypeError) as e:
            console.warning(
                f"Failed to fetch pypi version for {package.pypi}, error: {e}"
            )
            return None

    @overload
    def guess_index_url(
        self, package: str, *, should_die_if_not_found: Literal[True]
    ) -> str: ...
    @overload
    def guess_index_url(
        self, package: str, *, should_die_if_not_found: bool
    ) -> str | None: ...
    def guess_index_url(self, package, *, should_die_if_not_found):
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
    except (OSError, ValueError, KeyError, TypeError) as e:
        console.warning(f"Failed to fetch latest CPython version, error: {e}")
        return None
