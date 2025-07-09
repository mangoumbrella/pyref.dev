# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

The project has several components:

1. **Web Server** (`src/pyrefdev/server.py`): FastAPI application that serves redirects based on symbol lookup. `index.html` is the landing page of the server
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
```bash
pyrefdev-indexer add-docs --docs-directory api-docs --package <package> --url <API reference doc root URL>
pyrefdev-indexer crawl-docs --docs-directory api-docs --package <package>
pyrefdev-indexer parse-docs --docs-directory api-docs --package <package>
pyrefdev-indexer update-docs --docs-directory api-docs --package <package>
pyrefdev-indexer update-landing-page
```

## Development Workflow

- **Testing**: Run pytest to ensure mappings work correctly

## Important Notes

- Server deployment uses systemd and is configured in `pyrefdev.service`
