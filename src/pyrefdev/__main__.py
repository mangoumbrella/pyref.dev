import argparse
import webbrowser
import sys

from pyrefdev.mapping import MAPPING


def main():
    parser = argparse.ArgumentParser(
        prog="pyrefdev",
        description="pyref.dev is a fast, convenient way to access Python reference docs.",
    )
    parser.add_argument("symbol")
    ns = parser.parse_args()

    symbol = ns.symbol
    if not (url := MAPPING.get(symbol)):
        url = MAPPING.get(symbol.lower())
    if url:
        webbrowser.open_new_tab(url)
    else:
        print(f"{symbol} not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
