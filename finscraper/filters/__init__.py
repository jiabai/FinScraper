"""Filters module for FinScraper."""
from finscraper.filters.topic_filter import TopicFilter
from finscraper.filters.topic_config import (
    TOPIC_KEYWORDS,
    get_topics,
    get_keywords,
    add_topic,
    remove_topic
)

__all__ = [
    "TopicFilter",
    "TOPIC_KEYWORDS",
    "get_topics",
    "get_keywords",
    "add_topic",
    "remove_topic"
]
