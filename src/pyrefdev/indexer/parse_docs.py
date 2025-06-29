import builtins
from collections import defaultdict
from concurrent import futures
import difflib
import itertools
import multiprocessing
from pathlib import Path
import re
import sys
import threading
from urllib import parse

import bs4
from rich.progress import Progress

from pyrefdev import mapping
from pyrefdev.config import console, get_packages, Package
from pyrefdev.indexer.schema import CrawlState


_STDLIB_MODULES_NAMES = frozenset({*sys.stdlib_module_names, "test"})
_MODULE_FRAGMENT_PREFIX = "module-"


class ProgressExecutor(futures.ThreadPoolExecutor):
    def __init__(
        self,
        description: str,
        *,
        progress: Progress,
        total: int,
        transient: bool = False,
        max_workers=None,
        thread_name_prefix="",
        initializer=None,
        initargs=(),
    ) -> None:
        super().__init__(
            max_workers=max_workers,
            thread_name_prefix=thread_name_prefix,
            initializer=initializer,
            initargs=initargs,
        )
        self.progress = progress
        self._transient = transient
        self._task = self.progress.add_task(description=description, total=total)
        self._exit_stack = None

    def submit(self, fn, /, *args, **kwargs):
        def fn_wrapper(*fn_args, **fn_kwargs):
            try:
                return fn(*fn_args, **fn_kwargs)
            finally:
                self.progress.advance(self._task)

        return super().submit(fn_wrapper, *args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = super().__exit__(exc_type, exc_val, exc_tb)
        if self._transient:
            self.progress.update(self._task, visible=False)
        return result


def parse_docs(
    *,
    package: str | None = None,
    docs_directory: Path,
    in_place: bool = False,
    num_parallel_packages: int = multiprocessing.cpu_count(),
    num_threads_per_package: int = multiprocessing.cpu_count(),
) -> None:
    if sys.version_info[:2] != (3, 13):
        console.fatal("pyrefdev-indexer parse_docs must be run on Python 3.13.")

    packages = get_packages(package)
    with (
        Progress(console=console) as progress,
        ProgressExecutor(
            f"Parsing {len(packages)} packages",
            progress=progress,
            total=len(packages),
            max_workers=num_parallel_packages,
        ) as executor,
    ):
        fs = [
            executor.submit(
                _parse_package,
                executor.progress,
                pkg,
                docs_directory / pkg.pypi,
                in_place=in_place,
                num_threads_per_package=num_threads_per_package,
            )
            for pkg in packages
        ]
        for f in fs:
            f.result()


def _parse_package(
    progress: Progress,
    package: Package,
    package_docs: Path,
    *,
    in_place: bool,
    num_threads_per_package: int,
) -> None:
    crawl_state_file = package_docs.parent / f"{package.pypi}.json"
    crawl_state = CrawlState.loads(crawl_state_file.read_text())
    file_and_urls: list[tuple[str, str]] = list(crawl_state.file_to_urls.items())
    if package.is_cpython():
        symbol_to_urls: dict[str, str] = _SPECIAL_SYMBOLS.copy()
    else:
        symbol_to_urls: dict[str, str] = {
            ns: package.index_url for ns in package.namespaces
        }
    parser = _Parser(package)
    lock = threading.RLock()

    def parse(file, url):
        if package.is_cpython:
            maybe_module = url.removeprefix(
                "https://docs.python.org/3/library/"
            ).removesuffix(".html")
            maybe_module_prefix = maybe_module.split(".")[0]
            if maybe_module_prefix in _STDLIB_MODULES_NAMES:
                symbol_to_urls[maybe_module] = url
        symbols = parser.parse_symbols((package_docs / file).read_text())
        module_count = sum(
            1 if fragment.startswith(_MODULE_FRAGMENT_PREFIX) else 0
            for fragment in symbols.values()
        )
        for symbol, fragment in symbols.items():
            with lock:
                if symbol not in symbol_to_urls:
                    if (
                        fragment.startswith(_MODULE_FRAGMENT_PREFIX)
                        and module_count == 1
                    ):
                        # This page contains a single module, let's redirect to this page without the anchor.
                        symbol_to_urls[symbol] = f"{url}"
                    else:
                        symbol_to_urls[symbol] = f"{url}#{fragment}"

    with ProgressExecutor(
        f"Parsing {len(file_and_urls)} files for {package_docs}",
        progress=progress,
        total=len(file_and_urls),
        transient=True,
        max_workers=num_threads_per_package,
    ) as executor:
        fs = [executor.submit(parse, file, url) for file, url in file_and_urls]
        for f in fs:
            f.result()

    console.print(f"Found {len(symbol_to_urls)} symbols in {package.pypi}")
    _heuristically_fillin_modules(package, symbol_to_urls)
    lines = _create_symbols_map(symbol_to_urls)
    mapping_file = Path(mapping.__file__).parent / f"{package.pypi}.py"
    if in_place:
        mapping_file.write_text("\n".join(itertools.chain(lines, [""])))
    else:
        if mapping_file.exists():
            before = mapping_file.read_text().splitlines(keepends=True)
        else:
            before = []
        diffs = difflib.unified_diff(
            before, [line + "\n" for line in lines], fromfile="before", tofile="after"
        )
        if diffs:
            console.print("".join(diffs))


def _heuristically_fillin_modules(
    package: Package, symbol_to_urls: dict[str, str]
) -> None:
    extra_module_to_urls: dict[str, str] = {}
    for symbol in symbol_to_urls:
        if symbol in package.namespaces:
            continue
        namespaces = {ns for ns in package.namespaces if symbol.startswith(ns + ".")}
        assert len(namespaces) == 1, f"{symbol=} unexpectedly matches {namespaces=}"
        namespace = next(iter(namespaces))

        module = symbol
        while module != namespace:
            module = module.rsplit(".", maxsplit=1)[0]
            assert module
            if module in symbol_to_urls or module in extra_module_to_urls:
                break
            urls = {
                _remove_fragment(url)
                for s, url in symbol_to_urls.items()
                if s.startswith(module + ".")
            }
            if len(urls) == 1:
                extra_module_to_urls[module] = next(iter(urls))
    symbol_to_urls.update(extra_module_to_urls)


def _remove_fragment(url: str) -> str:
    return parse.urlunparse(parse.urlparse(url)._replace(fragment=""))


def _create_symbols_map(symbol_to_urls: dict[str, str]) -> list[str]:
    lowercase_symbols = defaultdict(list)
    for symbol in symbol_to_urls:
        lowercase_symbols[symbol.lower()].append(symbol)

    lines = [
        "# fmt: off",
        "",
        "MAPPING = {",
    ]
    previous_symbol = None
    extra_lowercase_symbols = set()
    for symbol, url in sorted(
        symbol_to_urls.items(), key=lambda t: (t[0].lower(), t[1])
    ):
        lower = symbol.lower()
        key = symbol if len(lowercase_symbols[lower]) > 1 else lower
        lines.append(f'    "{key}": "{url}",')
        if (
            previous_symbol is not None
            and (previous_lower_symbol := previous_symbol.lower())
            and len(lowercase_symbols[previous_lower_symbol]) > 1
            and previous_lower_symbol not in symbol_to_urls
            and previous_lower_symbol not in extra_lowercase_symbols
        ):
            # Ensure the lower case key is also available.
            lines.append(f'    "{previous_lower_symbol}": "{url}",')
            extra_lowercase_symbols.add(previous_lower_symbol)
        previous_symbol = symbol
    lines.append("}")
    return lines


class _Parser:
    def __init__(self, package: Package) -> None:
        self._package = package

    def parse_symbols(self, content: str) -> dict[str, str]:
        try:
            soup = bs4.BeautifulSoup(content, "html.parser")
        except bs4.ParserRejectedMarkup:
            return {}
        symbols = {}
        for element in soup.find_all(id=True):
            fragment = element["id"]
            symbol = fragment.removeprefix(_MODULE_FRAGMENT_PREFIX)
            if self._is_symbol(symbol):
                symbols[symbol] = fragment
        return symbols

    def _is_symbol(self, symbol: str) -> bool:
        if not re.match(
            r"^([a-zA-Z_][a-zA-Z_0-9]*)(\.[a-zA-Z_][a-zA-Z_0-9]*)*$", symbol
        ):
            return False
        if self._package.is_cpython():
            prefix = symbol.split(".")[0]
            if prefix in _STDLIB_MODULES_NAMES:
                return True
            if prefix in dir(builtins):
                return True
            return False
        else:
            for ns in self._package.namespaces:
                if symbol.startswith(ns + "."):
                    return True
            return False


_SPECIAL_SYMBOLS = {
    "__abs__": "https://docs.python.org/3/reference/datamodel.html#object.__abs__",
    "__add__": "https://docs.python.org/3/reference/datamodel.html#object.__add__",
    "__aenter__": "https://docs.python.org/3/reference/datamodel.html#object.__aenter__",
    "__aexit__": "https://docs.python.org/3/reference/datamodel.html#object.__aexit__",
    "__aiter__": "https://docs.python.org/3/reference/datamodel.html#object.__aiter__",
    "__and__": "https://docs.python.org/3/reference/datamodel.html#object.__and__",
    "__anext__": "https://docs.python.org/3/reference/datamodel.html#object.__anext__",
    "__annotations__": "https://docs.python.org/3/reference/datamodel.html#type.__annotations__",
    "__await__": "https://docs.python.org/3/reference/datamodel.html#object.__await__",
    "__bases__": "https://docs.python.org/3/reference/datamodel.html#type.__bases__",
    "__bool__": "https://docs.python.org/3/reference/datamodel.html#object.__bool__",
    "__buffer__": "https://docs.python.org/3/reference/datamodel.html#object.__buffer__",
    "__bytes__": "https://docs.python.org/3/reference/datamodel.html#object.__bytes__",
    "__call__": "https://docs.python.org/3/reference/datamodel.html#object.__call__",
    "__ceil__": "https://docs.python.org/3/reference/datamodel.html#object.__ceil__",
    "__class__": "https://docs.python.org/3/reference/datamodel.html#object.__class__",
    "__class_getitem__": "https://docs.python.org/3/reference/datamodel.html#object.__class_getitem__",
    "__complex__": "https://docs.python.org/3/reference/datamodel.html#object.__complex__",
    "__contains__": "https://docs.python.org/3/reference/datamodel.html#object.__contains__",
    "__copy__": "https://docs.python.org/3/library/copy.html#object.__copy__",
    "__deepcopy__": "https://docs.python.org/3/library/copy.html#object.__deepcopy__",
    "__del__": "https://docs.python.org/3/reference/datamodel.html#object.__del__",
    "__delattr__": "https://docs.python.org/3/reference/datamodel.html#object.__delattr__",
    "__delete__": "https://docs.python.org/3/reference/datamodel.html#object.__delete__",
    "__delitem__": "https://docs.python.org/3/reference/datamodel.html#object.__delitem__",
    "__dict__": "https://docs.python.org/3/reference/datamodel.html#object.__dict__",
    "__dir__": "https://docs.python.org/3/reference/datamodel.html#object.__dir__",
    "__divmod__": "https://docs.python.org/3/reference/datamodel.html#object.__divmod__",
    "__doc__": "https://docs.python.org/3/reference/datamodel.html#type.__doc__",
    "__enter__": "https://docs.python.org/3/reference/datamodel.html#object.__enter__",
    "__eq__": "https://docs.python.org/3/reference/datamodel.html#object.__eq__",
    "__exit__": "https://docs.python.org/3/reference/datamodel.html#object.__exit__",
    "__firstlineno__": "https://docs.python.org/3/reference/datamodel.html#type.__firstlineno__",
    "__float__": "https://docs.python.org/3/reference/datamodel.html#object.__float__",
    "__floor__": "https://docs.python.org/3/reference/datamodel.html#object.__floor__",
    "__floordiv__": "https://docs.python.org/3/reference/datamodel.html#object.__floordiv__",
    "__format__": "https://docs.python.org/3/reference/datamodel.html#object.__format__",
    "__future__.absolute_import": "https://docs.python.org/3/library/__future__.html",
    "__future__.annotations": "https://docs.python.org/3/library/__future__.html",
    "__future__.division": "https://docs.python.org/3/library/__future__.html",
    "__future__.generator_stop": "https://docs.python.org/3/library/__future__.html",
    "__future__.generators": "https://docs.python.org/3/library/__future__.html",
    "__future__.nested_scopes": "https://docs.python.org/3/library/__future__.html",
    "__future__.print_function": "https://docs.python.org/3/library/__future__.html",
    "__future__.unicode_literals": "https://docs.python.org/3/library/__future__.html",
    "__future__.with_statement": "https://docs.python.org/3/library/__future__.html",
    "__ge__": "https://docs.python.org/3/reference/datamodel.html#object.__ge__",
    "__get__": "https://docs.python.org/3/reference/datamodel.html#object.__get__",
    "__getattr__": "https://docs.python.org/3/reference/datamodel.html#object.__getattr__",
    "__getattribute__": "https://docs.python.org/3/reference/datamodel.html#object.__getattribute__",
    "__getitem__": "https://docs.python.org/3/reference/datamodel.html#object.__getitem__",
    "__getnewargs__": "https://docs.python.org/3/library/pickle.html#object.__getnewargs__",
    "__getnewargs_ex__": "https://docs.python.org/3/library/pickle.html#object.__getnewargs_ex__",
    "__getstate__": "https://docs.python.org/3/library/pickle.html#object.__getstate__",
    "__gt__": "https://docs.python.org/3/reference/datamodel.html#object.__gt__",
    "__hash__": "https://docs.python.org/3/reference/datamodel.html#object.__hash__",
    "__iadd__": "https://docs.python.org/3/reference/datamodel.html#object.__iadd__",
    "__iand__": "https://docs.python.org/3/reference/datamodel.html#object.__iand__",
    "__ifloordiv__": "https://docs.python.org/3/reference/datamodel.html#object.__ifloordiv__",
    "__ilshift__": "https://docs.python.org/3/reference/datamodel.html#object.__ilshift__",
    "__imatmul__": "https://docs.python.org/3/reference/datamodel.html#object.__imatmul__",
    "__imod__": "https://docs.python.org/3/reference/datamodel.html#object.__imod__",
    "__imul__": "https://docs.python.org/3/reference/datamodel.html#object.__imul__",
    "__index__": "https://docs.python.org/3/reference/datamodel.html#object.__index__",
    "__init__": "https://docs.python.org/3/reference/datamodel.html#object.__init__",
    "__init_subclass__": "https://docs.python.org/3/reference/datamodel.html#object.__init_subclass__",
    "__instancecheck__": "https://docs.python.org/3/reference/datamodel.html#type.__instancecheck__",
    "__int__": "https://docs.python.org/3/reference/datamodel.html#object.__int__",
    "__invert__": "https://docs.python.org/3/reference/datamodel.html#object.__invert__",
    "__ior__": "https://docs.python.org/3/reference/datamodel.html#object.__ior__",
    "__ipow__": "https://docs.python.org/3/reference/datamodel.html#object.__ipow__",
    "__irshift__": "https://docs.python.org/3/reference/datamodel.html#object.__irshift__",
    "__isub__": "https://docs.python.org/3/reference/datamodel.html#object.__isub__",
    "__iter__": "https://docs.python.org/3/reference/datamodel.html#object.__iter__",
    "__itruediv__": "https://docs.python.org/3/reference/datamodel.html#object.__itruediv__",
    "__ixor__": "https://docs.python.org/3/reference/datamodel.html#object.__ixor__",
    "__le__": "https://docs.python.org/3/reference/datamodel.html#object.__le__",
    "__len__": "https://docs.python.org/3/reference/datamodel.html#object.__len__",
    "__length_hint__": "https://docs.python.org/3/reference/datamodel.html#object.__length_hint__",
    "__lshift__": "https://docs.python.org/3/reference/datamodel.html#object.__lshift__",
    "__lt__": "https://docs.python.org/3/reference/datamodel.html#object.__lt__",
    "__match_args__": "https://docs.python.org/3/reference/datamodel.html#object.__match_args__",
    "__matmul__": "https://docs.python.org/3/reference/datamodel.html#object.__matmul__",
    "__missing__": "https://docs.python.org/3/reference/datamodel.html#object.__missing__",
    "__mod__": "https://docs.python.org/3/reference/datamodel.html#object.__mod__",
    "__module__": "https://docs.python.org/3/reference/datamodel.html#type.__module__",
    "__mro__": "https://docs.python.org/3/reference/datamodel.html#type.__mro__",
    "__mro_entries__": "https://docs.python.org/3/reference/datamodel.html#object.__mro_entries__",
    "__mul__": "https://docs.python.org/3/reference/datamodel.html#object.__mul__",
    "__name__": "https://docs.python.org/3/reference/datamodel.html#type.__name__",
    "__ne__": "https://docs.python.org/3/reference/datamodel.html#object.__ne__",
    "__neg__": "https://docs.python.org/3/reference/datamodel.html#object.__neg__",
    "__new__": "https://docs.python.org/3/reference/datamodel.html#object.__new__",
    "__objclass__": "https://docs.python.org/3/reference/datamodel.html#object.__objclass__",
    "__or__": "https://docs.python.org/3/reference/datamodel.html#object.__or__",
    "__pos__": "https://docs.python.org/3/reference/datamodel.html#object.__pos__",
    "__pow__": "https://docs.python.org/3/reference/datamodel.html#object.__pow__",
    "__qualname__": "https://docs.python.org/3/reference/datamodel.html#type.__qualname__",
    "__radd__": "https://docs.python.org/3/reference/datamodel.html#object.__radd__",
    "__rand__": "https://docs.python.org/3/reference/datamodel.html#object.__rand__",
    "__rdivmod__": "https://docs.python.org/3/reference/datamodel.html#object.__rdivmod__",
    "__reduce__": "https://docs.python.org/3/library/pickle.html#object.__reduce__",
    "__reduce_ex__": "https://docs.python.org/3/library/pickle.html#object.__reduce_ex__",
    "__release_buffer__": "https://docs.python.org/3/reference/datamodel.html#object.__release_buffer__",
    "__replace__": "https://docs.python.org/3/library/copy.html#object.__replace__",
    "__repr__": "https://docs.python.org/3/reference/datamodel.html#object.__repr__",
    "__reversed__": "https://docs.python.org/3/reference/datamodel.html#object.__reversed__",
    "__rfloordiv__": "https://docs.python.org/3/reference/datamodel.html#object.__rfloordiv__",
    "__rlshift__": "https://docs.python.org/3/reference/datamodel.html#object.__rlshift__",
    "__rmatmul__": "https://docs.python.org/3/reference/datamodel.html#object.__rmatmul__",
    "__rmod__": "https://docs.python.org/3/reference/datamodel.html#object.__rmod__",
    "__rmul__": "https://docs.python.org/3/reference/datamodel.html#object.__rmul__",
    "__ror__": "https://docs.python.org/3/reference/datamodel.html#object.__ror__",
    "__round__": "https://docs.python.org/3/reference/datamodel.html#object.__round__",
    "__rpow__": "https://docs.python.org/3/reference/datamodel.html#object.__rpow__",
    "__rrshift__": "https://docs.python.org/3/reference/datamodel.html#object.__rrshift__",
    "__rshift__": "https://docs.python.org/3/reference/datamodel.html#object.__rshift__",
    "__rsub__": "https://docs.python.org/3/reference/datamodel.html#object.__rsub__",
    "__rtruediv__": "https://docs.python.org/3/reference/datamodel.html#object.__rtruediv__",
    "__rxor__": "https://docs.python.org/3/reference/datamodel.html#object.__rxor__",
    "__set__": "https://docs.python.org/3/reference/datamodel.html#object.__set__",
    "__set_name__": "https://docs.python.org/3/reference/datamodel.html#object.__set_name__",
    "__setattr__": "https://docs.python.org/3/reference/datamodel.html#object.__setattr__",
    "__setitem__": "https://docs.python.org/3/reference/datamodel.html#object.__setitem__",
    "__setstate__": "https://docs.python.org/3/library/pickle.html#object.__setstate__",
    "__slots__": "https://docs.python.org/3/reference/datamodel.html#object.__slots__",
    "__static_attributes__": "https://docs.python.org/3/reference/datamodel.html#type.__static_attributes__",
    "__str__": "https://docs.python.org/3/reference/datamodel.html#object.__str__",
    "__sub__": "https://docs.python.org/3/reference/datamodel.html#object.__sub__",
    "__subclasscheck__": "https://docs.python.org/3/reference/datamodel.html#type.__subclasscheck__",
    "__subclasses__": "https://docs.python.org/3/reference/datamodel.html#type.__subclasses__",
    "__truediv__": "https://docs.python.org/3/reference/datamodel.html#object.__truediv__",
    "__trunc__": "https://docs.python.org/3/reference/datamodel.html#object.__trunc__",
    "__type_params__": "https://docs.python.org/3/reference/datamodel.html#type.__type_params__",
    "__xor__": "https://docs.python.org/3/reference/datamodel.html#object.__xor__",
    "__future__": "https://docs.python.org/3/library/__future__.html",
    "__main__": "https://docs.python.org/3/library/__main__.html",
    # docs.python.org has duplicated url fragments for the following symbols, hard code to be the correct ones.
    "any": "https://docs.python.org/3/library/functions.html#any",
    "credits": "https://docs.python.org/3/library/constants.html#credits",
    "dict": "https://docs.python.org/3/library/stdtypes.html#dict",
    "encodings": "https://docs.python.org/3/reference/lexical_analysis.html#encodings",  # No module ref.
    "filter": "https://docs.python.org/3/library/functions.html#filter",
    "globals": "https://docs.python.org/3/library/functions.html#globals",
    "help": "https://docs.python.org/3/library/functions.html#help",
    "object": "https://docs.python.org/3/library/functions.html#object",
    "set": "https://docs.python.org/3/library/stdtypes.html#set",
    "type": "https://docs.python.org/3/library/functions.html#type",
}
