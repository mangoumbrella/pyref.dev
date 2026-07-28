from concurrent import futures
from pathlib import Path
import contextlib
import queue
import signal
import threading
from typing import Any, Iterator
from urllib import error, parse

import bs4
from packaging import version
from rich.progress import (
    BarColumn,
    Progress,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from pyrefdev.config import console, get_packages, Package
from pyrefdev.indexer import objects_inv
from pyrefdev.indexer.index import Index, IndexState, urlopen


def _http_error_code(code: int) -> str:
    """Generate HTTP error code string."""
    return f"http-{code}"


HTTP_404_ERROR = _http_error_code(404)


def url_prefix(root_url: str) -> str:
    """The prefix a URL must start with to belong to a package's docs."""
    if root_url.endswith("/"):
        return root_url
    return root_url.rsplit("/", maxsplit=1)[0] + "/"


def save_path(url: str, prefix: str, docs_directory: Path) -> Path:
    """Where a crawled URL is stored on disk."""
    relative_path = url.removeprefix(prefix).removeprefix("/")
    output = docs_directory / relative_path
    if not relative_path.endswith(".html"):
        output = output / "index.html"
    return output


def should_crawl(url: str, prefix: str, exclude_root_urls: list[str]) -> bool:
    if not url.startswith(prefix):
        return False
    for exclude in exclude_root_urls:
        if url.startswith(exclude):
            return False
    ext = url.rsplit("/", maxsplit=1)[-1].rsplit(".", maxsplit=1)[-1]
    return (not ext) or (ext == "html")


def parse_links(current_url: str, content: str) -> set[str]:
    try:
        soup = bs4.BeautifulSoup(content, "html.parser")
    except bs4.ParserRejectedMarkup:
        return set()
    links = set()
    for link in soup.find_all("a"):
        href = link.get("href")
        if not isinstance(href, str):
            continue
        # href could be full URL, absolute path, and relative path.
        try:
            parsed_href = parse.urlparse(parse.urljoin(current_url, href))
        except ValueError:
            # A bad IPv6 literal in an href must not abort the page.
            continue
        # Remove the fragment.
        parsed_href = parsed_href._replace(fragment="")
        links.add(parse.urlunparse(parsed_href))
    return links


@contextlib.contextmanager
def _handle_interrupt(stop: threading.Event) -> Iterator[None]:
    """Turn the first Ctrl-C into a clean stop that preserves the frontier."""

    def handler(signum, frame):
        if stop.is_set():
            signal.signal(signal.SIGINT, previous)
            raise KeyboardInterrupt
        console.warning(
            "Interrupted, saving progress. Press Ctrl-C again to abort immediately."
        )
        stop.set()

    try:
        previous = signal.signal(signal.SIGINT, handler)
    except ValueError:
        # Not the main thread, so the caller owns signal handling.
        yield
        return
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, previous)


def crawl_docs(
    *,
    package: str | None = None,
    force: bool = False,
    upgrade: bool = False,
    retry_failed_urls: bool = True,
    retry_http_404: bool = False,
    index: Index = Index(),
    num_parallel_packages: int = 1,
    num_threads_per_package: int = 1,
    seconds_to_sleep_between_requests: float = 5.0,
    show_overall_progress: bool = True,
) -> None:
    """Crawl the docs into a local directory."""
    if num_parallel_packages <= 0:
        raise ValueError(
            f"--num-parallel-packages must be > 0, found {num_parallel_packages}"
        )
    if num_threads_per_package <= 0:
        raise ValueError(
            f"--num-threads-per-package must be > 0, found {num_threads_per_package}"
        )

    if show_overall_progress:
        console.print(f"Crawling documents into {index.docs_directory}")
    packages = get_packages(package)
    if not force and not upgrade and not retry_failed_urls:
        packages = [
            pkg
            for pkg in packages
            if (state := index.load_crawl_state(pkg.pypi)) is None
            or not state.completed
        ]

    stop = threading.Event()
    with (
        _handle_interrupt(stop),
        Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None),
            TaskProgressColumn(),
            TextColumn("{task.fields[extra]}"),
            TimeRemainingColumn(),
            console=console,
        ) as progress,
    ):
        if show_overall_progress:
            task = progress.add_task(
                f"Crawling {len(packages)} packages", total=len(packages), extra=""
            )
        else:
            task = None

        def crawl_package(pkg: Package):
            if stop.is_set():
                return
            try:
                package_version = index.fetch_package_version(pkg)
                if package_version is None:
                    return
                if pkg.objects_inv_url:
                    _crawl_objects_inv(pkg, index, stop)
                crawl_state = index.load_crawl_state(pkg.pypi)
                if crawl_state is not None:
                    crawled_version = version.parse(crawl_state.package_version)
                    if force:
                        console.print(f"{pkg.pypi} forced to re-crawl")
                        crawl_state = None
                    elif upgrade and package_version > crawled_version:
                        console.print(
                            f"{pkg.pypi} upgraded from {crawl_state.package_version} to {package_version!s}"
                        )
                        crawl_state = None
                    elif package_version < crawled_version:
                        console.warning(
                            f"{pkg.pypi}'s latest version {package_version!s} is older than previously crawled {crawl_state.package_version}"
                        )
                else:
                    crawl_state = None
                crawler = _Crawler(
                    pkg,
                    progress,
                    index,
                    pkg.index_url,
                    crawl_state,
                    seconds_to_sleep_between_requests,
                    retry_http_404,
                    stop,
                )
                try:
                    crawler.crawl(
                        num_threads=num_threads_per_package,
                        retry_failed_urls=retry_failed_urls,
                    )
                finally:
                    # Re-crawling from scratch costs hours at this rate limit.
                    crawler.save_crawl_state(package_version, index)
            except Exception as e:
                console.warning(f"Failed to crawl {pkg.pypi}, error: {e}")
            finally:
                if task is not None:
                    progress.advance(task)

        with futures.ThreadPoolExecutor(max_workers=num_parallel_packages) as executor:
            fs = [executor.submit(crawl_package, pkg) for pkg in packages]
            for f in fs:
                f.result()

    if stop.is_set():
        raise KeyboardInterrupt


