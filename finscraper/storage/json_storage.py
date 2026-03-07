"""JSON file storage."""
import pandas as pd
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class JSONStorage(BaseStorage):
    """JSON file storage."""
    
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save DataFrame to JSON file."""
        data.to_json(path, orient="records", force_ascii=False, indent=2)
        logger.info(f"Saved data to JSON: {path}")
    
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load DataFrame from JSON file."""
        df = pd.read_json(path, orient="records")
        logger.info(f"Loaded data from JSON: {path}")
        return df
