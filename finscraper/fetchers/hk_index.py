import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class HKIndexFetcher(BaseFetcher):
    """Fetcher for Hong Kong index data."""
    
    def __init__(self):
        super().__init__("hk-index")
    
    def fetch(self):
        """Fetch all Hong Kong index data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch Hong Kong index spot data."""
        self.logger.info("Fetching Hong Kong index spot data")
        
        try:
            df = self.client.fetch_index_hk_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_hk_index_spot(df)
                self.logger.info(f"Fetched {len(df)} Hong Kong index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch Hong Kong index spot data: {e}")
            raise
