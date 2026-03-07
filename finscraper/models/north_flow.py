"""North flow data models."""
from pydantic import BaseModel
from datetime import datetime


class NorthFlowDaily(BaseModel):
    """North-bound capital flow daily data model."""
    
    date: datetime
    sh_net_inflow: float
    sz_net_inflow: float
    total_net_inflow: float
    sh_net_buy: float
    sz_net_buy: float
    total_net_buy: float


class NorthFlowIntraday(BaseModel):
    """North-bound capital flow intraday data model."""
    
    time: datetime
    sh_net_inflow: float
    sz_net_inflow: float
    total_net_inflow: float
