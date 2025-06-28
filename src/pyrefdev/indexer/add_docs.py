import importlib
from pathlib import Path
import re

from pyrefdev import config
from pyrefdev import mapping
from pyrefdev.config import console
from pyrefdev.indexer.update_docs import update_docs


_MARKER = re.compile("(\n.*ENTRY-LINE-MARKER.*\n)")


def add_docs(
    package: str,
    *,
    index: str,
    crawler_root: str,
    pypi: str | None = None,
    docs_directory: Path | None = None,
) -> None:
    if package in config.SUPPORTED_PACKAGES:
        console.fatal(f"Package exists: {package}")
    pypi = pypi or package

    config_entry = f"""
    "{package}": Package(
        package="{package}",
        pypi="{pypi}",
        index="{index}",
        crawler_root="{crawler_root}",
    ),"""
    config_file = Path(config.__file__)
    config_content = config_file.read_text()
    config_content = _MARKER.sub(config_entry + r"\g<1>", config_content)
    config_file.write_text(config_content)

    mapping_file = Path(mapping.__file__).parent / f"{package}.py"
    mapping_file.write_text("MAPPING = {}")

    index_entry = f"""
            <li><a href="{index}" class="package-name">{pypi}</a></li>"""
    index_file = Path(config.__file__).parent.parent.parent / "index.html"
    index_content = index_file.read_text()
    index_content = _MARKER.sub(index_entry + r"\g<1>", index_content)
    index_file.write_text(index_content)

    importlib.reload(config)
    update_docs(package, docs_directory=docs_directory)
