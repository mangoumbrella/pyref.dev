import json
from pathlib import Path

from rich.progress import track

from pyrefdev.config import console
from pyrefdev.indexer.requests import urlopen


def crawl_pypi(*, docs_directory: Path) -> None:
    pypi_directory = docs_directory / "__pypi__"
    pypi_directory.mkdir(parents=True, exist_ok=True)
    with urlopen(
        "https://hugovk.github.io/top-pypi-packages/top-pypi-packages.min.json"
    ) as f:
        top_packages_data = json.load(f)
    rows = top_packages_data["rows"]
    for row in track(
        rows, description=f"Reading {len(rows)} packages", console=console
    ):
        package_name = row["project"]
        with urlopen(f"https://pypi.org/pypi/{package_name}/json") as f:
            data = f.read()
        (pypi_directory / f"{package_name}.json").write_bytes(data)
