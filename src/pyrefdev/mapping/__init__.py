"""Symbol lookup, served from a prebuilt SQLite index when one is available.

The per-package modules in this directory are the source of truth. Without an
index, lookups fall back to importing all of them.
"""

import dataclasses
import importlib
import os
import random
import sqlite3
import threading
from pathlib import Path
from urllib import parse

from pyrefdev.config import console, SUPPORTED_PACKAGES


INDEX_FILENAME = "index.sqlite"

# FTS5's trigram tokenizer indexes three-character windows, so it cannot match a
# needle shorter than that. Those searches fall back to a scan.
_MIN_TRIGRAM_LENGTH = 3

_LIKE_ESCAPE = "\\"


@dataclasses.dataclass(frozen=True, kw_only=True)
class PackageInfo:
    version: str
    mapping: dict[str, str]


@dataclasses.dataclass(frozen=True, kw_only=True)
class SearchResult:
    symbol: str
    url: str


def index_path() -> Path:
    if override := os.environ.get("PYREFDEV_INDEX"):
        return Path(override)
    return Path(__file__).parent / INDEX_FILENAME


def load_package_mapping(package: str) -> PackageInfo | None:
    """Read one package's mapping from its module, bypassing any index."""
    try:
        module = importlib.import_module(f"pyrefdev.mapping.{package}")
    except ImportError:
        return None
    return PackageInfo(
        version=getattr(module, "VERSION"), mapping=getattr(module, "MAPPING")
    )


def load_mapping(
    verify_duplicates: bool,
) -> tuple[dict[str, str], dict[str, PackageInfo]]:
    """Load every package's mapping into memory. Costs ~420MB; prefer the index."""
    mapping = {}
    packages = {}
    for package in SUPPORTED_PACKAGES:
        package_info = load_package_mapping(package)
        if package_info is None:
            console.warning(f"Missing mapping for {package}")
            continue
        if verify_duplicates:
            duplicates = set(mapping) & set(package_info.mapping)
            if duplicates:
                raise RuntimeError(
                    f"Found duplicated entries from {package}: {','.join(duplicates)}"
                )
        mapping.update(package_info.mapping)
        packages[package] = package_info
    return mapping, packages


def _display_symbol(key: str, url: str) -> str:
    """Prefer the URL fragment's spelling, which carries the real symbol casing."""
    fragment = parse.urlparse(url).fragment
    return fragment if fragment.lower() == key.lower() else key


class _SqliteBackend:
    """Answers queries from the prebuilt index, holding no symbols in memory."""

    name = "sqlite"

    def __init__(self, path: Path):
        self._path = path
        # sqlite3 connections are single-threaded, and Starlette may dispatch
        # across a threadpool, so each thread gets its own read-only handle.
        self._local = threading.local()

    @property
    def _connection(self) -> sqlite3.Connection:
        connection = getattr(self._local, "connection", None)
        if connection is None:
            connection = sqlite3.connect(
                f"file:{self._path}?mode=ro", uri=True, check_same_thread=False
            )
            self._local.connection = connection
        return connection

    def lookup(self, symbol: str) -> str | None:
        for candidate in (symbol, symbol.lower()):
            row = self._connection.execute(
                "SELECT url FROM symbol WHERE key = ?", (candidate,)
            ).fetchone()
            if row is not None:
                return row[0]
        return None

    def search(self, term: str, package: str) -> list[SearchResult]:
        if len(term) >= _MIN_TRIGRAM_LENGTH:
            sql = (
                "SELECT s.key, s.url FROM symbol_fts f "
                "JOIN symbol s ON s.id = f.rowid WHERE f.key MATCH ?"
            )
            # A bare double quote would terminate the FTS string literal early.
            params: list[str] = ['"' + term.replace('"', '""') + '"']
        else:
            escaped = term
            for character in (_LIKE_ESCAPE, "%", "_"):
                escaped = escaped.replace(character, _LIKE_ESCAPE + character)
            sql = (
                "SELECT s.key, s.url FROM symbol s "
                f"WHERE s.key LIKE ? ESCAPE '{_LIKE_ESCAPE}'"
            )
            params = [f"%{escaped}%"]
        if package:
            sql += " AND s.pypi = ?"
            params.append(package)
        return [
            SearchResult(symbol=_display_symbol(key, url), url=url)
            for key, url in self._connection.execute(sql, params)
        ]

    def random_url(self) -> str:
        package = self._connection.execute(
            "SELECT pypi FROM package ORDER BY RANDOM() LIMIT 1"
        ).fetchone()[0]
        return self._connection.execute(
            "SELECT url FROM symbol WHERE pypi = ? ORDER BY RANDOM() LIMIT 1",
            (package,),
        ).fetchone()[0]

    def symbol_count(self) -> int:
        return self._connection.execute(
            "SELECT COALESCE(SUM(num_symbols), 0) FROM package"
        ).fetchone()[0]


class _ModuleBackend:
    """Fallback for installs with no prebuilt index. Loads every mapping module."""

    name = "modules"

    def __init__(self):
        self._mapping, self._packages = load_mapping(verify_duplicates=False)

    def lookup(self, symbol: str) -> str | None:
        return self._mapping.get(symbol) or self._mapping.get(symbol.lower())

    def search(self, term: str, package: str) -> list[SearchResult]:
        if package:
            package_info = self._packages.get(package)
            mapping = package_info.mapping if package_info else {}
        else:
            mapping = self._mapping
        term_lower = term.lower()
        return [
            SearchResult(symbol=_display_symbol(key, url), url=url)
            for key, url in mapping.items()
            if term_lower in key.lower()
        ]

    def random_url(self) -> str:
        package = random.choice(list(self._packages))
        return random.choice(list(self._packages[package].mapping.values()))

    def symbol_count(self) -> int:
        return len(self._mapping)


_backend: _SqliteBackend | _ModuleBackend | None = None
_backend_lock = threading.Lock()


def backend() -> _SqliteBackend | _ModuleBackend:
    global _backend
    if _backend is None:
        with _backend_lock:
            if _backend is None:
                path = index_path()
                _backend = _SqliteBackend(path) if path.exists() else _ModuleBackend()
    return _backend


def lookup(symbol: str) -> str | None:
    """The documentation URL for a symbol, trying an exact then a lowercase match."""
    return backend().lookup(symbol)


def search(term: str, package: str = "") -> list[SearchResult]:
    """Every symbol containing `term`, case-insensitively, unranked."""
    return backend().search(term, package)


def random_url() -> str:
    """A random documentation URL, weighting each package equally."""
    return backend().random_url()


def symbol_count() -> int:
    return backend().symbol_count()
