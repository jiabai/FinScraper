"""Sector data models."""
from pydantic import BaseModel
from datetime import datetime


class SectorSpot(BaseModel):
    """Sector spot data model."""
    
    sector_code: str
    sector_name: str
    change_percent: float
    lead_stock: str
    lead_stock_change_percent: float
    total_stock_count: int
    up_count: int
    down_count: int
    amount: float
    updated_at: datetime


class SectorStock(BaseModel):
    """Sector stock data model."""
    
    sector_code: str
    sector_name: str
    stock_code: str
    stock_name: str
    change_percent: float
    price: float
    volume: int
    amount: float
