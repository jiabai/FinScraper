import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class ForexFetcher(BaseFetcher):
    """Fetcher for forex data."""
    
    def __init__(self):
        super().__init__("forex")
    
    def fetch(self):
        """Fetch all forex data."""
        return self.fetch_spot()
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch forex spot data."""
        self.logger.info("Fetching forex spot data")
        
        try:
            df = self.client.fetch_forex_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_forex_spot(df)
                self.logger.info(f"Fetched {len(df)} forex spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch forex spot data: {e}")
            raise
    
    def fetch_history(
        self,
        symbol: str,
        start_date: str = "",
        end_date: str = "",
        period: str = "daily",
    ) -> pd.DataFrame:
        """Fetch forex historical data."""
        self.logger.info(f"Fetching forex history for {symbol}")
        
        try:
            df = self.client.fetch_forex_hist_em(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            if df is not None and not df.empty:
                df = self.cleaner.clean_forex_history(df)
                self.logger.info(f"Fetched {len(df)} forex history records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch forex history for {symbol}: {e}")
            raise
    
    def fetch_latest(self, symbol: str = "USDCNH") -> dict:
        """Fetch latest forex data."""
        self.logger.info(f"Fetching latest forex data for {symbol}")
        try:
            return self.client.fetch_forex_latest(symbol)
        except Exception as e:
            self.logger.error(f"Failed to fetch latest forex data: {e}")
            return {}
