from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import importlib.metadata

from pyrefdev.mapping import MAPPING


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    try:
        version = importlib.metadata.version("pyrefdev")
        version = version.split("+")[0]  # Strip the git hash
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"

    return templates.TemplateResponse(
        "index.html", {"request": request, "version": version}
    )


@app.get("/is")
async def search_symbols(request: Request, symbol: str = ""):
    if not symbol:
        return templates.TemplateResponse(
            "search.html", {"request": request, "symbol": "", "results": []}
        )

    # Search by substring for now.
    results = []
    symbol_lower = symbol.lower()
    for key in MAPPING.keys():
        if symbol_lower in key.lower():
            results.append({"symbol": key, "url": MAPPING[key]})

    # Sort results: exact match first, then by length.
    results.sort(
        key=lambda x: (
            x["symbol"].lower() != symbol_lower,
            len(x["symbol"]),
            x["symbol"],
        )
    )

    return templates.TemplateResponse(
        "search.html", {"request": request, "symbol": symbol, "results": results}
    )


@app.get("/{symbol}")
async def redirects(symbol: str):
    if url := MAPPING.get(symbol):
        return RedirectResponse(url)
    if url := MAPPING.get(symbol.lower()):
        return RedirectResponse(url)
    return PlainTextResponse(content=f"{symbol} not found", status_code=404)
