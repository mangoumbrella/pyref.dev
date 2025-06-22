import cyclopts

import pyrefdev
from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.config import console


app = cyclopts.App(
    name="pyrefdev-indexer",
    help="The indexer for pyref.dev.",
    version=pyrefdev.__version__,
    console=console,
)
app.command(crawl_docs)


if __name__ == "__main__":
    app()
