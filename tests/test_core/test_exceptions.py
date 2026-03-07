"""Tests for exceptions module."""
import pytest
from finscraper.core.exceptions import (
    FinScraperError,
    NetworkError,
    DataError,
    StorageError,
    ValidationError,
)


def test_base_exception():
    error = FinScraperError("Test error")
    assert str(error) == "Test error"
    assert isinstance(error, Exception)


def test_network_error():
    error = NetworkError("Connection failed", status_code=500)
    assert str(error) == "Connection failed"
    assert error.status_code == 500


def test_data_error():
    error = DataError("Invalid data format", field="price")
    assert str(error) == "Invalid data format"
    assert error.field == "price"


def test_storage_error():
    error = StorageError("File write failed", path="/tmp/test.csv")
    assert str(error) == "File write failed"
    assert error.path == "/tmp/test.csv"


def test_validation_error():
    error = ValidationError("Invalid parameter", param="symbol")
    assert str(error) == "Invalid parameter"
    assert error.param == "symbol"
