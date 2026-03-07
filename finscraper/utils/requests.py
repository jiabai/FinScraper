from typing import Dict, Any, Optional
from urllib.parse import urljoin, urlparse


def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def build_url(base_url: str, path: str, params: Optional[Dict[str, Any]] = None) -> str:
    url = urljoin(base_url, path)
    if params:
        import requests
        req = requests.Request("GET", url, params=params)
        prepared = req.prepare()
        return prepared.url
    return url
