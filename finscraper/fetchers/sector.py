import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class SectorFetcher(BaseFetcher):
    """Fetcher for sector data."""
    
    def __init__(self):
        super().__init__("sector")
    
    def fetch(self):
        """Fetch all sector data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch sector spot data."""
        self.logger.info("Fetching sector spot data")
        
        try:
            df = self.client.fetch_sector_spot_ths()
            if df is not None and not df.empty:
                df = self.cleaner.clean_sector_spot(df)
                self.logger.info(f"Fetched {len(df)} sector spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch sector spot data: {e}")
            raise
