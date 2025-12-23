# pyref.dev

[pyref.dev](https://pyref.dev) is a fast, convenient way to access Python reference docs.

<p>
<a href="https://pypi.org/project/pyrefdev"><img alt="PyPI" src="https://img.shields.io/pypi/v/pyrefdev"></a>
<a href="https://pypi.org/project/pyrefdev"><img alt="Python veresions supported" src="https://img.shields.io/pypi/pyversions/pyrefdev"></a>
<a href="https://github.com/mangoumbrella/pyref.dev/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/pyrefdev.svg"></a>
</p>

It allows you to quickly jump to the official documentation for Python standard library modules and popular packages by using a simple URL pattern:

```
https://pyref.dev/<fully.qualified.symbol.name>
```

You can also search for symbols using:

```
https://pyref.dev/is?symbol=<SYMBOL>
```

And if you are feeling lucky, ask it to redirect to the first result:

```
https://pyref.dev/is?lucky=true&symbol=<SYMBOL>
```

Lastly, you can `pip install pyrefdev` and run the `pyrefdev` CLI tool.

## Examples

* [pyref.dev/json](https://pyref.dev/json)
* [pyref.dev/pathlib.Path](https://pyref.dev/pathlib.Path)
* [pyref.dev/datetime.datetime.strftime](https://pyref.dev/datetime.datetime.strftime)
* [pyref.dev/numpy.array](https://pyref.dev/numpy.array)

## Supported packages

See [pyref.dev](https://pyref.dev/#supported-packages) for the list of supported packages.

# Case sensitivity

For most of the cases, they are case-insensitive. However, for symbols like `typing.final` and `typing.Final`, you need to access them with the correct case.

## Server setup

To set up a new server:

```bash
> sudo apt update && sudo apt install nginx
> sudo rm /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
> curl -LsSf https://astral.sh/uv/install.sh | sh
> git clone https://github.com/mangoumbrella/pyref.dev
> cd pyref.dev
> uv venv --python 3.14
> uv sync --all-extras --locked
> sudo cp deploy/pyrefdev.service /etc/systemd/system/pyrefdev.service
> sudo cp deploy/pyrefdev.conf /etc/nginx/sites-available/pyrefdev
> sudo ln -sf /etc/nginx/sites-available/pyrefdev /etc/nginx/sites-enabled/pyrefdev
> systemctl start nginx.service
> systemctl start pyrefdev.service
```

To update to a new version:

```bash
git pull && git fetch --tags && uv pip install -e . && uv sync --all-extras --locked && systemctl restart pyrefdev.service
```

To upgrade uv venv's Python version:

```bash
uv venv --python 3.14
```

## Changelog

See [CHANGELOG.md](https://github.com/mangoumbrella/pyref.dev/blob/main/CHANGELOG.md).

## License

[pyref.dev](https://pyref.dev) is licensed under the terms of the Apache license. See [LICENSE](https://github.com/mangoumbrella/pyref.dev/blob/main/LICENSE) for more information.
