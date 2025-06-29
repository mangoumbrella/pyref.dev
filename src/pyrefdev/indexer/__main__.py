import cyclopts

import pyrefdev
from pyrefdev.indexer.add_docs import add_docs
from pyrefdev.indexer.crawl_docs import crawl_docs
from pyrefdev.indexer.parse_docs import parse_docs
from pyrefdev.indexer.update_docs import update_docs
from pyrefdev.indexer.update_landing_page import update_landing_page
from pyrefdev.config import console


app = cyclopts.App(
    name="pyrefdev-indexer",
    help="The indexer for pyref.dev.",
    version=pyrefdev.__version__,
    console=console,
)
app.command(add_docs)
app.command(crawl_docs)
app.command(parse_docs)
app.command(update_docs)
app.command(update_landing_page)


if __name__ == "__main__":
    app()
