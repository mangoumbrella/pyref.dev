import random
import sys

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import importlib.metadata
from urllib import parse

from pyrefdev.config import SUPPORTED_PACKAGES
from pyrefdev.mapping import MAPPING, PACKAGE_INFO_MAPPING


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

    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    packages = list(SUPPORTED_PACKAGES)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "version": version,
            "python_version": python_version,
            "packages": packages,
        },
    )


@app.get("/is")
async def search_symbols(
    request: Request, symbol: str = "", lucky: bool = False, package: str = ""
):
    packages = list(SUPPORTED_PACKAGES)

    if not symbol:
        if lucky:
            return RedirectResponse(_pick_random_url())
        else:
            package_url = (
                SUPPORTED_PACKAGES[package].index_url
                if package and package in SUPPORTED_PACKAGES
                else None
            )
            return templates.TemplateResponse(
                "search.html",
                {
                    "request": request,
                    "symbol": "",
                    "results": [],
                    "packages": packages,
                    "selected_package": package,
                    "package_url": package_url,
                },
            )

    # Determine which mapping to search
    if package:
        if package in PACKAGE_INFO_MAPPING:
            search_mapping = PACKAGE_INFO_MAPPING[package].mapping
        else:
            search_mapping = {}
    else:
        search_mapping = MAPPING

    # Search by substring for now.
    results = []
    symbol_lower = symbol.lower()
    for key in search_mapping.keys():
        if symbol_lower in key.lower():
            fragment = parse.urlparse(search_mapping[key]).fragment
            if fragment.lower() == key.lower():
                candidate = fragment
            else:
                candidate = key
            results.append({"symbol": candidate, "url": search_mapping[key]})

    def ranking_key(result):
        symbol_path = result["symbol"]
        components = symbol_path.split(".")
        num_components = len(components)

        if symbol_path.lower() == symbol_lower:
            # Prioritize exact case matches over case-insensitive matches (only if search term has uppercase)
            case_match_priority = (
                0 if (symbol != symbol_lower and symbol_path == symbol) else 1
            )
            return (
                0,
                0,
                case_match_priority,
                num_components,
                len(symbol_path),
                symbol_path,
            )

        # Check for exact component matches (case-insensitive)
        exact_component_matches = []
        exact_case_component_matches = []
        for i, component in enumerate(components):
            if component.lower() == symbol_lower:
                # Position from right (0 = rightmost, higher = more left)
                position_from_right = len(components) - 1 - i
                exact_component_matches.append(position_from_right)

                # Check if it's also an exact case match (only if search term has uppercase)
                if symbol != symbol_lower and component == symbol:
                    exact_case_component_matches.append(position_from_right)

        if exact_case_component_matches:
            # Prioritize rightmost position, then exact case matches
            best_position = min(exact_case_component_matches)
            return (1, best_position, 0, num_components, len(symbol_path), symbol_path)
        elif exact_component_matches:
            # Case-insensitive exact matches
            best_position = min(exact_component_matches)
            return (1, best_position, 1, num_components, len(symbol_path), symbol_path)

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

    # If lucky=true and we have results, redirect to the first (best) result
    if lucky and results:
        return RedirectResponse(results[0]["url"])

    package_url = (
        SUPPORTED_PACKAGES[package].index_url
        if package and package in SUPPORTED_PACKAGES
        else None
    )
    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "symbol": symbol,
            "results": results,
            "packages": packages,
            "selected_package": package,
            "package_url": package_url,
        },
    )


def _pick_random_url() -> str:
    package = random.choice(list(PACKAGE_INFO_MAPPING))
    return random.choice(list(PACKAGE_INFO_MAPPING[package].mapping.values()))


@app.get("/{symbol}")
async def redirects(symbol: str, lucky: bool = False):
    if url := MAPPING.get(symbol):
        return RedirectResponse(url)
    if url := MAPPING.get(symbol.lower()):
        return RedirectResponse(url)

    if lucky:
        return RedirectResponse(f"/is?symbol={symbol}&lucky=true")
    else:
        return RedirectResponse(f"/is?symbol={symbol}")
