# 专题新闻筛选功能 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在 FinScraper 中添加专题新闻筛选功能，支持按特定主题（如中东地缘局势、全国两会等）筛选新闻并返回URL链接

**Architecture:** 
- 创建新的专题筛选模块 `finscraper/filters/topic_filter.py`
- 扩展现有新闻 CLI 命令，添加 `topic` 和 `topics` 子命令
- 遵循现有架构模式，保持代码风格一致

**Tech Stack:** Python, Typer, akshare, pandas, pytest

---

## Task 1: 创建专题筛选模块

**Files:**
- Create: `finscraper/filters/__init__.py`
- Create: `finscraper/filters/topic_filter.py`
- Create: `finscraper/filters/topic_config.py`

**Step 1: 创建 filters 包的 __init__.py**

```python
"""Filters module for FinScraper."""
```

**Step 2: 创建专题配置文件 topic_config.py**

```python
"""
专题新闻关键词配置
定义不同专题的关键词列表
"""

TOPIC_KEYWORDS = {
    "中东地缘": [
        "中东", "以色列", "巴勒斯坦", "伊朗", "沙特", "海湾", "巴以冲突",
        "加沙", "黎巴嫩", "叙利亚", "也门", "胡塞", "哈马斯", "真主党",
        "哈梅内伊", "内塔尼亚胡", "耶路撒冷", "特拉维夫", "德黑兰"
    ],
    "全国两会": [
        "两会", "全国人大", "全国政协", "政府工作报告", "总理记者会",
        "代表委员", "人大会议", "政协会议", "立法", "议案", "提案",
        "十四五", "发展规划", "经济目标", "GDP目标", "民生"
    ],
    "美联储": [
        "美联储", "FOMC", "加息", "降息", "鲍威尔", "利率决议",
        "联邦基金利率", "量化宽松", "缩表", "通胀目标", "点阵图"
    ],
    "人工智能": [
        "人工智能", "AI", "ChatGPT", "大模型", "AIGC", "算力", "算法",
        "机器学习", "深度学习", "神经网络", "OpenAI", "百度", "阿里",
        "腾讯", "字节", "智谱", "月之暗面"
    ],
    "新能源": [
        "新能源", "光伏", "风电", "储能", "锂电池", "宁德时代", "比亚迪",
        "电动车", "特斯拉", "氢能", "充电桩", "碳中和", "碳达峰"
    ],
    "房地产": [
        "房地产", "房企", "房价", "楼市", "房贷", "限购", "土拍",
        "万科", "保利", "恒大", "碧桂园", "融创", "绿地"
    ]
}


def get_topics() -> list:
    """获取所有可用专题列表"""
    return list(TOPIC_KEYWORDS.keys())


def get_keywords(topic: str) -> list:
    """获取指定专题的关键词列表"""
    return TOPIC_KEYWORDS.get(topic, [])


def add_topic(topic: str, keywords: list) -> None:
    """添加或更新专题关键词"""
    TOPIC_KEYWORDS[topic] = keywords


def remove_topic(topic: str) -> bool:
    """移除专题"""
    if topic in TOPIC_KEYWORDS:
        del TOPIC_KEYWORDS[topic]
        return True
    return False
```

**Step 3: 创建专题筛选核心模块 topic_filter.py**

```python
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
            # 匹配标题
            title_mask = df[title_col].str.contains(pattern, case=False, na=False, regex=True)
            
            # 如果需要匹配内容
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
```

**Step 4: 更新 __init__.py 导出模块**

编辑 `finscraper/filters/__init__.py`：

```python
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
```

**Step 5: Commit**

```bash
git add finscraper/filters/__init__.py finscraper/filters/topic_filter.py finscraper/filters/topic_config.py
git commit -m "feat: add topic news filter module"
```

---

## Task 2: 扩展新闻 CLI 命令

**Files:**
- Modify: `finscraper/cli/commands/news.py`

**Step 1: 读取现有 news.py 文件**

先查看完整内容，然后进行修改。

**Step 2: 更新 import 并添加新的 CLI 命令**

在 `finscraper/cli/commands/news.py` 中添加：

```python
# 在文件顶部添加
from typing_extensions import Annotated
from finscraper.filters import TopicFilter, get_topics
import akshare as ak
```

在文件末尾添加新的命令：

