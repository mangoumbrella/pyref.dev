import multiprocessing
from pathlib import Path
import tempfile

from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.parse_docs import parse_docs


def update_docs(
    *,
    package: str | None = None,
    docs_directory: Path | None = None,
    force: bool = False,
    num_parallel_packages: int = multiprocessing.cpu_count(),
    num_threads_per_package: int | None = None,
) -> None:
    if docs_directory is None:
        docs_directory = Path(tempfile.mkdtemp(prefix="pyref.dev."))
    crawl_docs(
        package=package,
        docs_directory=docs_directory,
        force=force,
        num_parallel_packages=num_parallel_packages,
        num_threads_per_package=num_threads_per_package,
    )
    parse_docs(
        package=package,
        docs_directory=docs_directory,
        in_place=True,
        num_parallel_packages=num_parallel_packages,
    )
