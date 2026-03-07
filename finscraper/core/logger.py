"""Logging system for FinScraper."""
import sys
from pathlib import Path
from loguru import logger
from finscraper.config.settings import Settings


def get_logger(name: str):
    """Get a logger instance for the given module name."""
    settings = Settings()
    
    logger.remove()
    
    log_level = settings.log_level
    logger.add(sys.stderr, level=log_level, format="{time} | {level} | {name} | {message}")
    
    log_file = Path(settings.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(log_file, level="DEBUG", rotation="1 day", retention="7 days")
    
    return logger.bind(name=name)


def set_log_level(level: str):
    """Set the global log level."""
    import os
    os.environ["FINSCRAPER_LOG_LEVEL"] = level.upper()
