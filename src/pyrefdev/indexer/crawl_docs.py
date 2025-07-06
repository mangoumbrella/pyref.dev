from concurrent import futures
from pathlib import Path
import queue
import tempfile
import threading
from urllib import error, parse

import bs4
from packaging import version
from rich.progress import Progress, TaskID

from pyrefdev.config import console, get_packages, Package
from pyrefdev.indexer.requests import fetch_package_version, urlopen
from pyrefdev.indexer.schema import CrawlState


def crawl_docs(
    *,
    package: str | None = None,
    docs_directory: Path | None = None,
    force: bool = False,
    num_parallel_packages: int = 2,
    num_threads_per_package: int | None = None,
) -> None:
    """Crawl the docs into a local directory."""
    if num_parallel_packages <= 0:
        raise ValueError(
            f"--num-parallel-packages must be > 0, found {num_parallel_packages}"
        )
    if num_threads_per_package is None:
        num_threads_per_package = 2
    if num_threads_per_package <= 0:
        raise ValueError(
            f"--num-threads-per-package must be > 0, found {num_threads_per_package}"
        )

    if docs_directory:
        if docs_directory.exists():
            if not docs_directory.is_dir():
                console.fatal(f"{docs_directory} is not a directory")
    else:
        docs_directory = Path(tempfile.mkdtemp(prefix="pyref.dev."))

    console.print(f"Crawling documents into {docs_directory}")
    packages = get_packages(package)
    with Progress(console=console) as progress:
        task = progress.add_task(
            f"Crawling {len(packages)} packages", total=len(packages)
        )
        def crawl_package(pkg: Package):
            try:
                package_version = fetch_package_version(pkg)
                if package_version is None:
                    return
                subdir = docs_directory / pkg.pypi
                subdir.mkdir(parents=True, exist_ok=True)
                crawl_state_file = docs_directory / f"{pkg.pypi}.json"
                if not force and crawl_state_file.exists():
                    crawl_state = CrawlState.loads(crawl_state_file.read_text())
                    crawled_version = version.parse(crawl_state.package_version)
                    if package_version > crawled_version:
                        console.print(
                            f"{pkg} upgraded from {crawl_state.package_version} to {package_version!s}"
                        )
                        crawl_state = None
                    elif package_version < crawled_version:
                        console.warning(
                            f"{pkg}'s latest version {package_version!s} is older than previously crawled {crawl_state.package_version}"
                        )
                else:
                    crawl_state = None
                crawler = _Crawler(
                    pkg,
                    progress,
                    docs_directory / pkg.pypi,
                    pkg.index_url,
                    crawl_state,
                )
                crawler.crawl(num_threads=num_threads_per_package)
                crawler.save_crawl_state(package_version, crawl_state_file)
            finally:
                progress.advance(task)

        with futures.ThreadPoolExecutor(max_workers=num_parallel_packages) as executor:
            fs = [executor.submit(crawl_package, pkg) for pkg in packages]
            for f in fs:
                f.result()


