"""Custom exceptions for FinScraper."""
from typing import Optional


class FinScraperError(Exception):
    """Base exception for FinScraper."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NetworkError(FinScraperError):
    """Network-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class DataError(FinScraperError):
    """Data-related errors."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(message)


class StorageError(FinScraperError):
    """Storage-related errors."""
    
    def __init__(self, message: str, path: Optional[str] = None):
        self.path = path
        super().__init__(message)


class ValidationError(FinScraperError):
    """Validation-related errors."""
    
    def __init__(self, message: str, param: Optional[str] = None):
        self.param = param
        super().__init__(message)
