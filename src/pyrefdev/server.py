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

    def ranking_key(result):
        symbol_path = result["symbol"]
        components = symbol_path.split(".")
        num_components = len(components)

        if symbol_path.lower() == symbol_lower:
            return (0, 0, 0, num_components, len(symbol_path), symbol_path)

        # Check for exact component matches
        exact_component_matches = []
        for i, component in enumerate(components):
            if component.lower() == symbol_lower:
                # Position from right (0 = rightmost, higher = more left)
                position_from_right = len(components) - 1 - i
                exact_component_matches.append(position_from_right)

        if exact_component_matches:
            # Prioritize rightmost exact matches (smaller position_from_right)
            best_position = min(exact_component_matches)
            return (1, best_position, 0, num_components, len(symbol_path), symbol_path)

        # Check for component substring matches
        component_substring_matches = []
        for i, component in enumerate(components):
            if symbol_lower in component.lower():
                position_from_right = len(components) - 1 - i
                component_substring_matches.append(position_from_right)

        if component_substring_matches:
            best_position = min(component_substring_matches)
            return (2, best_position, 0, num_components, len(symbol_path), symbol_path)

        # Fallback to general substring match
        return (3, 0, 0, num_components, len(symbol_path), symbol_path)

    results.sort(key=ranking_key)

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
