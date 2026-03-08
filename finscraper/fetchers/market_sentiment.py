import pandas as pd
from finscraper.fetchers.base import BaseFetcher


class MarketSentimentFetcher(BaseFetcher):
    """Fetcher for market sentiment data."""
    
    def __init__(self):
        super().__init__("market-sentiment")
    
    def fetch(self):
        """Fetch all market sentiment data."""
        return self.fetch_sentiment()
    
    def fetch_sentiment(self) -> pd.DataFrame:
        """Fetch comprehensive market sentiment data."""
        self.logger.info("Fetching market sentiment data")
        
        try:
            up_down_df = self.fetch_up_down_count()
            limit_up_df = self.fetch_limit_up()
            limit_down_df = self.fetch_limit_down()
            
            sentiment_data = {
                "up_count": len(up_down_df[up_down_df["涨跌幅"] > 0]) if not up_down_df.empty and "涨跌幅" in up_down_df.columns else 0,
                "down_count": len(up_down_df[up_down_df["涨跌幅"] < 0]) if not up_down_df.empty and "涨跌幅" in up_down_df.columns else 0,
                "flat_count": len(up_down_df[up_down_df["涨跌幅"] == 0]) if not up_down_df.empty and "涨跌幅" in up_down_df.columns else 0,
                "limit_up_count": len(limit_up_df) if not limit_up_df.empty else 0,
                "limit_down_count": len(limit_down_df) if not limit_down_df.empty else 0,
            }
            
            df = pd.DataFrame([sentiment_data])
            self.logger.info("Successfully fetched market sentiment data")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch market sentiment data: {e}")
            raise
    
    def fetch_up_down_count(self) -> pd.DataFrame:
        """Fetch up/down stock count."""
        self.logger.info("Fetching up/down count")
        
        try:
            df = self.client.fetch_stock_zh_a_spot_fallback()
            if df is not None and not df.empty:
                df = self.cleaner.clean_market_sentiment_spot(df)
                self.logger.info(f"Fetched {len(df)} stocks for up/down count")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch up/down count: {e}")
            raise
    
    def fetch_limit_up(self, date: str = "") -> pd.DataFrame:
        """Fetch limit-up stocks."""
        self.logger.info("Fetching limit-up stocks")
        
        try:
            df = self.client.fetch_stock_zt_pool_em(date=date)
            if df is not None and not df.empty:
                df = self.cleaner.clean_limit_up(df)
                self.logger.info(f"Fetched {len(df)} limit-up stocks")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch limit-up stocks: {e}")
            raise
    
    def fetch_limit_down(self, date: str = "") -> pd.DataFrame:
        """Fetch limit-down stocks."""
        self.logger.info("Fetching limit-down stocks")
        
        try:
            df = self.client.fetch_stock_dt_pool_em(date=date)
            if df is not None and not df.empty:
                df = self.cleaner.clean_limit_down(df)
                self.logger.info(f"Fetched {len(df)} limit-down stocks")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch limit-down stocks: {e}")
            raise
