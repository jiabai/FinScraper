import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class NewsFetcher(BaseFetcher):
    """Fetcher for news data."""
    
    def __init__(self):
        super().__init__("news")
    
    def fetch(self):
        """Fetch all news data."""
        return self.fetch_global()
    
    def fetch_global(self) -> pd.DataFrame:
        """Fetch global news."""
        self.logger.info("Fetching global news")
        
        try:
            df = self.client.fetch_news_global_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_news_global(df)
                self.logger.info(f"Fetched {len(df)} global news records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch global news: {e}")
            raise
    
    def fetch_alert(self) -> pd.DataFrame:
        """Fetch news alerts."""
        self.logger.info("Fetching news alerts")
        
        try:
            df = self.client.fetch_news_alert_em()
            if df is not None and not df.empty:
                df = self.cleaner.clean_news_alert(df)
                self.logger.info(f"Fetched {len(df)} news alert records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch news alerts: {e}")
            raise
    
    def fetch_stock(self, symbol: str) -> pd.DataFrame:
        """Fetch stock news."""
        self.logger.info(f"Fetching news for stock: {symbol}")
        
        try:
            df = self.client.fetch_news_stock_em(symbol=symbol)
            if df is not None and not df.empty:
                df = self.cleaner.clean_news_stock(df)
                self.logger.info(f"Fetched {len(df)} news records for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch news for {symbol}: {e}")
            raise
