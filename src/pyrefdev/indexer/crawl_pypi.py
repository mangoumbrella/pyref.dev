import json
from urllib.error import HTTPError

from rich.progress import track

from pyrefdev.config import console
from pyrefdev.indexer.index import Index, urlopen


def crawl_pypi(*, refresh: bool = True, index: Index = Index()) -> None:
    """Crawl top 15000 PyPI packages."""
    with urlopen(
        "https://hugovk.github.io/top-pypi-packages/top-pypi-packages.min.json"
    ) as f:
        top_packages_data = json.load(f)
    rows = top_packages_data["rows"]
    for row in track(
        rows, description=f"Reading {len(rows)} packages", console=console
    ):
        package_name = row["project"]
        try:
            index.fetch_pypi_data(package_name, refresh=refresh)
        except HTTPError as e:
            if e.code == 404:
                console.warning(f"Package {package_name} not found")
                continue
            raise
