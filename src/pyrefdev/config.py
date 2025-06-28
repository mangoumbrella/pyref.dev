import dataclasses

from yib import yconsole


console = yconsole.Console(stderr=True)


@dataclasses.dataclass
class Package:
    package: str
    pypi: str
    index: str  # The URL for pyref.dev/<name>.
    crawler_root: str  # The seed and root URL for crawler.

    def is_stdlib(self):
        return self.package == "__python__"


SUPPORTED_PACKAGES: dict[str, Package] = {
    "__python__": Package(
        package="__python__",
        pypi="__python__",
        index="https://docs.python.org/3/library",
        crawler_root="https://docs.python.org/3/",
    ),
    "numpy": Package(
        package="numpy",
        pypi="numpy",
        index="https://numpy.org/doc/stable/reference/index.html",
        crawler_root="https://numpy.org/doc/stable/reference/",
    ),
    "pandas": Package(
        package="pandas",
        pypi="pandas",
        index="https://pandas.pydata.org/docs/reference/index.html",
        crawler_root="https://pandas.pydata.org/docs/reference/",
    ),
    "urllib3": Package(
        package="urllib3",
        pypi="urllib3",
        index="https://urllib3.readthedocs.io/en/stable/reference/index.html",
        crawler_root="https://urllib3.readthedocs.io/en/stable/reference/",
    ),
    "requests": Package(
        package="requests",
        pypi="requests",
        index="https://requests.readthedocs.io/en/latest/",
        crawler_root="https://requests.readthedocs.io/en/latest/",
    ),
    "dateutil": Package(
        package="dateutil",
        pypi="python-dateutil",
        index="https://dateutil.readthedocs.io/en/stable/",
        crawler_root="https://dateutil.readthedocs.io/en/stable/",
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
