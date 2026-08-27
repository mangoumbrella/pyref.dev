# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

The project has several components:

1. **Web Server** (`src/pyrefdev/server.py`): FastAPI application that serves redirects based on symbol lookup. `templates/index.html` is the landing page of the server, `static/styles.css` contains CSS styles
2. **CLI Tool** (`src/pyrefdev/__main__.py`): Command-line interface that opens documentation in browser
3. **Indexer** (`src/pyrefdev/indexer/`): Tools for crawling, parsing, and managing documentation mappings
4. **Mapping System** (`src/pyrefdev/mapping/`): Individual Python files per package containing symbol-to-URL mappings

## Common Commands

### Development Setup
```bash
uv sync --all-extras --locked
```

### Testing
```bash
uv run pytest
```

### Run Web Server
```bash
# Build the symbol index first; without it the server falls back to importing
# every mapping module, which costs ~420MB of RSS instead of ~85MB.
pyrefdev-indexer build-index
uv run uvicorn pyrefdev.server:app --reload
```

`build-index` is a no-op (~0.2s) when the index already matches the mapping
files, so it is safe to run before every start. Pass `--force` to rebuild
regardless.

### Run CLI Tool
```bash
pyrefdev <symbol>
```

### Indexer Operations

Common workflow for adding a new package:
```bash
# Add a new package (crawls by default)
pyrefdev-indexer add-docs --package <package> --url <API reference doc root URL>

# Or add without crawling, then crawl separately
pyrefdev-indexer add-docs --package <package> --url <API reference doc root URL> --no-crawl
pyrefdev-indexer crawl-docs --package <package>

# Parse the crawled docs to generate mappings
pyrefdev-indexer parse-docs --package <package>

# Or combine crawl + parse in one step
pyrefdev-indexer update-docs --package <package>

# Update the landing page after adding packages
pyrefdev-indexer update-landing-page

# Rebuild the symbol index the server queries (do this last, after the
# mapping files are final). The deployed service also does this on restart.
pyrefdev-indexer build-index
```

Additional indexer commands:
```bash
# Crawl with retry options
pyrefdev-indexer crawl-docs --package <package> --upgrade --retry-failed-urls

# Parse with options
pyrefdev-indexer parse-docs --package <package> --in-place --reparse-all

# PyPI operations
pyrefdev-indexer crawl-pypi      # Crawl top 15000 PyPI packages
pyrefdev-indexer parse-pypi      # Parse PyPI data and add new packages to config
```

## Development Workflow

- **Testing**: Run pytest to ensure mappings work correctly

## Important Notes

- Do not add tests unless explictly asked to.
- When creating a new file with content, ensure the file has an extra new line at the end.
- Do NOT add redundant comments describe what the cod does. When needed, DO add comments that explains "why".
- Server deployment relies on nginx and systemd, and the config files are in `deploy/`.
- **Symbol index**: the server queries a SQLite index (`src/pyrefdev/mapping/index.sqlite`,
  gitignored) built by `pyrefdev-indexer build-index`. The per-package files in
  `src/pyrefdev/mapping/` remain the source of truth; the index is a derived artifact.
  Deploys need no extra step: `ExecStartPre` in `deploy/pyrefdev.service` rebuilds it when
  the mapping files have changed, keyed off their names, sizes, and mtimes.
- **CSS Cache Busting**: Whenever you modify `static/styles.css`, you must increment the `?v=` version parameter in all `templates/*.html` files to ensure browsers load the updated styles
