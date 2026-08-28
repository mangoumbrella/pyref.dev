import sqlite3

import pytest

from pyrefdev import mapping
from pyrefdev.indexer import build_index as build_index_module
from pyrefdev.indexer.build_index import build_index


# Terms chosen to hit both query paths and the escaping in each: below and
# above the trigram floor, LIKE wildcards, and an FTS string delimiter.
SEARCH_TERMS = [
    "Argument",
    "argument",
    "path",
    "_",
    "__",
    "at",
    "e",
    "",
    "%",
    "a%b",
    'a"b',
    "'",
    "\\",
    "C++",
    "nosuchsymbolanywhere",
]


def raw(backend, term, package=""):
    return [(r.symbol, r.url) for r in backend.search(term, package)]


@pytest.mark.parametrize("term", SEARCH_TERMS)
def test_search_matches_module_backend(sqlite_backend, module_backend, term):
    """Both backends must agree on results and on their order.

    The server ranks with a stable sort, so equal-ranked results keep the order
    the backend returned them in. Matching raw order is what keeps the ranked
    page identical.
    """
    assert raw(sqlite_backend, term) == raw(module_backend, term)


@pytest.mark.parametrize("package", ["click", "attrs", "", "nosuchpackage"])
def test_search_scoped_to_package(sqlite_backend, module_backend, package):
    assert raw(sqlite_backend, "a", package) == raw(module_backend, "a", package)


def test_search_package_scope_is_a_subset(sqlite_backend):
    scoped = raw(sqlite_backend, "a", "click")
    assert scoped
    assert set(scoped) < set(raw(sqlite_backend, "a"))


def test_lookup_matches_module_backend(sqlite_backend, module_backend):
    for key in module_backend._mapping:
        assert sqlite_backend.lookup(key) == module_backend.lookup(key)


@pytest.mark.parametrize(
    "symbol",
    ["click.Argument", "CLICK.ARGUMENT", "Click.Argument", "nosuchsymbol", ""],
)
def test_lookup_is_case_insensitive(sqlite_backend, module_backend, symbol):
    assert sqlite_backend.lookup(symbol) == module_backend.lookup(symbol)


def test_lookup_prefers_exact_case(sqlite_backend):
    """A lowercase key must not shadow an exact match on the same symbol."""
    assert sqlite_backend.lookup("click.Argument").endswith("#click.Argument")


def test_symbol_count_matches_module_backend(sqlite_backend, module_backend):
    assert sqlite_backend.symbol_count() == module_backend.symbol_count()


def test_random_url_comes_from_the_index(sqlite_backend, module_backend):
    urls = set(module_backend._mapping.values())
    assert {sqlite_backend.random_url() for _ in range(50)} <= urls


def test_backend_falls_back_without_an_index(tmp_path, monkeypatch):
    monkeypatch.setenv("PYREFDEV_INDEX", str(tmp_path / "absent.sqlite"))
    monkeypatch.setattr(mapping, "_backend", None)
    assert mapping.backend().name == "modules"


def test_backend_uses_an_existing_index(small_index, monkeypatch):
    monkeypatch.setenv("PYREFDEV_INDEX", str(small_index))
    monkeypatch.setattr(mapping, "_backend", None)
    assert mapping.backend().name == "sqlite"


def test_index_path_honours_the_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("PYREFDEV_INDEX", str(tmp_path / "custom.sqlite"))
    assert mapping.index_path() == tmp_path / "custom.sqlite"


def test_rebuild_is_skipped_when_fresh(rebuildable_index, small_packages, monkeypatch):
    monkeypatch.setattr(build_index_module, "SUPPORTED_PACKAGES", small_packages)
    before = rebuildable_index.stat().st_mtime_ns
    build_index(rebuildable_index)
    assert rebuildable_index.stat().st_mtime_ns == before


def test_force_rebuilds_a_fresh_index(rebuildable_index, small_packages, monkeypatch):
    monkeypatch.setattr(build_index_module, "SUPPORTED_PACKAGES", small_packages)
    before = rebuildable_index.stat().st_mtime_ns
    build_index(rebuildable_index, force=True)
    assert rebuildable_index.stat().st_mtime_ns != before
    assert mapping._SqliteBackend(rebuildable_index).lookup("click.Argument")


