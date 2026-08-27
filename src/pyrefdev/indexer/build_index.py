import hashlib
import sqlite3
import sys
from pathlib import Path

from pyrefdev import mapping
from pyrefdev.config import console, SUPPORTED_PACKAGES


# Bump to invalidate existing indexes when the schema changes.
_SCHEMA_VERSION = 1


_SCHEMA = """
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE package(
    pypi TEXT PRIMARY KEY,
    version TEXT NOT NULL,
    num_symbols INTEGER NOT NULL
);
CREATE TABLE symbol(
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    url TEXT NOT NULL,
    pypi TEXT NOT NULL
);
"""


def build_index(output: Path | None = None, force: bool = False) -> None:
    """Build the SQLite symbol index that the server queries.

    Rebuilding is skipped when the existing index already matches the mapping
    files, so this is cheap enough to run before every server start.
    """
    if output is None:
        output = mapping.index_path()
    fingerprint = _source_fingerprint()
    if not force and _fingerprint_of(output) == fingerprint:
        console.print(f"{output} is up to date.")
        return
    partial = output.with_suffix(output.suffix + ".partial")
    partial.unlink(missing_ok=True)

    connection = sqlite3.connect(partial)
    # The file is rebuilt from scratch on every run, so durability buys nothing
    # and costs an fsync per transaction.
    connection.execute("PRAGMA journal_mode = OFF")
    connection.execute("PRAGMA synchronous = OFF")
    connection.executescript(_SCHEMA)

    total = 0
    with connection:
        for package in SUPPORTED_PACKAGES:
            package_info = mapping.load_package_mapping(package)
            if package_info is None:
                console.warning(f"Missing mapping for {package}")
                continue
            connection.executemany(
                "INSERT INTO symbol(key, url, pypi) VALUES(?, ?, ?)",
                ((k, u, package) for k, u in package_info.mapping.items()),
            )
            connection.execute(
                "INSERT INTO package(pypi, version, num_symbols) VALUES(?, ?, ?)",
                (package, package_info.version, len(package_info.mapping)),
            )
            total += len(package_info.mapping)
            _unload(package)

    console.print(f"Indexed {total:,} symbols; building indexes...")
    # Indexes are built after the bulk insert: maintaining them per-row would
    # dominate the build.
    try:
        connection.execute("CREATE UNIQUE INDEX symbol_key ON symbol(key)")
    except sqlite3.IntegrityError:
        _report_duplicates(connection)
    connection.execute("CREATE INDEX symbol_pypi ON symbol(pypi)")
    connection.executescript(
        """
        CREATE VIRTUAL TABLE symbol_fts USING fts5(
            key, content='symbol', content_rowid='id', tokenize='trigram'
        );
        INSERT INTO symbol_fts(rowid, key) SELECT id, key FROM symbol;
        """
    )
    connection.execute(
        "INSERT INTO meta(key, value) VALUES('fingerprint', ?)", (fingerprint,)
    )
    connection.commit()
    connection.execute("PRAGMA optimize")
    connection.close()

    partial.replace(output)
    size_mb = output.stat().st_size / 1048576
    console.print(f"Wrote {output} ({size_mb:.0f}MB, {total:,} symbols).")


def _source_fingerprint() -> str:
    """Identify the inputs an index was built from.

    SUPPORTED_PACKAGES is included because un-indexing a package must
    invalidate the index even though its mapping file stays on disk. Files are
    compared by size and mtime, not content, to keep this fast enough to run
    before every start.
    """
    digest = hashlib.sha256(str(_SCHEMA_VERSION).encode())
    digest.update(",".join(sorted(SUPPORTED_PACKAGES)).encode())
    sources = sorted(Path(mapping.__file__).parent.glob("*.py")) + [Path(__file__)]
    for path in sources:
        stat = path.stat()
        digest.update(f"{path.name}:{stat.st_size}:{stat.st_mtime_ns}".encode())
    return digest.hexdigest()


def _fingerprint_of(output: Path) -> str | None:
    """The fingerprint recorded in an existing index, if it can be read at all."""
    if not output.exists():
        return None
    try:
        connection = sqlite3.connect(f"file:{output}?mode=ro", uri=True)
    except sqlite3.Error:
        return None
    try:
        row = connection.execute(
            "SELECT value FROM meta WHERE key = 'fingerprint'"
        ).fetchone()
    except sqlite3.Error:
        # Predates the meta table, or the file is truncated or corrupt.
        return None
    finally:
        connection.close()
    return row[0] if row else None


def _report_duplicates(connection: sqlite3.Connection) -> None:
    """Name the packages that claim the same symbol, then abort.

    A collision needs resolving in config.py via `exclude_symbols`.
    """
    rows = connection.execute(
        """
        SELECT key, GROUP_CONCAT(pypi, ', ')
        FROM symbol GROUP BY key HAVING COUNT(*) > 1 LIMIT 10
        """
    ).fetchall()
    details = "\n".join(f"  {key}: claimed by {pypis}" for key, pypis in rows)
    console.fatal(f"Duplicated symbols across packages:\n{details}")


def _unload(package: str) -> None:
    """Drop a mapping module once indexed, so the build holds one at a time.

    Importing a submodule also binds it on its parent package, so evicting it
    from sys.modules alone would not release the mapping.
    """
    sys.modules.pop(f"pyrefdev.mapping.{package}", None)
    try:
        delattr(mapping, package)
    except AttributeError:
        pass
