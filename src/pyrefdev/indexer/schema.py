import dataclasses
import json


@dataclasses.dataclass
class CrawlState:
    package_version: str
    file_to_urls: dict[str, str]
    failed_urls: list[str]

    @classmethod
    def loads(cls, content: str) -> "CrawlState":
        return cls(**json.loads(content))

    def dumps(self) -> str:
        return json.dumps(dataclasses.asdict(self))
