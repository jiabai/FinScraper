import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class USIndexFetcher(BaseFetcher):
    """Fetcher for US index data."""
    
    def __init__(self):
        super().__init__("us-index")
    
    def fetch(self):
        """Fetch all US index data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch US index spot data."""
        self.logger.info("Fetching US index spot data")
        
        try:
            df = self.client.fetch_index_us_spot()
            if df is not None and not df.empty:
                df = self.cleaner.clean_us_index_spot(df)
                self.logger.info(f"Fetched {len(df)} US index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch US index spot data: {e}")
            raise
    
    def fetch_latest(self) -> dict:
        """Fetch latest US index data from Sina."""
        self.logger.info("Fetching latest US index data")
        try:
            return self.client.fetch_us_index_latest()
        except Exception as e:
            self.logger.error(f"Failed to fetch latest US index data: {e}")
            return {}
    
    def fetch_global(self) -> pd.DataFrame:
        """Fetch global index spot data."""
        self.logger.info("Fetching global index spot data")
        
        try:
            df = self.client.fetch_index_global_spot()
            if df is not None and not df.empty:
                df = self.cleaner.clean_global_index_spot(df)
                self.logger.info(f"Fetched {len(df)} global index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch global index spot data: {e}")
            raise
