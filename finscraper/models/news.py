"""News data models."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsItem(BaseModel):
    """News item data model."""
    
    title: str
    content: Optional[str] = None
    source: str
    publish_time: datetime
    url: Optional[str] = None
    importance: Optional[int] = None
