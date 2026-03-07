"""AkShare client with retry mechanism."""
import pandas as pd
import akshare as ak
from finscraper.core.logger import get_logger
from finscraper.core.retry import retry_with_backoff
from finscraper.core.exceptions import NetworkError

logger = get_logger(__name__)


class AkShareClient:
    """AkShare API client with retry mechanism."""
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_index_spot(self) -> pd.DataFrame:
        """Get A-share index spot data."""
        try:
            logger.info("Fetching index spot data")
            return ak.index_zh_a_spot_em()
        except Exception as e:
            logger.error(f"Failed to fetch index spot data: {e}")
            raise NetworkError(f"Failed to fetch index spot data: {e}")
    
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
    
    @retry_with_backoff(max_retries=3, exceptions=(Exception,))
    def get_north_flow_daily(self) -> pd.DataFrame:
        """Get north-bound capital flow daily data."""
        try:
            logger.info("Fetching north flow daily data")
            return ak.stock_em_hsgt_north_net_flow_in_em(symbol="北向")
        except Exception as e:
            logger.error(f"Failed to fetch north flow data: {e}")
            raise NetworkError(f"Failed to fetch north flow data: {e}")
