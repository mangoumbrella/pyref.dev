from pyrefdev.indexer.index import Index
from pyrefdev.indexer.add_docs import update_config
from pyrefdev.config import SUPPORTED_PACKAGES


def parse_pypi(*, index: Index = Index()) -> None:
    """Parse PyPI data and add new packages to the config."""
    for pypi in index.get_pypi_packages():
        if pypi in SUPPORTED_PACKAGES:
            continue
        url = index.guess_index_url(pypi, should_die_if_not_found=False)
        if url is None:
            continue
        update_config(pypi, url, None)
