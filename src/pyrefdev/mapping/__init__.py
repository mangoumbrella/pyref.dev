import dataclasses
import importlib

from pyrefdev.config import console, SUPPORTED_PACKAGES


@dataclasses.dataclass(frozen=True, kw_only=True)
class PackageInfo:
    version: str
    mapping: dict[str, str]


def load_mapping(
    verify_duplicates: bool,
) -> tuple[dict[str, str], dict[str, PackageInfo]]:
    mapping = {}
    packages = {}
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
        mapping.update(package_mapping)
        packages[package] = PackageInfo(
            version=getattr(package_module, "VERSION"), mapping=package_mapping
        )
    return mapping, packages


MAPPING, PACKAGE_INFO_MAPPING = load_mapping(verify_duplicates=False)
