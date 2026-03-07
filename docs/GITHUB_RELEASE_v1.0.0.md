# FinScraper v1.0.0

## 🎉 正式发布 v1.0.0

FinScraper 是一个基于 akshare 的专业金融数据获取工具，提供 A 股指数、北向资金、板块数据、大宗商品、资金流向和重要新闻等数据。

---

## ✨ 主要功能

| 功能 | 说明 |
|------|------|
| A 股指数 | 实时行情、历史数据 |
| 北向资金 | 日数据、日内数据 |
| 板块数据 | 板块列表、实时行情、成分股 |
| 大宗商品 | 商品实时行情、历史数据 |
| 资金流向 | 个股、板块和市场资金流向 |
| 重要新闻 | 全球新闻、新闻提醒、个股新闻 |

---

## 🚀 快速开始

### 安装

```bash
pip install -e .
```

### CLI 使用示例

```bash
# 获取指数实时行情
finscraper index spot

# 获取指数历史数据
finscraper index history 000001 --start-date 20240101

# 获取北向资金日数据
finscraper north-flow daily

# 获取板块实时行情
finscraper sector spot

# 保存数据到文件
finscraper index spot --output-path data/index_spot.csv
```

### Python API 使用

```python
from finscraper.fetchers import IndexFetcher

fetcher = IndexFetcher()
data = fetcher.fetch_spot()
print(data)
```

---

## 📦 安装和使用

详细文档请参考 [README.md](https://github.com/jiabai/FinScraper/blob/v1.0.0/README.md)

---

## 📋 里程碑

- ✅ Phase 1-7 全部完成
- ✅ 所有测试通过
- ✅ 完整的文档和示例

---

**FinScraper v1.0.0 正式发布！** 🚀
