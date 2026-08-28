import os

import pytest

from pyrefdev import mapping
from pyrefdev.config import SUPPORTED_PACKAGES
from pyrefdev.indexer import build_index as build_index_module


# Indexing all ~2000 packages takes ~16s and ~450MB. These few cover what the
# query layer needs to distinguish: mixed casing, underscores, dotted paths and
# more than one package to scope a search to.
SMALL_PACKAGES = ["attrs", "chardet", "click", "packaging"]

_STALE_TIME = 1_000_000_000


@pytest.fixture(scope="session")
def small_packages() -> dict:
    return {name: SUPPORTED_PACKAGES[name] for name in SMALL_PACKAGES}


@pytest.fixture(scope="session")
def small_index(tmp_path_factory, small_packages):
    """A real index built from a handful of packages."""
    output = tmp_path_factory.mktemp("index") / "index.sqlite"
    original = build_index_module.SUPPORTED_PACKAGES
    build_index_module.SUPPORTED_PACKAGES = small_packages
    try:
        build_index_module.build_index(output)
    finally:
        build_index_module.SUPPORTED_PACKAGES = original
    return output


@pytest.fixture(scope="session")
def sqlite_backend(small_index):
    return mapping._SqliteBackend(small_index)


@pytest.fixture(scope="session")
def module_backend(small_packages):
    """The fallback backend, restricted to the same packages as `small_index`."""
    original = mapping.SUPPORTED_PACKAGES
    mapping.SUPPORTED_PACKAGES = small_packages
    try:
        return mapping._ModuleBackend()
    finally:
        mapping.SUPPORTED_PACKAGES = original


@pytest.fixture
def rebuildable_index(small_index, tmp_path):
    """A private copy of the index, for tests that rebuild it.

    Rebuilding the session-scoped index would swap the file out from under the
    backends bound to it, which Windows refuses outright.
    """
    copy = tmp_path / "index.sqlite"
    copy.write_bytes(small_index.read_bytes())
    # Backdated so that "was it rewritten?" does not rest on clock resolution.
    os.utime(copy, (_STALE_TIME, _STALE_TIME))
    return copy
