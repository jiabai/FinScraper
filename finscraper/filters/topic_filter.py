"""
专题新闻筛选模块
"""
import pandas as pd
from typing import Optional, List, Dict
from finscraper.filters.topic_config import (
    TOPIC_KEYWORDS,
    get_topics,
    get_keywords
)
from finscraper.core.logger import get_logger

logger = get_logger(__name__)


class TopicFilter:
    """专题新闻筛选器"""
    
    def __init__(self):
        self.topics = get_topics()
        logger.info(f"TopicFilter initialized with {len(self.topics)} topics")
    
    def list_topics(self) -> List[str]:
        """列出所有可用专题"""
        return self.topics
    
    def filter_by_topic(
        self,
        df: pd.DataFrame,
        topic: str,
        title_col: str = "标题",
        content_col: Optional[str] = None,
        match_content: bool = False
    ) -> pd.DataFrame:
        """
        根据专题关键词筛选新闻
        
        Args:
            df: 新闻数据DataFrame
            topic: 专题名称
            title_col: 标题列名
            content_col: 内容列名
            match_content: 是否同时匹配内容
        
        Returns:
            筛选后的DataFrame
        """
        if topic not in TOPIC_KEYWORDS:
            logger.warning(f"Unknown topic: {topic}")
            return pd.DataFrame()
        
        keywords = TOPIC_KEYWORDS[topic]
        pattern = '|'.join(keywords)
        
        try:
            title_mask = df[title_col].str.contains(pattern, case=False, na=False, regex=True)
            
            if match_content and content_col and content_col in df.columns:
                content_mask = df[content_col].str.contains(pattern, case=False, na=False, regex=True)
                mask = title_mask | content_mask
            else:
                mask = title_mask
            
            filtered_df = df[mask].copy()
            logger.info(f"Filtered {len(filtered_df)} news for topic: {topic}")
            return filtered_df
            
        except Exception as e:
            logger.error(f"Failed to filter news: {e}")
            return pd.DataFrame()
    
    def get_topic_urls(
        self,
        df: pd.DataFrame,
        topic: str,
        title_col: str = "标题",
        url_col: str = "链接",
        match_content: bool = False
    ) -> List[str]:
        """
        获取专题新闻的URL列表
        
        Args:
            df: 新闻数据DataFrame
            topic: 专题名称
            title_col: 标题列名
            url_col: URL列名
            match_content: 是否同时匹配内容
        
        Returns:
            URL列表
        """
        filtered = self.filter_by_topic(
            df, topic, title_col=title_col, match_content=match_content
        )
        if filtered.empty:
            return []
        if url_col not in filtered.columns:
            logger.warning(f"URL column '{url_col}' not found")
            return []
        return filtered[url_col].tolist()
    
    def filter_multiple_topics(
        self,
        df: pd.DataFrame,
        topics: List[str],
        title_col: str = "标题",
        match_content: bool = False
    ) -> Dict[str, pd.DataFrame]:
        """
        同时筛选多个专题的新闻
        
        Args:
            df: 新闻数据DataFrame
            topics: 专题名称列表
            title_col: 标题列名
            match_content: 是否同时匹配内容
        
        Returns:
            专题名称到筛选DataFrame的字典
        """
        result = {}
        for topic in topics:
            filtered = self.filter_by_topic(
                df, topic, title_col=title_col, match_content=match_content
            )
            if not filtered.empty:
                result[topic] = filtered
        return result
