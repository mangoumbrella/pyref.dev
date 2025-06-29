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
            self.pypi = self.package.replace("_", "-")

    def is_cpython(self):
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
    "boto3": Package(
        package="boto3",
        pypi="boto3",
        index_url="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html",
    ),
    "setuptools": Package(
        package="setuptools",
        pypi="setuptools",
        index_url="https://setuptools.pypa.io/en/latest/",
    ),
    "botocore": Package(
        package="botocore",
        pypi="botocore",
        index_url="https://botocore.amazonaws.com/v1/documentation/api/latest/index.html",
    ),
    "charset_normalizer": Package(
        package="charset_normalizer",
        pypi="charset_normalizer",
        index_url="https://charset-normalizer.readthedocs.io/en/latest/",
    ),
    "typing_extensions": Package(
        package="typing_extensions",
        pypi="typing_extensions",
        index_url="https://typing-extensions.readthedocs.io/en/latest/",
    ),
    "packaging": Package(
        package="packaging",
        pypi="packaging",
        index_url="https://packaging.pypa.io/en/stable/",
    ),
    "s3fs": Package(
        package="s3fs",
        pypi="s3fs",
        index_url="https://s3fs.readthedocs.io/en/latest/",
    ),
    "six": Package(
        package="six",
        pypi="six",
        index_url="https://six.readthedocs.io/",
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
