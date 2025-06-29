import json
from urllib import request, error

from packaging import version

from pyrefdev.config import console, Package


def urlopen(url: str) -> str:
    req = request.Request(
        url, method="GET", headers={"User-Agent": "https://pyref.dev"}
    )
    return request.urlopen(req, timeout=60)


def fetch_package_version(package: Package) -> version.Version | None:
    if package.is_cpython():
        return _fetch_latest_cpython_version()
    try:
        with urlopen(f"https://pypi.org/pypi/{package.pypi}/json") as f:
            content = f.read().decode("utf-8")
        pypi_info = json.loads(content)
        return version.parse(pypi_info["info"]["version"])
    except error.URLError as e:
        console.print(
            f"[yellow]WARNING:[/yellow] Failed to fetch pypi version for {package.pypi}, error: {e}"
        )
        return None


def _fetch_latest_cpython_version() -> version.Version | None:
    try:
        with urlopen("https://endoflife.date/api/python.json") as f:
            content = f.read().decode("utf-8")
        latest_version = version.parse("3.13.5")  # Known version as of 2025-06-28
        cycles = json.loads(content)
        for cycle in cycles:
            if (latest := version.parse(cycle["latest"])) > latest_version:
                latest_version = latest
        return latest_version
    except error.URLError as e:
        console.print(
            f"[yellow]WARNING:[/yellow] Failed to fetch latest CPython version, error: {e}"
        )
        return None
