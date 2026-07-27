"""Extract symbols from hand-written docs that only show import statements.

Some documentation sites are guides rather than generated API references: their
pages carry no per-symbol anchors, so crawling the HTML finds nothing to map.
The import statements in their code examples do name the documented symbols with
their real module paths, and the section headings supply the anchors to link to.
"""

import collections
import re
from urllib.parse import urlparse

import bs4


_IMPORT = re.compile(r"^[ \t]*from[ \t]+([\w.]+)[ \t]+import[ \t]+(.+)$", re.MULTILINE)
_NAME = re.compile(r"[A-Za-z_]\w*")
_HEADING = re.compile(r"^h[1-6]$")


class DocumentedImports:
    """Accumulates the imports and anchors of a package's doc pages."""

    def __init__(self, namespaces: list[str]) -> None:
        self._namespaces = namespaces
        self._imported_symbols: set[str] = set()
        # Anchor id -> the page URLs whose headings define it.
        self._anchors: dict[str, set[str]] = collections.defaultdict(set)
        # Last path component of a page URL -> that page URL.
        self._page_urls: dict[str, str] = {}

    def add_page(self, url: str, content: str) -> None:
        try:
            soup = bs4.BeautifulSoup(content, "html.parser")
        except bs4.ParserRejectedMarkup:
            return
        # Navigation, search and footer are full of ids and code snippets that
        # have nothing to do with the page's own documentation.
        article = soup.find("article")
        if not isinstance(article, bs4.Tag):
            article = soup

        for block in article.find_all(["pre", "code"]):
            self._add_imports(block.get_text())
        for heading in article.find_all(_HEADING):
            anchor = heading.get("id")
            # Themes use leading underscores for their own layout anchors.
            if isinstance(anchor, str) and anchor and not anchor.startswith("_"):
                self._anchors[anchor].add(url)
        if slug := _page_slug(url):
            self._page_urls.setdefault(slug, url)

    def symbols(self) -> dict[str, str]:
        symbols = {}
        for symbol in sorted(self._imported_symbols):
            module, _, name = symbol.rpartition(".")
            if url := self._resolve(symbol, name, self._module_page_url(module)):
                symbols[symbol] = url
        return symbols

    def _add_imports(self, text: str) -> None:
        for module, names in _IMPORT.findall(text):
            if not self._is_in_namespace(module):
                continue
            for part in names.split("#")[0].split(","):
                # "from x import y as z" documents y, not the local alias z.
                if match := _NAME.search(part.split(" as ")[0]):
                    self._imported_symbols.add(f"{module}.{match.group()}")

    def _is_in_namespace(self, module: str) -> bool:
        return any(module.startswith(ns + ".") for ns in self._namespaces)

    def _module_page_url(self, module: str) -> str | None:
        """The page named after the module, or the closest parent package."""
        for component in reversed(module.split(".")):
            if url := self._page_urls.get(component):
                return url
        return None

    def _resolve(self, symbol: str, name: str, module_url: str | None) -> str | None:
        for anchor in (symbol, name.lower()):
            pages = self._anchors.get(anchor)
            if not pages:
                continue
            if module_url in pages:
                return f"{module_url}#{anchor}"
            # Anchors elsewhere are only trustworthy when the module has no page
            # of its own and nothing else claims the same anchor: a heading
            # repeated across pages (e.g. "Headers") is prose about the symbol
            # rather than the place where it is documented.
            if module_url is None and len(pages) == 1:
                return f"{next(iter(pages))}#{anchor}"
        return module_url


def _page_slug(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    return path.rsplit("/", maxsplit=1)[-1].removesuffix(".html")
