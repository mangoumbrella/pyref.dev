import json
import os
from pathlib import Path
import queue
import tempfile
import threading
from urllib import parse, request

import bs4
from rich.progress import Progress, TaskID

from .config import console, SUPPORTED_DOCS


def crawl_docs(output_directory: Path | None = None, num_threads: int = 2) -> None:
    """Crawl the docs into a local directory."""
    if output_directory:
        if output_directory.exists():
            if not output_directory.is_dir():
                pass
    else:
        output_directory = Path(tempfile.mkdtemp(prefix="pyref.dev."))

    console.print(f"Crawling documents into {output_directory}")
    for name, website in SUPPORTED_DOCS.items():
        subdir = output_directory / name
        if subdir.exists():
            console.fatal(f"{subdir} already exists.")
        subdir.mkdir(parents=True)
        crawler = _Crawler(
            output_directory / name,
            website,
        )
        crawler.crawl(num_threads=num_threads)
        crawler.save_url_map(output_directory / f"{name}.json")


class _Crawler:
    def __init__(self, output_directory: Path, root_url: str):
        self._output_directory = output_directory
        self._root_url = root_url

        self._seen_urls: set[str] = set()
        self._to_crawl_queue: queue.Queue[str] = queue.Queue()
        self._crawled_url_to_files: dict[str, Path] = {}
        self._lock = threading.RLock()

    def crawl(self, *, num_threads: int) -> None:
        if num_threads <= 0:
            raise ValueError(f"num_threads must be > 0, found {num_threads=}")
        self._to_crawl_queue.put(self._root_url)
        self._seen_urls.add(self._root_url)

        with Progress(console=console) as progress:
            task = progress.add_task(f"Crawling {self._root_url}")
            threads = []
            for _ in range(num_threads):
                thread = threading.Thread(
                    target=self._crawl_thread, args=(progress, task), daemon=True
                )
                thread.start()
                threads.append(thread)
            self._to_crawl_queue.join()

    def save_url_map(self, output: Path) -> None:
        metadata = {
            str(file.relative_to(self._output_directory)): url
            for url, file in self._crawled_url_to_files.items()
        }
        output.write_text(json.dumps(metadata))

    def _crawl_thread(self, progress: Progress, task: TaskID) -> None:
        while True:
            url = self._to_crawl_queue.get()
            try:
                saved = self._crawl_url(url)
            finally:
                if saved is not None:
                    self._crawled_url_to_files[url] = saved
                progress.update(
                    task,
                    total=len(self._seen_urls),
                    completed=len(self._crawled_url_to_files),
                    refresh=True,
                )
                self._to_crawl_queue.task_done()

    def _crawl_url(self, url: str) -> Path | None:
        try:
            with request.urlopen(url) as f:
                content = f.read().decode("utf-8", "backslashreplace")
        except request.URLError as e:
            console.print(
                "[yellow]WARNING:[/yellow] Failed to fetch url %s, error: %s", url, e
            )
            return None
        maybe_redirected_url = f.url
        if maybe_redirected_url != url and not self._should_crawl(maybe_redirected_url):
            return None
        saved = self._save(maybe_redirected_url, content)
        self._seen_urls.add(maybe_redirected_url)
        new_links = self._parse_links(maybe_redirected_url, content)
        with self._lock:
            for new_link in new_links:
                if new_link in self._seen_urls:
                    continue
                if not self._should_crawl(new_link):
                    continue
                self._to_crawl_queue.put(new_link)
                self._seen_urls.add(new_link)
        return saved

    def _save(self, url: str, content: str) -> Path:
        relative_path = url.removeprefix(self._root_url).removeprefix("/")
        output = self._output_directory / relative_path
        if not relative_path.endswith(".html"):
            output = output / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            existing_content = output.read_text()
            if content == existing_content:
                return output
            console.print(f"[yellow]WARNING:[/yellow] Overriding {output!s}")
        output.write_text(content)
        return output

    def _should_crawl(self, url: str) -> bool:
        if not url.startswith(self._root_url):
            return False
        ext = url.rsplit("/", maxsplit=1)[-1].rsplit(".", maxsplit=1)[-1]
        return (not ext) or (ext == "html")

    def _parse_links(self, current_url: str, content: str) -> set[str]:
        try:
            soup = bs4.BeautifulSoup(content, "html.parser")
        except bs4.ParserRejectedMarkup:
            return set()
        parsed_current_url = parse.urlparse(current_url)
        links = set()
        for link in soup.find_all("a"):
            if (href := link.get("href")) is None:
                continue
            # href could be full URL, absolute path, and relative path.
            parsed_href = parse.urlparse(href)
            # Remove the fragment.
            parsed_href = parsed_href._replace(fragment="")
            if parsed_href.netloc:
                pass
            elif parsed_href.path.startswith("/"):
                # Absolute path
                parsed_href = parsed_href._replace(
                    scheme=parsed_current_url.scheme, netloc=parsed_current_url.netloc
                )
            else:
                # Relative path
                new_path = os.path.normpath(
                    os.path.join(
                        os.path.dirname(parsed_current_url.path), parsed_href.path
                    )
                )
                parsed_href = parsed_href._replace(
                    scheme=parsed_current_url.scheme,
                    netloc=parsed_current_url.netloc,
                    path=new_path,
                )
            links.add(parse.urlunparse(parsed_href))
        return links
