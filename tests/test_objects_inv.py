import zlib

import pytest

from pyrefdev.indexer import objects_inv


_HEADER = (
    b"# Sphinx inventory version 2\n"
    b"# Project: Starlette\n"
    b"# Version: None\n"
    b"# The remainder of this file is compressed using zlib.\n"
)


def build(body: str, header: bytes = _HEADER) -> bytes:
    return header + zlib.compress(body.encode("utf-8"))


def test_parse_starlette():
    data = build(
        "starlette.applications.Starlette py:class 1 applications/#$ -\n"
        "starlette.templating.Jinja2Templates py:class 1 templates/#$ -\n"
        "starlette.testclient.TestClient py:class 1 testclient/#$ -\n"
    )

    inventory = objects_inv.parse(data)

    assert inventory.project == "Starlette"
    assert inventory.version == "None"
    assert inventory.entries == [
        objects_inv.InventoryEntry(
            name="starlette.applications.Starlette",
            domain="py",
            role="class",
            priority=1,
            uri="applications/#starlette.applications.Starlette",
            dispname="starlette.applications.Starlette",
        ),
        objects_inv.InventoryEntry(
            name="starlette.templating.Jinja2Templates",
            domain="py",
            role="class",
            priority=1,
            uri="templates/#starlette.templating.Jinja2Templates",
            dispname="starlette.templating.Jinja2Templates",
        ),
        objects_inv.InventoryEntry(
            name="starlette.testclient.TestClient",
            domain="py",
            role="class",
            priority=1,
            uri="testclient/#starlette.testclient.TestClient",
            dispname="starlette.testclient.TestClient",
        ),
    ]


def test_url_is_relative_to_the_objects_inv():
    data = build("starlette.testclient.TestClient py:class 1 testclient/#$ -\n")

    (entry,) = objects_inv.parse(data).entries

    assert (
        entry.url("https://starlette.dev/objects.inv")
        == "https://starlette.dev/testclient/#starlette.testclient.TestClient"
    )


def test_parse_uri_without_abbreviation():
    data = build("requests py:module 0 api/#module-requests requests\n")

    (entry,) = objects_inv.parse(data).entries

    assert entry.uri == "api/#module-requests"
    assert entry.dispname == "requests"


def test_parse_name_with_spaces():
    data = build("1.x style std:term -1 glossary.html#term-1.x-style 1.x style\n")

    (entry,) = objects_inv.parse(data).entries

    assert entry.name == "1.x style"
    assert entry.domain == "std"
    assert entry.role == "term"
    assert entry.priority == -1
    assert entry.dispname == "1.x style"


def test_parse_skips_unparsable_lines():
    data = build(
        "\n"
        "not an entry\n"
        "missing:colon-in-domain 1 page.html#anchor -\n"
        "starlette.testclient.TestClient py:class 1 testclient/#$ -\n"
    )

    entries = objects_inv.parse(data).entries

    assert [entry.name for entry in entries] == ["starlette.testclient.TestClient"]


def test_parse_truncated_header():
    with pytest.raises(objects_inv.ObjectsInvError, match="Truncated"):
        objects_inv.parse(b"# Sphinx inventory version 2\n# Project: Starlette\n")


def test_parse_unrecognized_header():
    with pytest.raises(objects_inv.ObjectsInvError, match="Unrecognized"):
        objects_inv.parse(build("", header=b"not an inventory\n" + _HEADER))


def test_parse_unsupported_version():
    header = _HEADER.replace(b"version 2", b"version 1")

    with pytest.raises(objects_inv.ObjectsInvError, match="Unsupported"):
        objects_inv.parse(build("", header=header))


def test_parse_missing_project():
    header = _HEADER.replace(b"# Project: Starlette", b"# Nope: Starlette")

    with pytest.raises(objects_inv.ObjectsInvError, match="Project"):
        objects_inv.parse(build("", header=header))


def test_parse_uncompressed_body():
    header = _HEADER.replace(b"compressed using zlib.", b"not compressed.")

    with pytest.raises(objects_inv.ObjectsInvError, match="zlib compressed"):
        objects_inv.parse(build("", header=header))


def test_parse_corrupt_body():
    with pytest.raises(objects_inv.ObjectsInvError, match="decompress"):
        objects_inv.parse(_HEADER + b"not actually zlib")
