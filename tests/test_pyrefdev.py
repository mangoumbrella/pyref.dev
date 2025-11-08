from pyrefdev import mapping
from pyrefdev import config


def test_no_duplicated_configs():
    assert len([pkg for pkg in config._packages if pkg.indexed]) == len(
        config.SUPPORTED_PACKAGES
    )


def test_no_duplicated_mappings():
    verified_mapping, packages = mapping.load_mapping(verify_duplicates=True)
    assert mapping.MAPPING == verified_mapping
    assert mapping.PACKAGE_INFO_MAPPING == packages
    assert sorted(mapping.PACKAGE_INFO_MAPPING) == sorted(config.SUPPORTED_PACKAGES)
