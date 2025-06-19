import cyclopts

import pyrefdev


app = cyclopts.App(
    name="pyref.dev indexer",
    help="The indexer for pyref.dev.",
    version=pyrefdev.__version__,
)


if __name__ == "__main__":
    app()
