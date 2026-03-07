"""Base fetcher for all data types."""
from abc import ABC, abstractmethod
from finscraper.core.logger import get_logger
from finscraper.core.akshare_client import AkShareClient
from finscraper.core.data_cleaner import DataCleaner


class BaseFetcher(ABC):
    """Base fetcher for all data types."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"finscraper.fetchers.{name}")
        self.client = AkShareClient()
        self.cleaner = DataCleaner()
    
    @abstractmethod
    def fetch(self):
        """Fetch data from source."""
        pass
    
    def _fetch_with_retry(self, fetch_func, *args, **kwargs):
        """Execute fetch function with retry mechanism."""
        try:
            self.logger.info(f"Fetching {self.name} data")
            result = fetch_func(*args, **kwargs)
            self.logger.info(f"Successfully fetched {self.name} data")
            return result
        except Exception as e:
            self.logger.error(f"Failed to fetch {self.name} data: {e}")
            raise
