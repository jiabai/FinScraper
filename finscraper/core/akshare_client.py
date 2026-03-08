"""AkShare client with retry mechanism."""
import pandas as pd
import akshare as ak
from finscraper.core.logger import get_logger
from finscraper.core.retry import retry_with_backoff
from finscraper.core.exceptions import NetworkError

logger = get_logger(__name__)


class AkShareClient:
    """AkShare API client with retry mechanism."""
    
    def _call_akshare(self, func_name: str, **kwargs) -> pd.DataFrame:
        """Call akshare function with retry mechanism."""
        try:
            func = getattr(ak, func_name)
            logger.debug(f"Calling akshare.{func_name} with args: {kwargs}")
            return func(**kwargs)
        except Exception as e:
            logger.error(f"akshare.{func_name} failed: {e}")
            raise NetworkError(f"Failed to call akshare.{func_name}: {e}")
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_index_spot(self) -> pd.DataFrame:
        """Get A-share index spot data."""
        try:
            logger.info("Fetching index spot data")
            return ak.stock_zh_index_spot_sina()
        except Exception as e:
            logger.error(f"Failed to fetch index spot data: {e}")
            raise NetworkError(f"Failed to fetch index spot data: {e}")

    def fetch_index_spot_sina(self) -> pd.DataFrame:
        """Fetch A-share index spot data from Sina."""
        return self._call_akshare("stock_zh_index_spot_sina")
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_index_history(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "",
        end_date: str = ""
    ) -> pd.DataFrame:
        """Get A-share index history data."""
        try:
            logger.info(f"Fetching index history for {symbol}")
            return ak.index_zh_a_hist(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date
            )
        except Exception as e:
            logger.error(f"Failed to fetch index history: {e}")
            raise NetworkError(f"Failed to fetch index history: {e}")
    
    def fetch_index_hist_zh_a(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "",
        end_date: str = "",
    ) -> pd.DataFrame:
        """Fetch A-share index historical data."""
        return self._call_akshare(
            "index_zh_a_hist",
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_north_flow_daily(self) -> pd.DataFrame:
        """Get north-bound capital flow daily data."""
        try:
            logger.info("Fetching north flow daily data")
            return ak.stock_hsgt_fund_flow_summary_em()
        except Exception as e:
            logger.error(f"Failed to fetch north flow data: {e}")
            raise NetworkError(f"Failed to fetch north flow data: {e}")
    
    def fetch_em_north_flow_20(self) -> pd.DataFrame:
        """Fetch northbound capital flow daily data."""
        return self._call_akshare("stock_hsgt_fund_flow_summary_em")
    
    def fetch_em_north_flow_today(self) -> pd.DataFrame:
        """Fetch northbound capital flow intraday data."""
        return self._call_akshare("stock_hsgt_fund_min_em")
    
    def fetch_sector_list_ths(self) -> pd.DataFrame:
        """Fetch sector list from East Money."""
        return self._call_akshare("stock_sector_spot")
    
    def fetch_sector_spot_ths(self) -> pd.DataFrame:
        """Fetch sector spot data from East Money."""
        return self._call_akshare("stock_sector_spot")
    
    def fetch_sector_detail_ths(self, symbol: str) -> pd.DataFrame:
        """Fetch sector detail (not implemented)."""
        raise NotImplementedError("Sector detail not implemented yet")
    
    def fetch_commodity_spot_em(self) -> pd.DataFrame:
        """Fetch commodity spot data from East Money."""
        return self._call_akshare("futures_global_spot_em")
    
    def fetch_commodity_hist_em(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "",
        end_date: str = "",
    ) -> pd.DataFrame:
        """Fetch commodity historical data from East Money."""
        return self._call_akshare(
            "futures_zh_hist",
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )
    
    def fetch_money_flow_stock_em(self) -> pd.DataFrame:
        """Fetch stock money flow data from East Money."""
        return self._call_akshare("stock_fund_flow_individual")
    
    def fetch_money_flow_sector_em(self) -> pd.DataFrame:
        """Fetch sector money flow data from East Money."""
        return self._call_akshare("stock_fund_flow_industry")
    
    def fetch_money_flow_market_em(self) -> pd.DataFrame:
        """Fetch market money flow data from East Money."""
        return self._call_akshare("stock_market_fund_flow")
    
    def fetch_news_global_em(self) -> pd.DataFrame:
        """Fetch global news from East Money."""
        raise NotImplementedError("news_global function not available in current AkShare version")
    
    def fetch_news_alert_em(self) -> pd.DataFrame:
        """Fetch news alerts from East Money."""
        return self._call_akshare("stock_news_main_cx")
    
    def fetch_news_stock_em(self, symbol: str) -> pd.DataFrame:
        """Fetch stock news from East Money."""
        return self._call_akshare("stock_news_em", symbol=symbol)
    
    def fetch_stock_zh_a_spot_em(self) -> pd.DataFrame:
        """Fetch all A-share spot data from East Money."""
        return self._call_akshare("stock_zh_a_spot_em")
    
    def fetch_stock_zh_a_spot_sina(self) -> pd.DataFrame:
        """Fetch all A-share spot data from Sina (alternative source)."""
        return self._call_akshare("stock_zh_a_spot")
    
    def fetch_stock_sh_a_spot_em(self) -> pd.DataFrame:
        """Fetch Shanghai A-share spot data from East Money."""
        return self._call_akshare("stock_sh_a_spot_em")
    
    def fetch_stock_sz_a_spot_em(self) -> pd.DataFrame:
        """Fetch Shenzhen A-share spot data from East Money."""
        return self._call_akshare("stock_sz_a_spot_em")
    
    def fetch_stock_zh_a_spot_fallback(self) -> pd.DataFrame:
        """Fetch A-share spot data with fallback to alternative sources.
        
        Tries multiple sources in order:
        1. East Money (stock_zh_a_spot_em)
        2. Sina Finance (stock_zh_a_spot)  
        3. Separate SH/SZ exchanges from East Money
        """
        sources = [
            ("East Money", self.fetch_stock_zh_a_spot_em),
            ("Sina", self.fetch_stock_zh_a_spot_sina),
        ]
        
        for source_name, fetch_func in sources:
            try:
                logger.info(f"Trying to fetch from {source_name}...")
                df = fetch_func()
                if df is not None and not df.empty:
                    logger.info(f"Successfully fetched {len(df)} stocks from {source_name}")
                    return df
            except Exception as e:
                logger.warning(f"Failed to fetch from {source_name}: {e}")
        
        logger.warning("Primary sources failed, trying fallback (separate SH/SZ)...")
        try:
            sh_df = self.fetch_stock_sh_a_spot_em()
            sz_df = self.fetch_stock_sz_a_spot_em()
            if sh_df is not None and sz_df is not None:
                result = pd.concat([sh_df, sz_df], ignore_index=True)
                logger.info(f"Fetched {len(result)} stocks via fallback (SH: {len(sh_df)}, SZ: {len(sz_df)})")
                return result
        except Exception as e2:
            logger.error(f"All fallback methods failed: {e2}")
        
        raise NetworkError(f"Failed to fetch A-share spot data from all available sources")
    
    def fetch_stock_zt_pool_em(self, date: str = "") -> pd.DataFrame:
        """Fetch limit-up stock pool from East Money."""
        if date:
            return self._call_akshare("stock_zt_pool_em", date=date)
        return self._call_akshare("stock_zt_pool_em")
    
    def fetch_stock_dt_pool_em(self, date: str = "") -> pd.DataFrame:
        """Fetch limit-down stock pool from East Money."""
        if date:
            return self._call_akshare("stock_zt_pool_dtgc_em", date=date)
        return self._call_akshare("stock_zt_pool_dtgc_em")
    
    def fetch_index_hk_spot_em(self) -> pd.DataFrame:
        """Fetch Hong Kong index spot data from Sina."""
        return self._call_akshare("stock_hk_index_spot_sina")
    
    def fetch_index_us_spot(self, symbol: str = ".DJI") -> pd.DataFrame:
        """Fetch US index spot data from Sina (returns historical data, need to get latest close)."""
        return self._call_akshare("index_us_stock_sina", symbol=symbol)
    
    def fetch_us_index_latest(self) -> dict:
        """Fetch latest US index data from Sina."""
        indices = {
            ".DJI": "道琼斯",
            ".IXIC": "纳斯达克",
            ".INX": "标普500"
        }
        result = {}
        for symbol, name in indices.items():
            try:
                df = self._call_akshare("index_us_stock_sina", symbol=symbol)
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    result[name] = {
                        'price': latest['close'],
                        'change': latest.get('close', 0) - latest.get('open', 0),
                        'change_percent': ((latest.get('close', 0) - latest.get('open', 0)) / latest.get('open', 1) * 100) if latest.get('open', 0) else 0
                    }
            except Exception as e:
                logger.warning(f"Failed to fetch US index {name}: {e}")
        return result
    
    def fetch_index_global_spot(self) -> pd.DataFrame:
        """Fetch global index spot data."""
        return self._call_akshare("index_global_spot")
    
    def fetch_forex_spot_em(self) -> pd.DataFrame:
        """Fetch forex spot data from East Money (deprecated)."""
        return self._call_akshare("forex_spot_em")
    
    def fetch_forex_latest(self, symbol: str = "USDCNH") -> dict:
        """Fetch latest forex data from East Money."""
        try:
            df = self._call_akshare("forex_hist_em", symbol=symbol)
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                return {
                    'symbol': symbol,
                    'price': latest.get('最新价', 0),
                    'open': latest.get('今开', 0),
                    'change_percent': latest.get('振幅', 0)
                }
        except Exception as e:
            logger.warning(f"Failed to fetch forex {symbol}: {e}")
        return {}
    
    def fetch_forex_hist_em(
        self,
        symbol: str,
        period: str = "daily",
        start_date: str = "",
        end_date: str = "",
    ) -> pd.DataFrame:
        """Fetch forex historical data from East Money."""
        return self._call_akshare(
            "forex_hist_em",
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
        )
