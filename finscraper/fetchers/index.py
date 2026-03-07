import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class IndexFetcher(BaseFetcher):
    """Fetcher for A-share index data."""
    
    def __init__(self):
        super().__init__("index")
    
    def fetch(self):
        """Fetch all index data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch index spot data."""
        self.logger.info("Fetching index spot data")

        try:
            df = self.client.fetch_index_spot_sina()
            if df is not None and not df.empty:
                df = self.cleaner.clean_index_spot(df)
                self.logger.info(f"Fetched {len(df)} index spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch index spot data: {e}")
            raise
    
    def fetch_history(
        self,
        symbol: str,
        start_date: str = "",
        end_date: str = "",
        period: str = "daily",
    ) -> pd.DataFrame:
        """Fetch index historical data."""
        self.logger.info(f"Fetching index history for {symbol}")
        
        try:
            df = self.client.fetch_index_hist_zh_a(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            if df is not None and not df.empty:
                df = self.cleaner.clean_index_history(df)
                self.logger.info(f"Fetched {len(df)} index history records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch index history for {symbol}: {e}")
            raise
