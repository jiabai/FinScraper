"""Commodity data models."""
from pydantic import BaseModel
from datetime import datetime


class CommoditySpot(BaseModel):
    """Commodity spot data model."""
    
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
    unit: str
    high: float
    low: float
    open: float
    close: float
    updated_at: datetime


class CommodityHistory(BaseModel):
    """Commodity history data model."""
    
    symbol: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    open_interest: int
