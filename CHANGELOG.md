# Changelog

## [Unreleased]

- Added `add-docs`, `update-docs` commands to `pyrefdev-indexer`.
- Added missing module symbols.
- Support [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
- Support [setuptools](https://setuptools.pypa.io/en/latest/).
- Support [botocore](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html).
- Support [charset-normalizer](https://charset-normalizer.readthedocs.io/en/latest/).
- Support [typing-extensions](https://typing-extensions.readthedocs.io/en/latest/).
- Support [packaging](https://packaging.pypa.io/en/stable/).
- Support [s3fs](https://s3fs.readthedocs.io/en/latest/).
- Support [six](https://six.readthedocs.io/).

## v2025.4

- Fix a bug in the crawler where relative paths aren't joined correctly.
- Support [pandas](https://pandas.pydata.org/docs/reference/index.html).
- Support [urllib3](https://urllib3.readthedocs.io/en/stable/reference/index.html).
- Support [requests](https://requests.readthedocs.io/en/latest/).
- Support [python-dateutil](https://dateutil.readthedocs.io/en/stable/).

## v2025.3

- Support [numpy](https://numpy.org/doc/stable/reference/index.html).

## v2025.2

- Added a new `pyrefdev-indexer` CLI to `crawl-docs` and `parse-docs`. The `mapping.py` is now reproducible and easily updatable when Python 3.14 is released.
- Update the mappings.

## v2025.1

Initial release.
