import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class NorthFlowFetcher(BaseFetcher):
    """Fetcher for northbound capital flow data."""
    
    def __init__(self):
        super().__init__("north-flow")
    
    def fetch(self):
        """Fetch all north flow data."""
        return self.fetch_daily()
    
    def fetch_daily(self) -> pd.DataFrame:
        """Fetch north flow daily data."""
        self.logger.info("Fetching north flow daily data")
        
        try:
            df = self.client.fetch_em_north_flow_20()
            if df is not None and not df.empty:
                df = self.cleaner.clean_north_flow_daily(df)
                self.logger.info(f"Fetched {len(df)} north flow daily records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch north flow daily data: {e}")
            raise
    
    def fetch_intraday(self) -> pd.DataFrame:
        """Fetch north flow intraday data."""
        self.logger.info("Fetching north flow intraday data")
        
        try:
            df = self.client.fetch_em_north_flow_today()
            if df is not None and not df.empty:
                df = self.cleaner.clean_north_flow_intraday(df)
                self.logger.info(f"Fetched {len(df)} north flow intraday records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch north flow intraday data: {e}")
            raise
