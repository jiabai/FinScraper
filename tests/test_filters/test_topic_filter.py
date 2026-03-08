"""Tests for topic filter module."""
import pandas as pd
import pytest
from finscraper.filters import TopicFilter, TOPIC_KEYWORDS, get_topics


class TestTopicConfig:
    """Test topic configuration."""
    
    def test_get_topics(self):
        """Test getting list of topics."""
        topics = get_topics()
        assert isinstance(topics, list)
        assert len(topics) > 0
        assert "中东地缘" in topics
    
    def test_topic_keywords(self):
        """Test topic keywords are present."""
        assert "中东地缘" in TOPIC_KEYWORDS
        keywords = TOPIC_KEYWORDS["中东地缘"]
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert "中东" in keywords


class TestTopicFilter:
    """Test TopicFilter class."""
    
    @pytest.fixture
    def filter(self):
        """Create TopicFilter instance."""
        return TopicFilter()
    
    @pytest.fixture
    def sample_news(self):
        """Create sample news DataFrame."""
        data = {
            "标题": [
                "伊朗对美以发起新一波打击",
                "全国人大常委会召开会议",
                "特斯拉发布新款电动车",
                "美联储宣布利率决议",
                "普通新闻标题"
            ],
            "摘要": [
                "伊朗伊斯兰革命卫队今天发布公告...",
                "十三届全国人大常委会...",
                "Model 3 Highland 正式发布...",
                "FOMC会议决定维持利率不变...",
                "这是一条普通新闻..."
            ],
            "链接": [
                "https://example.com/news1",
                "https://example.com/news2",
                "https://example.com/news3",
                "https://example.com/news4",
                "https://example.com/news5"
            ]
        }
        return pd.DataFrame(data)
    
    def test_list_topics(self, filter):
        """Test listing topics."""
        topics = filter.list_topics()
        assert isinstance(topics, list)
        assert len(topics) > 0
    
    def test_filter_by_topic(self, filter, sample_news):
        """Test filtering news by topic."""
        result = filter.filter_by_topic(sample_news, "中东地缘", title_col="标题")
        assert len(result) == 1
        assert "伊朗" in result.iloc[0]["标题"]
        
        result = filter.filter_by_topic(sample_news, "美联储", title_col="标题")
        assert len(result) == 1
        assert "美联储" in result.iloc[0]["标题"]
        
        result = filter.filter_by_topic(sample_news, "不存在的专题", title_col="标题")
        assert len(result) == 0
    
    def test_get_topic_urls(self, filter, sample_news):
        """Test getting topic URLs."""
        urls = filter.get_topic_urls(sample_news, "中东地缘", title_col="标题", url_col="链接")
        assert isinstance(urls, list)
        assert len(urls) == 1
        assert urls[0] == "https://example.com/news1"
    
    def test_filter_multiple_topics(self, filter, sample_news):
        """Test filtering multiple topics."""
        result = filter.filter_multiple_topics(
            sample_news, 
            ["中东地缘", "美联储"], 
            title_col="标题"
        )
        assert isinstance(result, dict)
        assert "中东地缘" in result
        assert "美联储" in result
        assert len(result["中东地缘"]) == 1
        assert len(result["美联储"]) == 1
