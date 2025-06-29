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


# fmt: off
_packages = [
    Package(
        pypi="__python__",
        index_url="https://docs.python.org/3/library",
        exclude_root_urls=[
            "https://docs.python.org/3/copyright.html",  # Conflict with built-in copyright.
        ],
    ),
    Package(pypi="boto3", index_url="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html", exclude_root_urls=["https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/"]),  # TODO: Support boto services
    Package(pypi="botocore", index_url="https://botocore.amazonaws.com/v1/documentation/api/latest/index.html", exclude_root_urls=["https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/"]),  # TODO: Support boto services
    Package(pypi="charset-normalizer", index_url="https://charset-normalizer.readthedocs.io/en/latest/"),
    Package(pypi="google-api-core", namespaces=["google.api_core"], index_url="https://googleapis.dev/python/google-api-core/latest/"),
    Package(pypi="numpy", index_url="https://numpy.org/doc/stable/reference/index.html"),
    Package(pypi="packaging", index_url="https://packaging.pypa.io/en/stable/"),
    Package(pypi="pandas", index_url="https://pandas.pydata.org/docs/reference/index.html"),
    Package(pypi="protobuf", index_url="https://googleapis.dev/python/protobuf/latest/",namespaces=["google.protobuf"]),
    Package(pypi="python-dateutil", namespaces=["dateutil"], index_url="https://dateutil.readthedocs.io/en/stable/"),
    Package(pypi="requests", index_url="https://requests.readthedocs.io/en/latest/"),
    Package(pypi="s3fs", index_url="https://s3fs.readthedocs.io/en/latest/"),
    Package(pypi="setuptools", index_url="https://setuptools.pypa.io/en/latest/"),
    Package(pypi="six", index_url="https://six.readthedocs.io/"),
    Package(pypi="typing-extensions", index_url="https://typing-extensions.readthedocs.io/en/latest/"),
    Package(pypi="urllib3", index_url="https://urllib3.readthedocs.io/en/stable/reference/index.html"),
    # ENTRY-LINE-MARKER
]
# fmt: on


SUPPORTED_PACKAGES: dict[str, Package] = {pkg.pypi: pkg for pkg in _packages}


def get_packages(package: str | None) -> list[Package]:
    if package is None:
        return list(SUPPORTED_PACKAGES.values())
    else:
        if package not in SUPPORTED_PACKAGES:
            console.fatal(f"No package named {package}")
        return [SUPPORTED_PACKAGES[package]]
