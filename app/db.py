from app.entities import Url
from app.utils import get_env_var


class UrlsDB:
    def __init__(self, urls: str):
        self.URLS_DB = {
            url: None for url in get_env_var("URLS").replace(" ", "").split(",")
        }

    def get_url(self, url: str) -> Url:
        return Url(url=url, status=self.URLS_DB[url])

    def get_all_urls(self) -> list[Url]:
        return [Url(url=url, status=status) for url, status in self.URLS_DB.items()]

    def get_urls_by_status(self, status: bool) -> list[Url]:
        return [Url(url=url, status=s) for url, s in self.URLS_DB.items() if s == status]

    def change_url_status(self, url: str, status: bool):
        self.URLS_DB[url] = status # type: ignore

DB = UrlsDB(get_env_var("URLS"))
