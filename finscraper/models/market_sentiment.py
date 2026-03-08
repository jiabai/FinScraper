"""Market sentiment data models."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MarketSentimentSpot(BaseModel):
    """Market sentiment spot data model."""
    
    up_count: int
    down_count: int
    flat_count: int
    limit_up_count: int
    limit_down_count: int
    updated_at: datetime


class LimitUpStock(BaseModel):
    """Limit-up stock data model."""
    
    symbol: str
    name: str
    price: float
    change_percent: float
    limit_up_time: Optional[str] = None
    first_limit_up_time: Optional[str] = None
    last_limit_up_time: Optional[str] = None
    open_times: Optional[int] = None


class LimitDownStock(BaseModel):
    """Limit-down stock data model."""
    
    symbol: str
    name: str
    price: float
    change_percent: float
    limit_down_time: Optional[str] = None
