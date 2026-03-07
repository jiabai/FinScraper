"""CSV file storage."""
import pandas as pd
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class CSVStorage(BaseStorage):
    """CSV file storage."""
    
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save DataFrame to CSV file."""
        data.to_csv(path, index=False, encoding="utf-8-sig")
        logger.info(f"Saved data to CSV: {path}")
    
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load DataFrame from CSV file."""
        df = pd.read_csv(path)
        logger.info(f"Loaded data from CSV: {path}")
        return df
