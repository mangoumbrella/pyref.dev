import importlib
from pathlib import Path
import re

from pyrefdev import config
from pyrefdev.config import console
from pyrefdev.indexer.index import Index
from pyrefdev.indexer.update_docs import update_docs
from pyrefdev.indexer.update_landing_page import update_landing_page_with_packages


_MARKER = re.compile("(\n.*ENTRY-LINE-MARKER.*\n)")


def add_docs(
    *,
    package: str,
    url: str | None = None,
    namespaces: list[str] | None = None,
    crawl: bool = True,
    index: Index = Index(),
    num_threads_per_package: int = 1,
) -> None:
    """Add a new package."""
    if package in config.SUPPORTED_PACKAGES:
        console.fatal(f"Package exists: {package}")

    if url is None:
        url = index.guess_index_url(package, should_die_if_not_found=True)
    update_config(package, url, namespaces)

    if crawl:
        importlib.reload(config)
        update_docs(
            index=index,
            package=package,
            num_threads_per_package=num_threads_per_package,
        )
        update_landing_page_with_packages(config.SUPPORTED_PACKAGES)


def update_config(package: str, url: str, namespaces: list[str] | None = None) -> None:
    if namespaces:
        ns_content = ", ".join(f'"{ns}"' for ns in namespaces)
        ns_str = f", namespaces=[{ns_content}]"
    else:
        ns_str = ""
    config_entry = (
        f'\n    Package(pypi="{package}"{ns_str}, index_url="{url}", indexed=False),'
    )
    config_file = Path(config.__file__)
    config_content = config_file.read_text()
    config_content = _MARKER.sub(config_entry + r"\g<1>", config_content)
    config_file.write_text(config_content)