```python
@news_app.command("topics")
def list_topics():
    """列出所有可用专题"""
    try:
        topics = get_topics()
        print_info("可用专题列表:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")
        print_success(f"共 {len(topics)} 个专题")
    except Exception as e:
        print_error(f"获取专题列表失败: {e}")
        raise typer.Exit(code=1)


@news_app.command("topic")
def topic_news(
    name: Annotated[
        str,
        typer.Option("--name", "-n", help="专题名称"),
    ],
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="输出格式 (table|csv|json|parquet|sqlite)"),
    ] = "table",
    output_path: Annotated[
        str,
        typer.Option("--output-path", "-p", help="输出文件路径"),
    ] = None,
    urls_only: Annotated[
        bool,
        typer.Option("--urls-only", "-u", help="仅输出URL列表"),
    ] = False,
    match_content: Annotated[
        bool,
        typer.Option("--match-content", "-c", help="同时匹配新闻内容"),
    ] = False,
):
    """获取指定专题的新闻"""
    try:
        print_info(f"正在获取专题新闻: {name}")
        
        # 获取新闻数据
        df = ak.stock_info_global_em()
        if df is None or df.empty:
            print_info("暂无新闻数据")
            return
        
        # 筛选专题新闻
        filter = TopicFilter()
        filtered_df = filter.filter_by_topic(
            df, 
            topic=name, 
            title_col="标题", 
            content_col="摘要" if match_content else None,
            match_content=match_content
        )
        
        if filtered_df is None or filtered_df.empty:
            print_info(f"专题 '{name}' 暂无相关新闻")
            return
        
        # 输出 URL 列表
        if urls_only:
            urls = filtered_df["链接"].tolist()
            print_success(f"找到 {len(urls)} 条相关新闻:")
            for i, url in enumerate(urls, 1):
                print(f"{i}. {url}")
            
            if output_path:
                with open(output_path, "w", encoding="utf-8") as f:
                    for url in urls:
                        f.write(f"{url}\n")
                print_success(f"URL列表已保存到: {output_path}")
            return
        
        # 输出完整新闻
        print_info(f"找到 {len(filtered_df)} 条相关新闻")
        
        if output == "table":
            output_data_str = output_data(filtered_df, format="table")
            typer.echo(output_data_str)
        else:
            print_info(f"使用 {output} 格式输出")
        
        if output_path:
            save_data(filtered_df, output_path, format=output)
            print_success(f"数据已保存到: {output_path}")
        
    except Exception as e:
        print_error(f"获取专题新闻失败: {e}")
        raise typer.Exit(code=1)
```

**Step 3: Commit**

```bash
git add finscraper/cli/commands/news.py
git commit -m "feat: add topic news CLI commands"
```

---

## Task 3: 创建测试文件

**Files:**
- Create: `tests/test_filters/test_topic_filter.py`

**Step 1: 创建测试文件**

```python
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
        # 测试中东地缘专题
        result = filter.filter_by_topic(sample_news, "中东地缘", title_col="标题")
        assert len(result) == 1
        assert "伊朗" in result.iloc[0]["标题"]
        
        # 测试美联储专题
        result = filter.filter_by_topic(sample_news, "美联储", title_col="标题")
        assert len(result) == 1
        assert "美联储" in result.iloc[0]["标题"]
        
        # 测试不存在的专题
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
```

**Step 2: 创建测试目录的 __init__.py**

```python
"""Tests for filters module."""
```

**Step 3: 运行测试验证**

```bash
pytest tests/test_filters/test_topic_filter.py -v
```

**Step 4: Commit**

```bash
git add tests/test_filters/__init__.py tests/test_filters/test_topic_filter.py
git commit -m "test: add topic filter tests"
```

---

## Task 4: 更新用户文档

**Files:**
- Modify: `docs/USER_GUIDE.md`

**Step 1: 在用户文档中添加专题新闻筛选部分**

在合适的位置添加：

```markdown
### 专题新闻筛选

FinScraper 支持按特定主题筛选新闻，帮助你快速获取关注领域的资讯。

#### 列出所有可用专题

```bash
finscraper news topics
```

#### 获取指定专题的新闻

```bash
# 获取中东地缘相关新闻
finscraper news topic --name "中东地缘"

# 仅输出 URL 列表
finscraper news topic --name "中东地缘" --urls-only

# 保存到文件
finscraper news topic --name "中东地缘" --output csv --output-path middle_east_news.csv

# 同时匹配新闻内容
finscraper news topic --name "中东地缘" --match-content
```

#### Python API 使用

```python
from finscraper.filters import TopicFilter
import akshare as ak

# 获取新闻数据
df = ak.stock_info_global_em()

# 创建筛选器
filter = TopicFilter()

# 列出可用专题
topics = filter.list_topics()
print(topics)  # ['中东地缘', '全国两会', '美联储', ...]

# 筛选专题新闻
filtered_df = filter.filter_by_topic(df, topic="中东地缘")

# 获取 URL 列表
urls = filter.get_topic_urls(df, topic="中东地缘")
```

#### 内置专题

- **中东地缘**: 中东地区相关新闻（以色列、巴勒斯坦、伊朗、沙特等）
- **全国两会**: 全国人大、政协相关新闻
- **美联储**: 美联储货币政策相关新闻
- **人工智能**: AI、大模型相关新闻
- **新能源**: 光伏、风电、电动车等相关新闻
- **房地产**: 房地产行业相关新闻
```

**Step 2: Commit**

```bash
git add docs/USER_GUIDE.md
git commit -m "docs: update user guide with topic filter"
```

---

## Task 5: 完整功能测试

**Files:**
- N/A (执行测试命令)

**Step 1: 运行 CLI 命令测试**

```bash
# 测试列出专题
finscraper news topics

# 测试获取专题新闻
finscraper news topic --name "中东地缘"

# 测试仅输出 URL
finscraper news topic --name "中东地缘" --urls-only
```

**Step 2: 运行完整测试套件**

```bash
pytest tests/test_filters/ -v
```

---

## 执行选择

计划已保存到 `docs/plans/2026-03-08-topic-news-filter.md`。两种执行选项：

**1. Subagent-Driven (本会话)** - 我将为每个任务分配独立的子代理，在任务之间进行代码审查，快速迭代

**2. Parallel Session (独立会话)** - 在新会话中使用 executing-plans 技能批量执行，带检查点

你选择哪种方式？
