"""US index data models."""
from pydantic import BaseModel
from datetime import datetime


class USIndexSpot(BaseModel):
    """US index spot data model."""
    
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
