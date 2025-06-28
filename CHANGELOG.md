# Changelog

## [Unreleased]

- Added `add-docs`, `update-docs` commands to `pyrefdev-indexer`.

## v2025.4

- Fix a bug in the crawler where relative paths aren't joined correctly.
- Support [pandas](https://pandas.pydata.org/docs/reference/index.html)
- Support [urllib3](https://urllib3.readthedocs.io/en/stable/reference/index.html)
- Support [requests](https://requests.readthedocs.io/en/latest/)
- Support [python-dateutil](https://dateutil.readthedocs.io/en/stable/)

## v2025.3

- Support [numpy](https://numpy.org/doc/stable/reference/index.html).

## v2025.2

- Added a new `pyrefdev-indexer` CLI to `crawl-docs` and `parse-docs`. The `mapping.py` is now reproducible and easily updatable when Python 3.14 is released.
- Update the mappings.

## v2025.1

Initial release.
