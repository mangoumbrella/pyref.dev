import multiprocessing

from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.index import Index
from pyrefdev.indexer.parse_docs import parse_docs
from pyrefdev.config import console, get_packages
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)
from pyrefdev.indexer.update_config import update_config


def update_docs(
    *,
    package: str | None = None,
    force: bool = False,
    upgrade: bool = True,
    retry_http_404: bool = False,
    index: Index = Index(),
    seconds_to_sleep_between_requests: float = 5.0,
    num_parallel_packages: int = multiprocessing.cpu_count(),
    num_threads_per_package: int = multiprocessing.cpu_count(),
) -> None:
    """Crawl and parse docs."""
    should_update_last_updated_package = package is None
    packages = get_packages(package)
    if (last_updated_package_name := index.load_last_updated_package()) is not None:
        package_names = [pkg.pypi for pkg in packages]
        try:
            first_index = package_names.index(last_updated_package_name)
        except ValueError:
            pass
        else:
            new_order = packages[first_index + 1 :] + packages[: first_index + 1]
            assert len(packages) == len(new_order)
            packages = new_order

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        expand=True,
    ) as progress:
        task = progress.add_task(f"Updating {len(packages)} packages")
        for pkg in packages:
            crawl_docs(
                package=pkg.pypi,
                index=index,
                force=force,
                upgrade=upgrade,
                retry_failed_urls=True,
                retry_http_404=retry_http_404,
                seconds_to_sleep_between_requests=seconds_to_sleep_between_requests,
                show_overall_progress=False,
            )
            parse_docs(
                package=pkg.pypi,
                index=index,
                in_place=True,
                reparse=True,
                num_parallel_packages=num_parallel_packages,
                num_threads_per_package=num_threads_per_package,
                show_overall_progress=False,
            )
            update_config()
            if should_update_last_updated_package:
                index.save_last_updated_package(pkg.pypi)
            progress.advance(task)
