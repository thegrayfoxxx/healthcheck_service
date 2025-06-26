from dataclasses import dataclass


@dataclass
class Url:
    url: str
    status: bool | None = None
