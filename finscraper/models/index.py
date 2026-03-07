"""A-share index data models."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IndexSpot(BaseModel):
    """A-share index spot data model."""
    
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    volume: int
    amount: float
    high: float
    low: float
    open: float
    close: float
    updated_at: datetime


class IndexHistory(BaseModel):
    """A-share index history data model."""
    
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
