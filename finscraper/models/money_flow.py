"""Money flow data models."""
from pydantic import BaseModel
from datetime import datetime


class StockMoneyFlow(BaseModel):
    """Stock money flow data model."""
    
    stock_code: str
    stock_name: str
    date: datetime
    main_net_inflow: float
    main_net_inflow_percent: float
    super_large_net_inflow: float
    super_large_net_inflow_percent: float
    large_net_inflow: float
    large_net_inflow_percent: float
    medium_net_inflow: float
    medium_net_inflow_percent: float
    small_net_inflow: float
    small_net_inflow_percent: float


class SectorMoneyFlow(BaseModel):
    """Sector money flow data model."""
    
    sector_code: str
    sector_name: str
    date: datetime
    net_inflow: float
    net_inflow_percent: float
    lead_stock: str
