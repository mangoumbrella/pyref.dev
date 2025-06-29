from pyrefdev import mapping
from pyrefdev import config


def test_no_duplicated_configs():
    assert len(config._packages) == len(config.SUPPORTED_PACKAGES)


def test_no_duplicated_mappings():
    verified_mapping = mapping.load_mapping(verify_duplicates=True)
    assert mapping.MAPPING == verified_mapping
