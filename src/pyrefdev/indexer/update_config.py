import re
from pathlib import Path

from pyrefdev import config
from pyrefdev.config import console, ALL_PACKAGES


_PACKAGE_LINE = re.compile(
    r'^(\s*Package\(pypi="([^"]+)")(.*?)(, indexed=False)?(\),?)$',
    re.MULTILINE,
)


def update_config() -> None:
    """Update indexed=False flags in config.py."""
    config_file = Path(config.__file__)
    config_content = config_file.read_text()

    def replace_package_line(match: re.Match) -> str:
        prefix = match.group(1)
        package_name = match.group(2)
        middle = match.group(3)
        indexed_false_flag = match.group(4)
        closing = match.group(5)

        is_indexed = package_name in ALL_PACKAGES
        has_indexed_false = indexed_false_flag is not None

        if is_indexed and has_indexed_false:
            console.print(f"Removing indexed=False for {package_name}")
            return f"{prefix}{middle}{closing}"
        elif not is_indexed and not has_indexed_false:
            console.print(f"Adding indexed=False for {package_name}")
            return f"{prefix}{middle}, indexed=False{closing}"
        else:
            return match.group(0)

    updated_content = _PACKAGE_LINE.sub(replace_package_line, config_content)

    if updated_content != config_content:
        config_file.write_text(updated_content)
        console.print("Updated config.py")
    else:
        console.print("No changes needed")
