import importlib

from pyrefdev.config import SUPPORTED_DOCS


def load_mapping(verify_duplicates: bool) -> dict[str, str]:
    mapping = {}
    for site in SUPPORTED_DOCS:
        site_module = importlib.import_module(f"pyrefdev.mapping.{site}")
        site_mapping = getattr(site_module, "MAPPING")
        if verify_duplicates:
            duplicates = set(mapping) & set(site_mapping)
            if duplicates:
                raise RuntimeError(
                    f"Found duplicated entries from {site}: {','.join(duplicates)}"
                )
        mapping.update(getattr(site_module, "MAPPING"))
    return mapping


MAPPING = load_mapping(verify_duplicates=False)
