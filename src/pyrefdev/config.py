import dataclasses

from yib import yconsole


console = yconsole.Console(stderr=True)


@dataclasses.dataclass
class Package:
    pypi: str
    # The crawler will crawl URLs with the same prefix until the last slash.
    index_url: str
    namespaces: list[str] = dataclasses.field(default_factory=list)
    exclude_root_urls: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if not self.namespaces:
            self.namespaces = [self.pypi.replace("-", "_")]

    def is_cpython(self):
        return self.pypi == "__python__"


SUPPORTED_PACKAGES: dict[str, Package] = {
    "__python__": Package(
        pypi="__python__",
        index_url="https://docs.python.org/3/library",
        exclude_root_urls=[
            "https://docs.python.org/3/copyright.html",  # Conflict with built-in copyright.
        ],
    ),
    "numpy": Package(
        pypi="numpy",
        index_url="https://numpy.org/doc/stable/reference/index.html",
    ),
    "pandas": Package(
        pypi="pandas",
        index_url="https://pandas.pydata.org/docs/reference/index.html",
    ),
    "urllib3": Package(
        pypi="urllib3",
        index_url="https://urllib3.readthedocs.io/en/stable/reference/index.html",
    ),
    "requests": Package(
        pypi="requests",
        index_url="https://requests.readthedocs.io/en/latest/",
    ),
    "dateutil": Package(
        pypi="python-dateutil",
        namespaces=["dateutil"],
        index_url="https://dateutil.readthedocs.io/en/stable/",
    ),
    "boto3": Package(
        pypi="boto3",
        index_url="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html",
        exclude_root_urls=[
            # TODO: Support boto services.
            "https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/",
        ],
    ),
    "botocore": Package(
        pypi="botocore",
        index_url="https://botocore.amazonaws.com/v1/documentation/api/latest/index.html",
        exclude_root_urls=[
            # TODO: Support boto services.
            "https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/",
        ],
    ),
    "setuptools": Package(
        pypi="setuptools",
        index_url="https://setuptools.pypa.io/en/latest/",
    ),
    "charset-normalizer": Package(
        pypi="charset-normalizer",
        index_url="https://charset-normalizer.readthedocs.io/en/latest/",
    ),
    "typing-extensions": Package(
        pypi="typing-extensions",
        index_url="https://typing-extensions.readthedocs.io/en/latest/",
    ),
    "packaging": Package(
        pypi="packaging",
        index_url="https://packaging.pypa.io/en/stable/",
    ),
    "s3fs": Package(
        pypi="s3fs",
        index_url="https://s3fs.readthedocs.io/en/latest/",
    ),
    "six": Package(
        pypi="six",
        index_url="https://six.readthedocs.io/",
    ),
    "protobuf": Package(
        pypi="protobuf",
        index_url="https://googleapis.dev/python/protobuf/latest/",
        namespaces=["google.protobuf"],
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
