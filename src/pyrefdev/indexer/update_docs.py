import multiprocessing

from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.index import Index
from pyrefdev.indexer.parse_docs import parse_docs
from pyrefdev.config import console, get_packages
from rich.progress import track
from pyrefdev.indexer.update_config import update_config


def update_docs(
    *,
    package: str | None = None,
    force: bool = False,
    upgrade: bool = True,
    retry_failed_urls: bool = True,
    retry_http_404: bool = False,
    index: Index = Index(),
    num_parallel_packages: int = multiprocessing.cpu_count(),
    num_threads_per_package: int = multiprocessing.cpu_count(),
) -> None:
    """Crawl and parse docs."""
    packages = get_packages(package)
    if (last_updated_package_name := index.load_last_updated_package()) is not None:
        package_names = [pkg.pypi for pkg in packages]
        try:
            first_index = package_names.index(last_updated_package_name)
        except ValueError:
            pass
        else:
            new_order = packages[first_index:] + packages[:first_index]
            assert len(packages) == len(new_order)
            packages = new_order

    for pkg in track(
        packages, description=f"Updating {len(packages)} packages", console=console
    ):
        crawl_docs(
            package=pkg.pypi,
            index=index,
            force=force,
            upgrade=upgrade,
            retry_failed_urls=retry_failed_urls,
            retry_http_404=retry_http_404,
        )
        parse_docs(
            package=pkg.pypi,
            index=index,
            in_place=True,
            reparse=True,
            num_parallel_packages=num_parallel_packages,
            num_threads_per_package=num_threads_per_package,
        )
        update_config()
        index.save_last_updated_package(pkg.pypi)
