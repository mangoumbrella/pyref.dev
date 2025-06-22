from yib import yconsole


console = yconsole.Console(stderr=True)


SUPPORTED_DOCS: dict[str, str] = {
    "__python__": "https://docs.python.org/3/",  # Trailing slash to prevent crawling docs like https://docs.python.org/3.5/
}
