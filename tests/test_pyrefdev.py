from pyrefdev import mapping
from pyrefdev import config


def test_no_duplicated_configs():
    assert len(config._packages) == len(config.SUPPORTED_PACKAGES)


def test_no_duplicated_mappings():
    verified_mapping, verified_mapping_by_package = mapping.load_mapping(
        verify_duplicates=True
    )
    assert mapping.MAPPING == verified_mapping
    assert mapping.MAPPING_BY_PACKAGE == verified_mapping_by_package
    assert sorted(mapping.MAPPING_BY_PACKAGE) == sorted(config.SUPPORTED_PACKAGES)
