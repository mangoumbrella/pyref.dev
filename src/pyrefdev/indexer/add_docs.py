import importlib
import json
from pathlib import Path
import re

from pyrefdev import config
from pyrefdev.config import console
from pyrefdev.indexer.requests import fetch_pypi_data, urlopen
from pyrefdev.indexer.update_docs import update_docs
from pyrefdev.indexer.update_landing_page import update_landing_page_with_packages


_MARKER = re.compile("(\n.*ENTRY-LINE-MARKER.*\n)")


def add_docs(
    *,
    package: str,
    docs_directory: Path | None = None,
    url: str | None = None,
    namespaces: list[str] | None = None,
    crawl: bool = True,
    num_threads_per_package: int | None = None,
) -> None:
    if package in config.SUPPORTED_PACKAGES:
        console.fatal(f"Package exists: {package}")

    if url is None:
        url = _guess_index_url_or_die(package, docs_directory)

    if namespaces:
        ns_content = ", ".join(f'"{ns}"' for ns in namespaces)
        ns_str = f", namespaces=[{ns_content}]"
    else:
        ns_str = ""
    config_entry = f'\n    Package(pypi="{package}"{ns_str}, index_url="{url}"),'
    config_file = Path(config.__file__)
    config_content = config_file.read_text()
    config_content = _MARKER.sub(config_entry + r"\g<1>", config_content)
    config_file.write_text(config_content)

    if crawl:
        importlib.reload(config)
        update_docs(
            docs_directory=docs_directory,
            package=package,
            num_threads_per_package=num_threads_per_package,
        )
        update_landing_page_with_packages(config.SUPPORTED_PACKAGES)


_URL_PATTERN = re.compile(r"https?://([^\s/]+\.readthedocs\.io)\b")


def _guess_index_url_or_die(package: str, docs_directory: Path) -> str:
    pypi_data_file = docs_directory / "__pypi__" / f"{package}.json"
    if pypi_data_file.exists():
        data = pypi_data_file.read_bytes()
    else:
        data = fetch_pypi_data(package)
    pypi_info = json.loads(data).get("info", {})
    candidates = list(pypi_info.get("project_urls", {}).values())
    candidates.append(pypi_info.get("description", ""))

    readthedocs_urls = set()

    for url in candidates:
        for match in _URL_PATTERN.findall(url):
            readthedocs_urls.add(f"https://{match}")

    if len(readthedocs_urls) == 1:
        url = next(iter(readthedocs_urls))
        with urlopen(url) as f:
            url = f.url  # Maybe redirected URL.
        return url
    elif len(readthedocs_urls) == 0:
        console.fatal(f"No readthedocs.io URLs found for package: {package}")
    else:
        console.fatal(
            f"Multiple readthedocs.io URLs found for package: {package}. URLs:\n"
            + "\n".join(readthedocs_urls)
        )
