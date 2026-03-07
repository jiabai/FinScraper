from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import time
import requests

from finscraper.config.settings import settings


class BaseSpider(ABC):
    def __init__(self, name: str):
        self.name = name
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": settings.user_agent})

    def _request(
        self,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        for attempt in range(settings.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    timeout=settings.request_timeout,
                )
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if attempt == settings.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError("Unreachable")

    @abstractmethod
    def fetch(self, *args: Any, **kwargs: Any) -> Any:
        pass
