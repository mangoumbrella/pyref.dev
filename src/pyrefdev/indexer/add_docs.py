import importlib
from pathlib import Path
import re

from pyrefdev import config
from pyrefdev.config import console
from pyrefdev.indexer.update_docs import update_docs
from pyrefdev.indexer.update_landing_page import update_landing_page_with_packages


_MARKER = re.compile("(\n.*ENTRY-LINE-MARKER.*\n)")


def add_docs(
    *,
    package: str,
    docs_directory: Path | None = None,
    url: str,
    crawl: bool = True,
) -> None:
    if package in config.SUPPORTED_PACKAGES:
        console.fatal(f"Package exists: {package}")

    config_entry = f'\n    Package(pypi="{package}", index_url="{url}"),'
    config_file = Path(config.__file__)
    config_content = config_file.read_text()
    config_content = _MARKER.sub(config_entry + r"\g<1>", config_content)
    config_file.write_text(config_content)

    if crawl:
        importlib.reload(config)
        update_docs(docs_directory=docs_directory, package=package)
        update_landing_page_with_packages(config.SUPPORTED_PACKAGES)
