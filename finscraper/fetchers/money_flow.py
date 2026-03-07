import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class MoneyFlowFetcher(BaseFetcher):
    """Fetcher for money flow data."""
    
    def __init__(self):
        super().__init__("money-flow")
    
    def fetch(self):
        """Fetch all money flow data."""
        return self.fetch_market()
    
    def fetch_stock(self) -> pd.DataFrame:
        """Fetch stock money flow data."""
        self.logger.info("Fetching stock money flow data")
        
        try:
            df = self.client.fetch_money_flow_stock_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_money_flow_stock(df)
                self.logger.info(f"Fetched {len(df)} stock money flow records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch stock money flow data: {e}")
            raise
    
    def fetch_sector(self) -> pd.DataFrame:
        """Fetch sector money flow data."""
        self.logger.info("Fetching sector money flow data")
        
        try:
            df = self.client.fetch_money_flow_sector_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_money_flow_sector(df)
                self.logger.info(f"Fetched {len(df)} sector money flow records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch sector money flow data: {e}")
            raise
    
    def fetch_market(self) -> pd.DataFrame:
        """Fetch market money flow data."""
        self.logger.info("Fetching market money flow data")
        
        try:
            df = self.client.fetch_money_flow_market_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_money_flow_market(df)
                self.logger.info(f"Fetched {len(df)} market money flow records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch market money flow data: {e}")
            raise
