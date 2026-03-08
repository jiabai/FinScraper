"""Forex data models."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ForexSpot(BaseModel):
    """Forex spot data model."""
    
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    high: float
    low: float
    open: float
    close: float
    updated_at: datetime


class ForexHistory(BaseModel):
    """Forex history data model."""
    
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
