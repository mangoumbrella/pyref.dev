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
    Package(pypi="attrs", index_url="https://www.attrs.org/en/stable/", namespaces=["attrs", "attr"]),
    Package(pypi="boto3", index_url="https://boto3.amazonaws.com/v1/documentation/api/latest/index.html", exclude_root_urls=["https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/"]),  # TODO: Support boto services
    Package(pypi="botocore", index_url="https://botocore.amazonaws.com/v1/documentation/api/latest/index.html", exclude_root_urls=["https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/"]),  # TODO: Support boto services
    Package(pypi="charset-normalizer", index_url="https://charset-normalizer.readthedocs.io/en/latest/"),
    Package(pypi="cryptography", index_url="https://cryptography.io/en/latest/"),
    Package(pypi="fsspec", index_url="https://filesystem-spec.readthedocs.io/en/latest/"),
    Package(pypi="google-api-core", namespaces=["google.api_core"], index_url="https://googleapis.dev/python/google-api-core/latest/"),
    Package(pypi="numpy", index_url="https://numpy.org/doc/stable/reference/index.html"),
    Package(pypi="packaging", index_url="https://packaging.pypa.io/en/stable/"),
    Package(pypi="pandas", index_url="https://pandas.pydata.org/docs/reference/index.html"),
    Package(pypi="protobuf", index_url="https://googleapis.dev/python/protobuf/latest/",namespaces=["google.protobuf"]),
    Package(pypi="pydantic-core", index_url="https://docs.pydantic.dev/latest/"),
    Package(pypi="pydantic", index_url="https://docs.pydantic.dev/latest/"),
    Package(pypi="python-dateutil", namespaces=["dateutil"], index_url="https://dateutil.readthedocs.io/en/stable/"),
    Package(pypi="requests", index_url="https://requests.readthedocs.io/en/latest/"),
    Package(pypi="s3fs", index_url="https://s3fs.readthedocs.io/en/latest/"),
    Package(pypi="setuptools", index_url="https://setuptools.pypa.io/en/latest/"),
    Package(pypi="six", index_url="https://six.readthedocs.io/"),
    Package(pypi="typing-extensions", index_url="https://typing-extensions.readthedocs.io/en/latest/"),
    Package(pypi="urllib3", index_url="https://urllib3.readthedocs.io/en/stable/reference/index.html"),
    Package(pypi="platformdirs", index_url="https://platformdirs.readthedocs.io/en/latest/"),
    Package(pypi="click", index_url="https://click.palletsprojects.com/en/stable/"),
    Package(pypi="grpcio", index_url="https://grpc.github.io/grpc/python/index.html", namespaces=["grpc"]),
    Package(pypi="jinja2", index_url="https://jinja.palletsprojects.com/en/latest/"),
    Package(pypi="pyasn1", index_url="https://pyasn1.readthedocs.io/en/latest/contents.html"),
    Package(pypi="h11", index_url="https://h11.readthedocs.io/en/latest/"),
    Package(pypi="filelock", index_url="https://py-filelock.readthedocs.io/en/latest/"),
    Package(pypi="aiohttp", index_url="https://docs.aiohttp.org/en/stable/"),
    Package(pypi="cachetools", index_url="https://cachetools.readthedocs.io/en/latest/"),
    Package(pypi="pluggy", index_url="https://pluggy.readthedocs.io/en/latest/"),
    Package(pypi="markupsafe", index_url="https://markupsafe.palletsprojects.com/en/stable/"),
    Package(pypi="scipy", index_url="https://docs.scipy.org/doc/scipy/reference/index.html"),
    Package(pypi="propcache", index_url="https://propcache.aio-libs.org/en/latest/"),
    Package(pypi="pathspec", index_url="https://python-path-specification.readthedocs.io/en/latest/index.html"),
    Package(pypi="aiosignal", index_url="https://aiosignal.aio-libs.org/en/stable/"),
    Package(pypi="pyOpenSSL", namespaces=["OpenSSL"], index_url="https://www.pyopenssl.org/en/latest/"),
    Package(pypi="oauthlib", index_url="https://oauthlib.readthedocs.io/en/latest/"),
    Package(pypi="requests-toolbelt", index_url="https://toolbelt.readthedocs.io/en/latest/index.html"),
    Package(pypi="azure-identity", namespaces=["azure.identity"], index_url="https://azuresdkdocs.z19.web.core.windows.net/python/azure-identity/latest/index.html"),
    Package(pypi="distlib", index_url="https://distlib.readthedocs.io/en/latest/"),
    Package(pypi="pillow", namespaces=["PIL"], index_url="https://pillow.readthedocs.io/en/stable/"),
    Package(pypi="frozenlist", index_url="https://frozenlist.aio-libs.org/en/latest/"),
    Package(pypi="pyparsing", index_url="https://pyparsing-docs.readthedocs.io/en/latest/"),
    Package(pypi="tomlkit", index_url="https://tomlkit.readthedocs.io/en/latest/"),
    Package(pypi="rich", index_url="https://rich.readthedocs.io/en/latest/"),
    Package(pypi="sqlalchemy", index_url="https://docs.sqlalchemy.org/en/20/"),
    Package(pypi="requests-oauthlib", index_url="https://requests-oauthlib.readthedocs.io/en/latest/"),
    Package(pypi="yarl", index_url="https://yarl.aio-libs.org/en/latest/"),
    Package(pypi="multidict", index_url="https://multidict.aio-libs.org/en/stable/"),
    Package(pypi="pyarrow", index_url="https://arrow.apache.org/docs/python/api.html"),
    Package(pypi="sniffio", index_url="https://sniffio.readthedocs.io/en/latest/"),
    Package(pypi="jsonschema", index_url="https://python-jsonschema.readthedocs.io/en/stable/"),
    Package(pypi="google-auth", namespaces=["google.auth"], index_url="https://googleapis.dev/python/google-auth/latest/"),
    Package(pypi="pyjwt", namespaces=["jwt"], index_url="https://pyjwt.readthedocs.io/en/stable/"),
    Package(pypi="anyio", index_url="https://anyio.readthedocs.io/en/stable/"),
    Package(pypi="psutil", index_url="https://psutil.readthedocs.io/en/latest/"),
    Package(pypi="wrapt", index_url="https://wrapt.readthedocs.io/en/master/"),
    Package(pypi="pygments", index_url="https://pygments.org/docs/api/"),
    Package(pypi="rpds-py", namespaces=["rpds"], index_url="https://rpds.readthedocs.io/en/latest/"),
    Package(pypi="pytest", index_url="https://docs.pytest.org/en/stable/reference/index.html"),
    Package(pypi="libcst", index_url="https://libcst.readthedocs.io/en/latest/"),
    Package(pypi="numba", index_url="https://numba.readthedocs.io/en/stable/reference/index.html"),
    Package(pypi="trio", index_url="https://trio.readthedocs.io/en/stable/"),
    Package(pypi="tox", index_url="https://tox.wiki/en/stable/"),
    Package(pypi="h5py", index_url="https://docs.h5py.org/en/stable/"),
    Package(pypi="cattrs", index_url="https://catt.rs/en/stable/"),
    Package(pypi="nbformat", index_url="https://nbformat.readthedocs.io/en/latest/"),
    Package(pypi="semver", index_url="https://python-semver.readthedocs.io/en/latest/"),
    Package(pypi="aioitertools", index_url="https://aioitertools.omnilib.dev/en/stable/"),
    Package(pypi="torch", index_url="https://docs.pytorch.org/docs/stable/index.html"),
    Package(pypi="arrow", index_url="https://arrow.readthedocs.io/en/latest/"),
    Package(pypi="apache-beam", index_url="https://beam.apache.org/releases/pydoc/current/"),
    Package(pypi="fastapi", index_url="https://fastapi.tiangolo.com/reference/"),
    Package(pypi="flask", index_url="https://flask.palletsprojects.com/en/stable/"),
    Package(pypi="fastjsonschema", index_url="https://horejsek.github.io/python-fastjsonschema/"),
    Package(pypi="jupyter-core", index_url="https://jupyter-core.readthedocs.io/en/latest/"),
    Package(pypi="more-itertools", index_url="https://more-itertools.readthedocs.io/en/stable/"),
    Package(pypi="werkzeug", index_url="https://werkzeug.palletsprojects.com/en/stable/"),
    Package(pypi="scikit-learn", namespaces=["sklearn"], index_url="https://scikit-learn.org/stable/api/index.html"),
    Package(pypi="coverage", index_url="https://coverage.readthedocs.io/en/latest/"),
    Package(pypi="matplotlib", index_url="https://matplotlib.org/stable/api/index.html"),
    Package(pypi="networkx", index_url="https://networkx.org/documentation/stable/reference/index.html"),
    Package(pypi="ipython", index_url="https://ipython.readthedocs.io/en/stable/"),
    Package(pypi="httplib2", index_url="https://httplib2.readthedocs.io/en/latest/"),
    Package(pypi="cyclopts", index_url="https://cyclopts.readthedocs.io/en/latest/"),
    Package(pypi="yib", index_url="https://yib.readthedocs.io/en/latest/"),
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
