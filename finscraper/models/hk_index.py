"""Hong Kong index data models."""
from pydantic import BaseModel
from datetime import datetime


class HKIndexSpot(BaseModel):
    """Hong Kong index spot data model."""
    
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
