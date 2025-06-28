from pathlib import Path
import tempfile

from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.parse_docs import parse_docs


def update_docs(
    *,
    package: str | None = None,
    docs_directory: Path | None = None,
) -> None:
    if docs_directory is None:
        docs_directory = Path(tempfile.mkdtemp(prefix="pyref.dev."))
    crawl_docs(docs_directory, package=package)
    parse_docs(docs_directory, package=package, in_place=True)