def test_fingerprint_tracks_mapping_files(small_packages, monkeypatch, tmp_path):
    """Editing a mapping file must invalidate an index built from it."""
    monkeypatch.setattr(build_index_module, "SUPPORTED_PACKAGES", small_packages)
    monkeypatch.setattr(mapping, "__file__", str(tmp_path / "__init__.py"))
    edited = tmp_path / "click.py"
    edited.write_text('MAPPING = {"a.B": "http://one"}\n')
    before = build_index_module._source_fingerprint()
    edited.write_text('MAPPING = {"a.B": "http://two", "c.D": "http://three"}\n')
    assert build_index_module._source_fingerprint() != before


def test_fingerprint_tracks_the_reader(small_packages, monkeypatch, tmp_path):
    """__init__.py reads the mapping modules, so it decides what gets indexed."""
    monkeypatch.setattr(build_index_module, "SUPPORTED_PACKAGES", small_packages)
    monkeypatch.setattr(mapping, "__file__", str(tmp_path / "__init__.py"))
    (tmp_path / "click.py").write_text('MAPPING = {"a.B": "http://one"}\n')
    init = tmp_path / "__init__.py"
    init.write_text("# reader\n")
    before = build_index_module._source_fingerprint()
    init.write_text("# reader, edited differently\n")
    assert build_index_module._source_fingerprint() != before


def test_fingerprint_ignores_unrelated_files(small_packages, monkeypatch, tmp_path):
    monkeypatch.setattr(build_index_module, "SUPPORTED_PACKAGES", small_packages)
    monkeypatch.setattr(mapping, "__file__", str(tmp_path / "__init__.py"))
    (tmp_path / "click.py").write_text('MAPPING = {"a.B": "http://one"}\n')
    before = build_index_module._source_fingerprint()
    (tmp_path / "notes.txt").write_text("not a mapping file\n")
    assert build_index_module._source_fingerprint() == before


def test_fingerprint_tracks_indexed_packages(small_packages, monkeypatch):
    monkeypatch.setattr(build_index_module, "SUPPORTED_PACKAGES", small_packages)
    before = build_index_module._source_fingerprint()
    fewer = {k: v for k, v in small_packages.items() if k != "click"}
    monkeypatch.setattr(build_index_module, "SUPPORTED_PACKAGES", fewer)
    assert build_index_module._source_fingerprint() != before


def test_fingerprint_of_a_missing_index(tmp_path):
    assert build_index_module._fingerprint_of(tmp_path / "absent.sqlite") is None


def test_fingerprint_of_a_corrupt_index(tmp_path):
    corrupt = tmp_path / "corrupt.sqlite"
    corrupt.write_bytes(b"not a database")
    assert build_index_module._fingerprint_of(corrupt) is None


def test_a_failed_build_leaves_the_index_intact(rebuildable_index, monkeypatch):
    """The rebuild goes to a temporary file, so a crash cannot corrupt the index."""
    before = rebuildable_index.read_bytes()

    def explode(package):
        raise RuntimeError("simulated failure")

    monkeypatch.setattr(mapping, "load_package_mapping", explode)
    with pytest.raises(RuntimeError):
        build_index(rebuildable_index, force=True)
    assert rebuildable_index.read_bytes() == before
    assert mapping._SqliteBackend(rebuildable_index).lookup("click.Argument")


def test_duplicate_symbols_are_reported(tmp_path):
    connection = sqlite3.connect(tmp_path / "dupes.sqlite")
    connection.executescript(build_index_module._SCHEMA)
    connection.executemany(
        "INSERT INTO symbol(key, url, pypi) VALUES(?, ?, ?)",
        [("a.B", "http://one", "alpha"), ("a.B", "http://two", "beta")],
    )
    with pytest.raises(SystemExit):
        build_index_module._report_duplicates(connection)


def test_the_index_has_no_duplicate_keys(small_index):
    connection = sqlite3.connect(small_index)
    duplicates = connection.execute(
        "SELECT COUNT(*) FROM (SELECT key FROM symbol GROUP BY key HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    assert duplicates == 0
