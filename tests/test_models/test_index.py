"""Tests for index models."""
import pytest
from datetime import datetime
from finscraper.models.index import IndexSpot, IndexHistory


def test_index_spot_creation():
    spot = IndexSpot(
        symbol="000001",
        name="上证指数",
        price=3000.50,
        change=10.50,
        change_percent=0.35,
        volume=1000000,
        amount=150000000.0,
        high=3010.0,
        low=2990.0,
        open=2995.0,
        close=3000.50,
        updated_at=datetime(2024, 1, 1, 15, 0, 0)
    )
    
    assert spot.symbol == "000001"
    assert spot.name == "上证指数"
    assert spot.price == 3000.50
    assert spot.change_percent == 0.35


def test_index_history_creation():
    history = IndexHistory(
        symbol="000001",
        date=datetime(2024, 1, 1),
        open=2995.0,
        high=3010.0,
        low=2990.0,
        close=3000.50,
        volume=1000000,
        amount=150000000.0
    )
    
    assert history.symbol == "000001"
    assert history.close == 3000.50


def test_index_spot_validation():
    with pytest.raises(ValueError):
        IndexSpot(
            symbol="000001",
            name="上证指数",
            price="invalid",
            change=10.50,
            change_percent=0.35,
            volume=1000000,
            amount=150000000.0,
            high=3010.0,
            low=2990.0,
            open=2995.0,
            close=3000.50,
            updated_at=datetime(2024, 1, 1, 15, 0, 0)
        )
