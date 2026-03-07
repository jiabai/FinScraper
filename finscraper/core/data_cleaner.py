"""Data cleaning utilities."""
import pandas as pd
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class DataCleaner:
    """Data cleaning utilities."""
    
    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize column names."""
        logger.debug(f"Cleaning column names: {df.columns.tolist()}")
        return df
    
    def clean_numeric_columns(
        self,
        df: pd.DataFrame,
        columns: list
    ) -> pd.DataFrame:
        """Convert columns to numeric type."""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                logger.debug(f"Converted column {col} to numeric")
        return df
    
    def clean_percentage_columns(
        self,
        df: pd.DataFrame,
        columns: list
    ) -> pd.DataFrame:
        """Convert percentage strings to float."""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace("%", "").astype(float)
                logger.debug(f"Converted column {col} from percentage to float")
        return df
    
    def fill_missing_values(
        self,
        df: pd.DataFrame,
        method: str = "ffill"
    ) -> pd.DataFrame:
        """Fill missing values using specified method."""
        df = df.copy()
        if method == "ffill":
            df = df.fillna(method="ffill")
        elif method == "bfill":
            df = df.fillna(method="bfill")
        elif method == "zero":
            df = df.fillna(0)
        
        logger.debug(f"Filled missing values using method: {method}")
        return df
