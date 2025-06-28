import dataclasses

from yib import yconsole


console = yconsole.Console(stderr=True)


@dataclasses.dataclass
class Package:
    package: str
    # The crawler will crawl URLs with the same prefix until the last slash.
    index_url: str
    pypi: str = ""

    def __post_init__(self):
        if not self.pypi:
            self.pypi = self.package

    def is_stdlib(self):
        return self.package == "__python__"


SUPPORTED_PACKAGES: dict[str, Package] = {
    "__python__": Package(
        package="__python__",
        index_url="https://docs.python.org/3/library",
    ),
    "numpy": Package(
        package="numpy",
        index_url="https://numpy.org/doc/stable/reference/index.html",
    ),
    "pandas": Package(
        package="pandas",
        index_url="https://pandas.pydata.org/docs/reference/index.html",
    ),
    "urllib3": Package(
        package="urllib3",
        index_url="https://urllib3.readthedocs.io/en/stable/reference/index.html",
    ),
    "requests": Package(
        package="requests",
        index_url="https://requests.readthedocs.io/en/latest/",
    ),
    "dateutil": Package(
        package="dateutil",
        index_url="https://dateutil.readthedocs.io/en/stable/",
        pypi="python-dateutil",
    ),
    # ENTRY-LINE-MARKER
}


def get_packages(package: str | None) -> list[Package]:
    if package is None:
        return list(SUPPORTED_PACKAGES.values())
    else:
        if package not in SUPPORTED_PACKAGES:
            console.fatal(f"No package named {package}")
        return [SUPPORTED_PACKAGES[package]]
