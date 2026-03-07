"""SQLite database storage."""
import pandas as pd
import sqlite3
from finscraper.storage.base import BaseStorage
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class SQLiteStorage(BaseStorage):
    """SQLite database storage."""
    
    def save(
        self,
        data: pd.DataFrame,
        path: str,
        table_name: str = "data",
        **kwargs
    ) -> None:
        """Save DataFrame to SQLite database."""
        conn = sqlite3.connect(path)
        data.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        logger.info(f"Saved data to SQLite: {path}, table: {table_name}")
    
    def load(self, path: str, table_name: str = "data", **kwargs) -> pd.DataFrame:
        """Load DataFrame from SQLite database."""
        conn = sqlite3.connect(path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        logger.info(f"Loaded data from SQLite: {path}, table: {table_name}")
        return df
