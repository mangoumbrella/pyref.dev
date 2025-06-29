# Changelog

## [Unreleased]

- Added `add-docs`, `update-docs`, and `update-landing-page` commands to `pyrefdev-indexer`.
- Added missing module symbols.
- Support [attrs]("https://www.attrs.org/en/stable/").
- Support [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
- Support [botocore](https://botocore.amazonaws.com/v1/documentation/api/latest/index.html).
- Support [charset-normalizer](https://charset-normalizer.readthedocs.io/en/latest/).
- Support [cryptography](https://cryptography.io/en/latest/).
- Support [fsspec](https://filesystem-spec.readthedocs.io/en/latest/").
- Support [google-api-core](https://googleapis.dev/python/google-api-core/latest/").
- Support [packaging](https://packaging.pypa.io/en/stable/).
- Support [protobuf](https://googleapis.dev/python/protobuf/latest/).
- Support [pydantic-core](https://docs.pydantic.dev/latest/").
- Support [pydantic](https://docs.pydantic.dev/latest/").
- Support [s3fs](https://s3fs.readthedocs.io/en/latest/).
- Support [setuptools](https://setuptools.pypa.io/en/latest/).
- Support [six](https://six.readthedocs.io/).
- Support [typing-extensions](https://typing-extensions.readthedocs.io/en/latest/).

## v2025.4

- Fix a bug in the crawler where relative paths aren't joined correctly.
- Support [pandas](https://pandas.pydata.org/docs/reference/index.html).
- Support [python-dateutil](https://dateutil.readthedocs.io/en/stable/).
- Support [requests](https://requests.readthedocs.io/en/latest/).
- Support [urllib3](https://urllib3.readthedocs.io/en/stable/reference/index.html).

## v2025.3

- Support [numpy](https://numpy.org/doc/stable/reference/index.html).

## v2025.2

- Added a new `pyrefdev-indexer` CLI to `crawl-docs` and `parse-docs`. The `mapping.py` is now reproducible and easily updatable when Python 3.14 is released.
- Update the mappings.

## v2025.1

Initial release.
