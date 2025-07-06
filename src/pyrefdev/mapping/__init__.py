import importlib

from pyrefdev.config import console, SUPPORTED_PACKAGES


def load_mapping(verify_duplicates: bool) -> dict[str, str]:
    mapping = {}
    for package in SUPPORTED_PACKAGES:
        try:
            package_module = importlib.import_module(f"pyrefdev.mapping.{package}")
        except ImportError:
            console.warning(f"Missing mapping for {package}")
            continue
        package_mapping = getattr(package_module, "MAPPING")
        if verify_duplicates:
            duplicates = set(mapping) & set(package_mapping)
            if duplicates:
                raise RuntimeError(
                    f"Found duplicated entries from {package}: {','.join(duplicates)}"
                )
        mapping.update(getattr(package_module, "MAPPING"))
    return mapping


MAPPING = load_mapping(verify_duplicates=False)
