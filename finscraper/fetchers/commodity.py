import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class CommodityFetcher(BaseFetcher):
    """Fetcher for commodity data."""
    
    def __init__(self):
        super().__init__("commodity")
    
    def fetch(self):
        """Fetch all commodity data."""
        return self.fetch_spot()
    
    def fetch_list(self) -> pd.DataFrame:
        """Fetch commodity list."""
        self.logger.info("Fetching commodity list")
        
        try:
            df = self.client.fetch_commodity_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_commodity_spot(df)
                self.logger.info(f"Fetched {len(df)} commodities")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch commodity list: {e}")
            raise
    
    def fetch_spot(self) -> pd.DataFrame:
        """Fetch commodity spot data."""
        self.logger.debug("Fetching commodity spot data")
        
        try:
            df = self.client.fetch_commodity_spot_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_commodity_spot(df)
                self.logger.debug(f"Fetched {len(df)} commodity spot records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch commodity spot data: {e}")
            raise
    
    def fetch_history(
        self,
        symbol: str,
        start_date: str = "",
        end_date: str = "",
        period: str = "daily",
    ) -> pd.DataFrame:
        """Fetch commodity historical data."""
        self.logger.info(f"Fetching commodity history for {symbol}")
        
        try:
            df = self.client.fetch_commodity_hist_em(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
            if df is not None and not df.empty:
                df = self.cleaner.clean_commodity_history(df)
                self.logger.info(f"Fetched {len(df)} commodity history records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch commodity history for {symbol}: {e}")
            raise
