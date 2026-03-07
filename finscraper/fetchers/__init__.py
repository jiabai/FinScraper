"""Fetchers module for FinScraper."""
from finscraper.fetchers.index import IndexFetcher
from finscraper.fetchers.north_flow import NorthFlowFetcher
from finscraper.fetchers.sector import SectorFetcher
from finscraper.fetchers.commodity import CommodityFetcher
from finscraper.fetchers.money_flow import MoneyFlowFetcher
from finscraper.fetchers.news import NewsFetcher

__all__ = [
    "IndexFetcher",
    "NorthFlowFetcher",
    "SectorFetcher",
    "CommodityFetcher",
    "MoneyFlowFetcher",
    "NewsFetcher",
]

