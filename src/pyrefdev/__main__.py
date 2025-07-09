import webbrowser
import sys
from typing import Annotated

import cyclopts
from cyclopts import Parameter

import pyrefdev
from pyrefdev.mapping import MAPPING


app = cyclopts.App("pyrefdev", help=pyrefdev.__doc__)


@app.default
def main(
    symbol: str,
    /,
    *,
    should_print: Annotated[
        bool,
        Parameter(
            name=["--print", "-p"],
            negative="--no-print",
            help="When true, print the API reference URL instead of opening it in the browser.",
        ),
    ] = False,
):
    if not (url := MAPPING.get(symbol)):
        url = MAPPING.get(symbol.lower())
    if url:
        if should_print:
            print(url)
        else:
            webbrowser.open_new_tab(url)
    else:
        print(f"{symbol} not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    app()
