"""Tests for logger module."""
import pytest
from finscraper.core.logger import get_logger, set_log_level


def test_get_logger_returns_logger():
    logger = get_logger("test_module")
    assert logger is not None
    assert hasattr(logger, "info")
    assert hasattr(logger, "error")


def test_set_log_level():
    import os
    os.environ["FINSCRAPER_LOG_LEVEL"] = "DEBUG"
    logger = get_logger("test_debug")
    assert logger is not None


def test_logger_writes_to_file(tmp_path):
    import os
    from pathlib import Path
    
    log_file = tmp_path / "test.log"
    os.environ["FINSCRAPER_LOG_FILE"] = str(log_file)
    
    logger = get_logger("test_file")
    logger.info("Test message")
    
    assert log_file.exists()
