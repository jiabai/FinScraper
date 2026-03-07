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
    
    def convert_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert all applicable columns to numeric type."""
        df = df.copy()
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors="ignore")
            except Exception:
                pass
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
    
    def clean_index_spot(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean index spot data."""
        df = df.copy()
        df = self.clean_column_names(df)
        df = self.convert_numeric_columns(df)
        return df
    
    def clean_index_history(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean index history data."""
        df = df.copy()
        df = self.clean_column_names(df)
        df = self.convert_numeric_columns(df)
        return df
    
    def clean_north_flow_daily(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean north flow daily data."""
        df = df.copy()
        df = self.clean_column_names(df)
        df = self.convert_numeric_columns(df)
        return df
    
    def clean_north_flow_intraday(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean north flow intraday data."""
        df = df.copy()
        df = self.clean_column_names(df)
        df = self.convert_numeric_columns(df)
        return df
    
    def clean_sector_list(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean sector list data."""
        df = df.copy()
        df = self.clean_column_names(df)
        return df
    
    def clean_sector_spot(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean sector spot data."""
        df = df.copy()
        df = self.clean_column_names(df)
        df = self.convert_numeric_columns(df)
        return df
    
    def clean_sector_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean sector stocks data."""
        df = df.copy()
        df = self.clean_column_names(df)
        df = self.convert_numeric_columns(df)
        return df
