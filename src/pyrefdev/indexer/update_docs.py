from pathlib import Path
import tempfile

from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.parse_docs import parse_docs


def update_docs(
    *,
    package: str | None = None,
    docs_directory: Path | None = None,
    num_parallel_packages: int = 2,
    num_threads_per_package: int = 2,
) -> None:
    if docs_directory is None:
        docs_directory = Path(tempfile.mkdtemp(prefix="pyref.dev."))
    crawl_docs(
        package=package,
        docs_directory=docs_directory,
        num_parallel_packages=num_parallel_packages,
        num_threads_per_package=num_threads_per_package,
    )
    parse_docs(package=package, docs_directory=docs_directory, in_place=True)
