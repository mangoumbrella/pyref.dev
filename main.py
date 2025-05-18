import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/{symbol}")
async def redirects(symbol: str):
    if symbol.startswith("_"):
        raise HTTPException(status_code=404, detail="Documentation not found.")
    if symbol not in sys.stdlib_module_names:
        raise HTTPException(status_code=404, detail="Documentation not found.")
    return RedirectResponse(f"https://docs.python.org/3/library/{symbol}.html")
