# 编码规范

## 目录结构规范

```
finscraper/
├── spiders/          # 爬虫实现
│   ├── base.py       # 爬虫基类
│   └── *.py          # 具体爬虫
├── utils/            # 工具函数
│   ├── requests.py   # 请求相关工具
│   ├── parser.py     # 解析相关工具
│   └── storage.py    # 存储相关工具
├── models/           # 数据模型
│   └── schemas.py    # Pydantic模型
└── config/           # 配置
    └── settings.py   # 配置管理
```

## 代码风格

### 命名规范

- 模块名：小写，下划线分隔（`data_parser.py`）
- 类名：大驼峰（`FinancialDataSpider`）
- 函数名：小写，下划线分隔（`fetch_stock_data`）
- 变量名：小写，下划线分隔（`stock_price`）
- 常量：大写，下划线分隔（`MAX_RETRIES`）

### 类型注解

所有函数必须添加类型注解：

```python
from typing import List, Optional
from datetime import datetime

def fetch_stock_data(symbol: str, start_date: Optional[datetime] = None) -> List[dict]:
    pass
```

### 文档字符串

使用Google风格的文档字符串：

```python
def fetch_stock_data(symbol: str, start_date: Optional[datetime] = None) -> List[dict]:
    """获取股票数据

    Args:
        symbol: 股票代码
        start_date: 开始日期，默认为None

    Returns:
        股票数据列表

    Raises:
        NetworkError: 网络请求失败
    """
    pass
```

## Git提交规范

提交信息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

示例：

```
feat(spiders): 添加股票数据爬虫

- 实现东方财富网股票数据抓取
- 添加数据验证逻辑
- 支持增量更新
```
