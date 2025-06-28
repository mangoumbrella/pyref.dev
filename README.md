# pyref.dev

[pyref.dev](https://pyref.dev) is a fast, convenient way to access Python reference docs.

<p>
<a href="https://pypi.org/project/pyrefdev"><img alt="PyPI" src="https://img.shields.io/pypi/v/pyrefdev"></a>
<a href="https://pypi.org/project/pyrefdev"><img alt="Python veresions supported" src="https://img.shields.io/pypi/pyversions/pyrefdev"></a>
<a href="https://github.com/mangoumbrella/pyref.dev/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/pyrefdev.svg"></a>
</p>

It allows you to quickly jump to the official documentation for any Python standard library module, class, or function by using a simple URL pattern:

```
https://pyref.dev/<fully.qualified.symbol.name>
```

Alternatively, you could also `pip install pyrefdev` and run the `pyrefdev` CLI tool.

## Examples

* https://pyref.dev/json
* https://pyref.dev/pathlib.Path
* https://pyref.dev/datetime.datetime.strftime

For now, the symbols are case-insensitive.

## Server Setup

To set up a new server:

```bash
> git clone https://github.com/mangoumbrella/pyref.dev
> cd pyref.dev
> sudo cp pyrefdev.service /etc/systemd/system/pyrefdev.service
> systemctl start pyrefdev.service
```

To update to a new version:

```bash
> cd pyref.dev
> git pull
> uv sync --all-extras
> systemctl restart pyrefdev.service
```

## Changelog

See [CHANGELOG.md](https://github.com/mangoumbrella/pyref.dev/blob/main/CHANGELOG.md).

## License

[pyref.dev](https://pyref.dev) is licensed under the terms of the Apache license. See [LICENSE](https://github.com/mangoumbrella/pyref.dev/blob/main/LICENSE) for more information.