def _crawl_objects_inv(
    package: Package, index: Index, stop: threading.Event | None = None
) -> None:
    """Save the Sphinx inventory next to the package's crawled pages."""
    assert package.objects_inv_url is not None
    try:
        with urlopen(package.objects_inv_url, stop=stop) as f:
            content = f.read()
    except Exception as e:
        # Docs without an inventory are still worth crawling.
        console.warning(f"Failed to fetch {package.objects_inv_url}, error: {e}")
        return
    output = index.docs_directory / package.pypi / objects_inv.FILENAME
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)


class _Crawler:
    def __init__(
        self,
        package: Package,
        progress: Progress,
        index: Index,
        root_url: str,
        crawl_state: IndexState | None,
        seconds_to_sleep_between_requests: float,
        retry_http_404: bool,
        stop: threading.Event,
    ):
        self._package = package
        self._progress = progress
        self._docs_directory = index.docs_directory / package.pypi
        self._root_url = root_url
        self._prefix = url_prefix(root_url)
        self._seconds_to_sleep_between_requests = seconds_to_sleep_between_requests
        self._retry_http_404 = retry_http_404
        self._stop = stop

        self._seen_urls: set[str] = set()
        # None is the sentinel that tells a worker thread to exit.
        self._to_crawl_queue: queue.Queue[str | None] = queue.Queue()
        self._lock = threading.RLock()
        self._pending_urls: list[str] = []
        self._completed = False

        self._crawl_state = crawl_state
        if crawl_state is None:
            self._file_to_urls: dict[str, str] = {}
            self._failed_urls: dict[str, str] = {}
            self._redirects: dict[str, str] = {}
        else:
            self._file_to_urls = crawl_state.file_to_urls
            self._failed_urls = crawl_state.failed_urls
            self._redirects = crawl_state.redirects
            # Already-fetched pages must not be fetched again on resume, and a
            # URL that redirected counts as fetched under either of its names.
            self._seen_urls.update(self._file_to_urls.values())
            self._seen_urls.update(self._redirects)
            self._seen_urls.update(self._redirects.values())

    def _initial_urls(self, *, retry_failed_urls: bool) -> list[str]:
        """The frontier to start from: the root, or whatever the last run left."""
        if self._crawl_state is None:
            return [self._root_url]
        urls = list(self._crawl_state.pending_urls)
        if retry_failed_urls:
            urls.extend(
                url
                for url, error_code in self._failed_urls.items()
                if error_code != HTTP_404_ERROR or self._retry_http_404
            )
        return list(dict.fromkeys(urls))

    def crawl(self, *, num_threads: int, retry_failed_urls: bool) -> None:
        initial_urls = self._initial_urls(retry_failed_urls=retry_failed_urls)
        if not initial_urls:
            # An empty frontier means the previous run exhausted it.
            self._completed = True
            return

        for url in initial_urls:
            self._seen_urls.add(url)
            self._to_crawl_queue.put(url)

        task = self._progress.add_task(
            f"Crawling {self._root_url.removeprefix('https://')}",
            total=len(self._seen_urls),
            completed=len(self._file_to_urls),
            extra="",
        )
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(
                target=self._crawl_thread, args=(task,), daemon=True
            )
            thread.start()
            threads.append(thread)
        try:
            self._to_crawl_queue.join()
            # Workers drain the queue without fetching once stopped, so an empty
            # queue only means the crawl finished if nothing asked it to stop.
            self._completed = not self._stop.is_set()
        finally:
            # Otherwise every package leaks num_threads blocked workers.
            for _ in threads:
                self._to_crawl_queue.put(None)
            for thread in threads:
                thread.join()
            self._record_pending()
        self._progress.update(task, visible=False)

    def _record_pending(self) -> None:
        # Whatever is left is the frontier the next run has to resume from.
        while True:
            try:
                url = self._to_crawl_queue.get_nowait()
            except queue.Empty:
                return
            if url is not None:
                with self._lock:
                    self._pending_urls.append(url)

    def save_crawl_state(self, package_version: version.Version, index: Index) -> None:
        with self._lock:
            state = IndexState(
                package_version=str(package_version),
                file_to_urls=dict(self._file_to_urls),
                failed_urls=dict(self._failed_urls),
                redirects=dict(self._redirects),
                pending_urls=list(dict.fromkeys(self._pending_urls)),
                completed=self._completed,
            )
        index.save_crawl_state(self._package.pypi, state)

    def _crawl_thread(self, task: TaskID) -> None:
        while True:
            url = self._to_crawl_queue.get()
            if url is None:
                self._to_crawl_queue.task_done()
                return
            if self._stop.is_set():
                # Drain without fetching so join() returns and the frontier survives.
                with self._lock:
                    self._pending_urls.append(url)
                self._to_crawl_queue.task_done()
                continue
            result = None
            try:
                result = self._crawl_url(url)
            except Exception as e:
                # An escaping exception would skip task_done() and hang crawl.
                console.warning(f"Failed to crawl url {url}, error: {e}")
                self._record_failure(url, "")
            finally:
                # task_done() last would be skipped if the update below raises.
                try:
                    kwargs: dict[str, Any] = {}
                    with self._lock:
                        if result is not None:
                            saved, final_url = result
                            relative = str(saved.relative_to(self._docs_directory))
                            # The file is named after the URL the content came
                            # from, so record that one and keep the redirect
                            # separately rather than losing either name.
                            self._file_to_urls[relative] = final_url
                            if final_url != url:
                                self._redirects[url] = final_url
                            # A URL that succeeds is no longer a failure to retry.
                            self._failed_urls.pop(url, None)
                            kwargs["extra"] = str(saved)[-24:]
                        total = len(self._seen_urls)
                        completed = len(self._file_to_urls)
                    self._progress.update(
                        task,
                        total=total,
                        completed=completed,
                        refresh=True,
                        **kwargs,
                    )
                finally:
                    self._to_crawl_queue.task_done()

    def _record_failure(self, url: str, error_code: str) -> None:
        with self._lock:
            self._failed_urls[url] = error_code

    def _fetch_and_save_url(self, url: str) -> tuple[Path, str, str] | None:
        try:
            with urlopen(url, stop=self._stop) as f:
                content = f.read().decode("utf-8", "backslashreplace")
        except error.HTTPError as e:
            console.warning(f"Failed to fetch url {url}, error: {e}")
            self._record_failure(url, _http_error_code(e.code))
            return None
        except Exception as e:
            console.warning(f"Failed to fetch url {url}, error: {e}")
            self._record_failure(url, "")
            return None
        finally:
            # Failures need pacing too, or a failing host gets hammered.
            self._stop.wait(self._seconds_to_sleep_between_requests)
        maybe_redirected_url = f.url
        if maybe_redirected_url != url and not self._should_crawl(maybe_redirected_url):
            return None
        try:
            saved = self._save(maybe_redirected_url, content)
        except OSError as e:
            # A URL can exceed NAME_MAX or collide with an existing directory.
            console.warning(f"Failed to save url {url}, error: {e}")
            self._record_failure(url, "")
            return None
        return saved, maybe_redirected_url, content

    def _crawl_url(self, url: str) -> tuple[Path, str] | None:
        if (result := self._fetch_and_save_url(url)) is None:
            return None
        saved, maybe_redirected_url, content = result
        new_links = self._parse_links(maybe_redirected_url, content)
        with self._lock:
            self._seen_urls.add(maybe_redirected_url)
            for new_link in new_links:
                if new_link in self._seen_urls:
                    continue
                if not self._should_crawl(new_link):
                    continue
                self._to_crawl_queue.put(new_link)
                self._seen_urls.add(new_link)
        return saved, maybe_redirected_url

    def _save(self, url: str, content: str) -> Path:
        output = save_path(url, self._prefix, self._docs_directory)
        output.parent.mkdir(parents=True, exist_ok=True)
        # Bytes keep this independent of the locale's default encoding.
        encoded = content.encode("utf-8")
        if output.exists() and output.read_bytes() == encoded:
            return output
        output.write_bytes(encoded)
        return output

    def _should_crawl(self, url: str) -> bool:
        return should_crawl(url, self._prefix, self._package.exclude_root_urls)

    def _parse_links(self, current_url: str, content: str) -> set[str]:
        return parse_links(current_url, content)
