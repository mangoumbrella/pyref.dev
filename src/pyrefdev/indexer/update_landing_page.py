from pathlib import Path
import re

from pyrefdev.config import console, Package, SUPPORTED_PACKAGES
from pyrefdev import mapping


def update_landing_page(file: Path | None = None) -> None:
    """Update the landing page."""
    update_landing_page_with_packages(SUPPORTED_PACKAGES, file)


def update_count(content: str, name: str, value: int, file: Path) -> str:
    """Update every data-count="<name>" figure in the landing page."""
    # The surrounding whitespace is captured and put back rather than
    # normalised: the formatter puts a figure on its own line once the line
    # grows past its print width, and rewriting that to one line would make the
    # two tools fight over the file.
    new_content, replaced = re.subn(
        rf'(data-count="{name}">\s*)[0-9][0-9,]*(?:\.[0-9]+)*(\s*</)',
        rf"\g<1>{value:,}\g<2>",
        content,
    )
    if not replaced:
        console.fatal(f'{file} has no data-count="{name}" figure')
    return new_content


def update_landing_page_with_packages(
    pkgs: dict[str, Package], file: Path | None = None
) -> None:
    if file is None:
        file = Path(__file__).parent.parent.parent.parent / "templates" / "index.html"
        if not file.exists():
            console.fatal(f"{file} does not exist")

    packages = sorted(
        (p for p in pkgs.values() if not p.is_cpython()),
        key=lambda p: p.pypi,
    )
    content = file.read_text()

    # The indentation comes from the marker itself rather than being assumed,
    # so the block stays aligned if the template is ever reindented. The list is
    # marked prettier-ignore in the template, which is what keeps one package
    # per line: the formatter would otherwise expand each <li> to four.
    def replace_packages(match: re.Match[str]) -> str:
        indent = match.group(1)
        return "\n".join(
            [
                f"{indent}<!-- BEGIN PYPI PACKAGES -->",
                *[
                    f'{indent}<li><a href="{p.index_url}">{p.pypi}</a></li>'
                    for p in packages
                ],
                f"{indent}<!-- END PYPI PACKAGES -->",
            ]
        )

    new_content, replaced = re.subn(
        r"^([ \t]*)<!-- BEGIN PYPI PACKAGES -->.*?^[ \t]*<!-- END PYPI PACKAGES -->",
        replace_packages,
        content,
        flags=re.DOTALL | re.MULTILINE,
    )
    if replaced != 1:
        console.fatal(f"{file} has no <!-- BEGIN/END PYPI PACKAGES --> block")

    # Both the hero figure and the "N total" above the package index carry
    # data-count="packages", so one substitution keeps them in step.
    num_packages = len(SUPPORTED_PACKAGES)
    new_content = update_count(new_content, "packages", num_packages, file)
    all_symbols, _ = mapping.load_mapping(verify_duplicates=False)
    new_content = update_count(new_content, "symbols", len(all_symbols), file)

    file.write_text(new_content)
