import multiprocessing

from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.index import Index
from pyrefdev.indexer.parse_docs import parse_docs
from pyrefdev.indexer.update_configs import update_configs


def update_docs(
    *,
    package: str | None = None,
    upgrade: bool = False,
    retry_failed_urls: bool = True,
    retry_http_404: bool = False,
    index: Index = Index(),
    num_parallel_packages: int = multiprocessing.cpu_count(),
    num_threads_per_package: int = multiprocessing.cpu_count(),
) -> None:
    """Crawl and parse docs."""
    crawl_docs(
        package=package,
        index=index,
        upgrade=upgrade,
        retry_failed_urls=retry_failed_urls,
        retry_http_404=retry_http_404,
    )
    parse_docs(
        package=package,
        index=index,
        in_place=True,
        num_parallel_packages=num_parallel_packages,
        num_threads_per_package=num_threads_per_package,
    )
    update_configs()
