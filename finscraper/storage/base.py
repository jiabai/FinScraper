"""Base storage interface."""
from abc import ABC, abstractmethod
import pandas as pd


class BaseStorage(ABC):
    """Base storage interface."""
    
    @abstractmethod
    def save(self, data: pd.DataFrame, path: str, **kwargs) -> None:
        """Save data to storage."""
        pass
    
    @abstractmethod
    def load(self, path: str, **kwargs) -> pd.DataFrame:
        """Load data from storage."""
        pass