class _Crawler:
    def __init__(
        self,
        package: Package,
        progress: Progress,
        docs_directory: Path,
        root_url: str,
        crawl_state: CrawlState | None,
    ):
        self._package = package
        self._progress = progress
        self._docs_directory = docs_directory
        self._root_url = root_url
        self._prefix = (
            root_url
            if root_url.endswith("/")
            else root_url.rsplit("/", maxsplit=1)[0] + "/"
        )

        self._seen_urls: set[str] = set()
        self._to_crawl_queue: queue.Queue[str] = queue.Queue()
        self._crawled_url_to_files: dict[str, Path] = {}
        self._lock = threading.RLock()

        self._crawl_state = crawl_state
        if crawl_state is None:
            self._failed_urls: list[str] = []
        else:
            self._failed_urls = crawl_state.failed_urls

    def crawl(self, *, num_threads: int) -> None:
        if self._crawl_state is None:
            self._to_crawl_queue.put(self._root_url)
            self._seen_urls.add(self._root_url)

            task = self._progress.add_task(f"Crawling {self._root_url}")
            threads = []
            for _ in range(num_threads):
                thread = threading.Thread(
                    target=self._crawl_thread, args=(task,), daemon=True
                )
                thread.start()
                threads.append(thread)
            self._to_crawl_queue.join()
            self._progress.update(task, visible=False)

        else:
            if not self._failed_urls:
                return
            task = self._progress.add_task(
                f"Retrying previously {len(self._failed_urls)} failed URLs",
                total=len(self._failed_urls),
            )

            def fetch_and_save(url: str) -> tuple[Path, str, str] | None:
                result = self._fetch_and_save_url(url)
                self._progress.advance(task)
                return result

            with futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                url_to_futures = {
                    url: executor.submit(fetch_and_save, url)
                    for url in list(self._failed_urls)  # Need to create a copy
                }
            failed_urls = []
            for url, f in url_to_futures.items():
                if (result := f.result()) is None:
                    failed_urls.append(url)
                else:
                    saved, _, _ = result
                    self._crawl_state.file_to_urls[
                        str(saved.relative_to(self._docs_directory))
                    ] = url
            self._crawl_state.failed_urls = failed_urls

    def save_crawl_state(self, package_version: version.Version, output: Path) -> None:
        if (state := self._crawl_state) is None:
            file_to_urls = {
                str(file.relative_to(self._docs_directory)): url
                for url, file in self._crawled_url_to_files.items()
            }
            state = CrawlState(
                package_version=str(package_version),
                file_to_urls=file_to_urls,
                failed_urls=self._failed_urls,
            )
        output.write_text(state.dumps())

    def _crawl_thread(self, task: TaskID) -> None:
        while True:
            url = self._to_crawl_queue.get()
            try:
                saved = self._crawl_url(url)
            finally:
                if saved is not None:
                    self._crawled_url_to_files[url] = saved
                self._progress.update(
                    task,
                    total=len(self._seen_urls),
                    completed=len(self._crawled_url_to_files),
                    refresh=True,
                )
                self._to_crawl_queue.task_done()

    def _fetch_and_save_url(self, url: str) -> tuple[Path, str, str] | None:
        try:
            with urlopen(url) as f:
                content = f.read().decode("utf-8", "backslashreplace")
        except error.URLError as e:
            console.warning(f"Failed to fetch url {url}, error: {e}")
            self._failed_urls.append(url)
            return None
        maybe_redirected_url = f.url
        if maybe_redirected_url != url and not self._should_crawl(maybe_redirected_url):
            return None
        saved = self._save(maybe_redirected_url, content)
        return saved, maybe_redirected_url, content

    def _crawl_url(self, url: str) -> Path | None:
        if (result := self._fetch_and_save_url(url)) is None:
            return None
        saved, maybe_redirected_url, content = result
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
        relative_path = url.removeprefix(self._prefix).removeprefix("/")
        output = self._docs_directory / relative_path
        if not relative_path.endswith(".html"):
            output = output / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            existing_content = output.read_text()
            if content == existing_content:
                return output
            console.warning(f"Overriding {output!s}")
        output.write_text(content)
        return output

    def _should_crawl(self, url: str) -> bool:
        if not url.startswith(self._prefix):
            return False
        for exclude in self._package.exclude_root_urls:
            if url.startswith(exclude):
                return False
        ext = url.rsplit("/", maxsplit=1)[-1].rsplit(".", maxsplit=1)[-1]
        return (not ext) or (ext == "html")

    def _parse_links(self, current_url: str, content: str) -> set[str]:
        try:
            soup = bs4.BeautifulSoup(content, "html.parser")
        except bs4.ParserRejectedMarkup:
            return set()
        links = set()
        for link in soup.find_all("a"):
            if (href := link.get("href")) is None:
                continue
            absolute_href = parse.urljoin(current_url, href)
            # href could be full URL, absolute path, and relative path.
            parsed_href = parse.urlparse(absolute_href)
            # Remove the fragment.
            parsed_href = parsed_href._replace(fragment="")
            links.add(parse.urlunparse(parsed_href))
        return links
