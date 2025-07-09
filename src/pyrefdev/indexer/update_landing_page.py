from pathlib import Path
import re

from pyrefdev.config import console, Package, SUPPORTED_PACKAGES
from pyrefdev.mapping import MAPPING


def update_landing_page(file: Path | None = None) -> None:
    update_landing_page_with_packages(SUPPORTED_PACKAGES, file)


def update_landing_page_with_packages(
    packages: dict[str, Package], file: Path | None = None
) -> None:
    if file is None:
        file = Path(__file__).parent.parent.parent.parent / "templates" / "index.html"
        if not file.exists():
            console.fatal(f"{file} does not exist")

    packages = sorted(
        (p for p in packages.values() if not p.is_cpython()),
        key=lambda p: p.pypi,
    )
    indent = "            "
    lines = [
        f"{indent}<!-- BEGIN PYPI PACKAGES -->",
        *[f'{indent}<li><a href="{p.index_url}">{p.pypi}</a></li>' for p in packages],
        f"{indent}<!-- END PYPI PACKAGES -->",
    ]
    new_content = re.sub(
        rf"{indent}<!-- BEGIN PYPI PACKAGES -->.*<!-- END PYPI PACKAGES -->",
        "\n".join(lines),
        file.read_text(),
        flags=re.DOTALL,
    )

    num_packages = len(SUPPORTED_PACKAGES)
    new_content = re.sub(
        r'(class="stat-number">)([0-9]+(?:\.[0-9]+)*)(</span> packages)',
        rf"\g<1>{num_packages:,}\g<3>",
        new_content,
    )
    num_symbols = len(MAPPING)
    new_content = re.sub(
        r'(class="stat-number">)([0-9]+(?:\.[0-9]+)*)(</span> symbols)',
        rf"\g<1>{num_symbols:,}\g<3>",
        new_content,
    )

    file.write_text(new_content)
