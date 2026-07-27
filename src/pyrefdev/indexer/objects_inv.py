"""Parser for Sphinx ``objects.inv`` inventory files.

See https://sphobjinv.readthedocs.io/en/stable/syntax.html for the format.
"""

import dataclasses
import re
import zlib
from urllib.parse import urljoin


FILENAME = "objects.inv"

_NUM_HEADER_LINES = 4
_INVENTORY_VERSION_LINE = re.compile(rb"^#\s*Sphinx inventory version (\S+)\s*$")
_PROJECT_LINE = re.compile(rb"^#\s*Project:\s*(.*?)\s*$")
_VERSION_LINE = re.compile(rb"^#\s*Version:\s*(.*?)\s*$")
# name may contain spaces, so it is matched non-greedily, like Sphinx does.
_ENTRY_LINE = re.compile(
    r"^(?P<name>.+?)\s+(?P<domain>[^\s:]+):(?P<role>\S+)\s+"
    r"(?P<priority>-?\d+)\s+(?P<uri>\S*)\s+(?P<dispname>.+)$"
)


class ObjectsInvError(ValueError):
    """Raised when an objects.inv file cannot be parsed."""


@dataclasses.dataclass(frozen=True)
class InventoryEntry:
    name: str
    domain: str
    role: str
    priority: int
    # Relative to the location of the objects.inv file, with the trailing "$"
    # abbreviation already expanded.
    uri: str
    dispname: str

    def url(self, base_url: str) -> str:
        return urljoin(base_url, self.uri)


@dataclasses.dataclass(frozen=True)
class Inventory:
    project: str
    version: str
    entries: list[InventoryEntry]


def parse(data: bytes) -> Inventory:
    """Parse the content of a version 2 objects.inv file."""
    lines = data.split(b"\n", _NUM_HEADER_LINES)
    if len(lines) <= _NUM_HEADER_LINES:
        raise ObjectsInvError("Truncated objects.inv: missing header.")
    inventory_version_line, project_line, version_line, compression_line, body = lines

    if match := _INVENTORY_VERSION_LINE.match(inventory_version_line.rstrip(b"\r")):
        inventory_version = match.group(1).decode("utf-8", errors="replace")
    else:
        raise ObjectsInvError(
            f"Unrecognized objects.inv header: {inventory_version_line[:80]!r}"
        )
    if inventory_version != "2":
        raise ObjectsInvError(
            f"Unsupported objects.inv version: {inventory_version}, only version 2 is supported."
        )

    project = _parse_header_field(_PROJECT_LINE, project_line, "Project")
    version = _parse_header_field(_VERSION_LINE, version_line, "Version")
    if b"zlib" not in compression_line:
        raise ObjectsInvError(
            f"Expected a zlib compressed objects.inv body, got: {compression_line[:80]!r}"
        )

    try:
        decompressed = zlib.decompress(body)
    except zlib.error as e:
        raise ObjectsInvError(f"Failed to decompress objects.inv body: {e}") from e
    try:
        content = decompressed.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ObjectsInvError(f"objects.inv body is not valid UTF-8: {e}") from e

    entries = []
    for line in content.splitlines():
        if entry := _parse_entry(line):
            entries.append(entry)
    return Inventory(project=project, version=version, entries=entries)


def _parse_header_field(pattern: re.Pattern[bytes], line: bytes, name: str) -> str:
    match = pattern.match(line.rstrip(b"\r"))
    if not match:
        raise ObjectsInvError(f"Missing '# {name}:' line in objects.inv: {line[:80]!r}")
    return match.group(1).decode("utf-8", errors="replace")


def _parse_entry(line: str) -> InventoryEntry | None:
    match = _ENTRY_LINE.match(line.rstrip())
    if not match:
        return None
    name = match.group("name")
    uri = match.group("uri")
    if uri.endswith("$"):
        # "$" abbreviates the anchor, which is the object name.
        uri = uri[:-1] + name
    dispname = match.group("dispname")
    return InventoryEntry(
        name=name,
        domain=match.group("domain"),
        role=match.group("role"),
        priority=int(match.group("priority")),
        uri=uri,
        # "-" abbreviates a display name identical to the object name.
        dispname=name if dispname == "-" else dispname,
    )
