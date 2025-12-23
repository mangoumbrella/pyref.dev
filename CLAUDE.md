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
uv run uvicorn pyrefdev.server:app --reload
```

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
- **CSS Cache Busting**: Whenever you modify `static/styles.css`, you must increment the `?v=` version parameter in all `templates/*.html` files to ensure browsers load the updated styles
