from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse, PlainTextResponse

from .mapping import MAPPING


app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/{symbol}")
async def redirects(symbol: str):
    if url := MAPPING.get(symbol):
        return RedirectResponse(url)
    if url := MAPPING.get(symbol.lower()):
        return RedirectResponse(url)
    return PlainTextResponse(content=f"{symbol} not found", status_code=404)
