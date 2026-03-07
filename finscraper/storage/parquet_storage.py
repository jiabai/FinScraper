"""Parquet file storage."""
import pandas as pd
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class ParquetStorage(BaseStorage):
    """Parquet file storage."""
    
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save DataFrame to Parquet file."""
        data.to_parquet(path, index=False)
        logger.info(f"Saved data to Parquet: {path}")
    
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load DataFrame from Parquet file."""
        df = pd.read_parquet(path)
        logger.info(f"Loaded data from Parquet: {path}")
        return df
