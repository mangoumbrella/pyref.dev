from pyrefdev import mapping


def test_no_duplicates():
    verified_mapping = mapping.load_mapping(verify_duplicates=True)
    assert mapping.MAPPING == verified_mapping
