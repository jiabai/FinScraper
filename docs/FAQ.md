# 常见问题解答 (FAQ)

本文档收集了 FinScraper 使用过程中的常见问题及其解决方案。

---

## 目录

1. [安装问题](#安装问题)
2. [使用问题](#使用问题)
3. [数据获取问题](#数据获取问题)
4. [存储问题](#存储问题)
5. [性能问题](#性能问题)
6. [错误排查](#错误排查)

---

## 安装问题

### Q: 安装时出现依赖冲突怎么办？

**A**: 建议使用虚拟环境安装：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装
pip install -e .
```

### Q: 安装 akshare 时出错？

**A**: akshare 依赖较多，建议：

1. 确保 Python 版本 >= 3.10
2. 升级 pip：`pip install --upgrade pip`
3. 如果网络问题，使用国内镜像：
   ```bash
   pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

### Q: Windows 上安装后命令找不到？

**A**: 确保：

1. 虚拟环境已激活
2. 使用 `pip install -e .` 安装
3. 检查 PATH 环境变量是否包含 Python Scripts 目录

---

## 使用问题

### Q: 如何查看所有可用命令？

**A**: 使用 `--help` 参数：

```bash
# 查看主命令帮助
finscraper --help

# 查看子命令帮助
finscraper index --help
finscraper index spot --help
```

### Q: 如何获取特定指数的数据？

**A**: 使用 `--symbols` 参数：

```bash
# 获取上证指数和深证成指
finscraper index spot --symbols sh000001,sz399001

# 简写
finscraper index spot -s sh000001
```

### Q: 如何获取历史数据？

**A**: 使用 `history` 子命令：

```bash
# 获取上证指数历史数据
finscraper index history 000001

# 指定日期范围
finscraper index history 000001 --start-date 20240101 --end-date 20241231

# 获取周线数据
finscraper index history 000001 --period weekly
```

### Q: 如何保存数据到文件？

**A**: 使用 `--output-path` 或 `-p` 参数：

```bash
# 保存为 CSV（默认）
finscraper index spot -p data/indices.csv

# 指定格式
finscraper index spot -o json -p data/indices.json
finscraper index spot -o parquet -p data/indices.parquet
finscraper index spot -o sqlite -p data/finance.db
```

### Q: 如何开启详细日志？

**A**: 使用 `-v` 参数：

```bash
# INFO 级别
finscraper -v index spot

# DEBUG 级别
finscraper -vv index spot

# 安静模式（只显示错误）
finscraper -q index spot
```

### Q: 如何使用配置文件？

**A**: 创建 `config.yaml` 文件：

```yaml
request_timeout: 60
max_retries: 5
log_level: "DEBUG"
data_dir: "my_data"
```

然后使用 `-c` 参数：

```bash
finscraper -c config.yaml index spot
```

---

## 数据获取问题

### Q: 获取数据时超时怎么办？

**A**: 可能的原因和解决方案：

1. **网络问题**：检查网络连接
2. **服务器响应慢**：增加超时时间
   ```bash
   export FINSCRAPER_REQUEST_TIMEOUT=60
   ```
3. **请求频率过高**：稍后重试

### Q: 数据获取失败，提示网络错误？

**A**: 检查以下几点：

1. 网络连接是否正常
2. 是否需要代理（公司网络）
3. 数据源服务器是否可用

如果需要代理：

```python
import os
os.environ['HTTP_PROXY'] = 'http://proxy:port'
os.environ['HTTPS_PROXY'] = 'http://proxy:port'
```

### Q: 获取的数据为空怎么办？

**A**: 可能的原因：

1. **非交易时间**：股市数据在交易时间更新
2. **日期范围无效**：检查日期参数
3. **代码不存在**：确认代码是否正确

```bash
# 先列出可用指数
finscraper index list
```

### Q: 北向资金数据为什么有时获取不到？

**A**: 北向资金数据特点：

- 日数据：交易日收盘后更新
- 日内数据：交易时间实时更新
- 节假日无数据

### Q: 如何获取特定板块的成分股？

**A**: 使用 `sector stocks` 命令：

```bash
# 先获取板块列表
finscraper sector spot

# 找到板块代码后获取成分股
finscraper sector stocks BK0428
```

### Q: 新闻数据如何按专题筛选？

**A**: 使用 `news topic` 命令：

```bash
# 列出所有专题
finscraper news topics

# 获取特定专题新闻
finscraper news topic --name "中东地缘"

# 只获取 URL
finscraper news topic --name "中东地缘" --urls-only
```

---

## 存储问题

### Q: CSV 文件中文乱码怎么办？

**A**: FinScraper 默认使用 UTF-8-BOM 编码，Excel 应该能正确显示。如果仍有问题：

1. 用记事本打开，另存为 UTF-8 编码
2. 或使用 Python 读取：
   ```python
   import pandas as pd
   df = pd.read_csv('data.csv', encoding='utf-8-sig')
   ```

### Q: Parquet 文件如何读取？

**A**: 使用 pandas：

```python
import pandas as pd

df = pd.read_parquet('data.parquet')
```

### Q: SQLite 数据库如何查询？

**A**: 使用 sqlite3 或 pandas：

```python
import sqlite3
import pandas as pd

# 方法1：sqlite3
conn = sqlite3.connect('data/finance.db')
cursor = conn.execute("SELECT * FROM index_spot")
for row in cursor:
    print(row)

# 方法2：pandas
df = pd.read_sql("SELECT * FROM index_spot", conn)
conn.close()
```

### Q: 如何追加数据到已有文件？

**A**: 目前需要手动处理：

```python
import pandas as pd

# 读取已有数据
existing = pd.read_csv('data.csv')

# 获取新数据
new_data = fetcher.fetch_spot()

# 合并
combined = pd.concat([existing, new_data]).drop_duplicates()

# 保存
combined.to_csv('data.csv', index=False, encoding='utf-8-sig')
```

---

## 性能问题

### Q: 获取大量数据很慢怎么办？

**A**: 优化建议：

1. **使用 Parquet 格式**：大数据量时更高效
   ```bash
   finscraper index spot -o parquet -p data/indices.parquet
   ```

2. **批量获取**：避免频繁请求

3. **减少日志输出**：使用安静模式
   ```bash
   finscraper -q index spot
   ```

### Q: 如何实现定时自动获取？

**A**: 使用系统定时任务：

**Windows (任务计划程序)**:
```batch
:: create_task.bat
schtasks /create /tn "FinScraper" /tr "python D:\FinScraper\scripts\fetch_all.py" /sc daily /st 09:30
```

**Linux/macOS (cron)**:
```bash
# 编辑 crontab
crontab -e

# 添加任务（每天 9:30 执行）
30 9 * * * cd /path/to/FinScraper && python scripts/fetch_all.py
```

**Python (schedule 库)**:
```python
import schedule
import time
from finscraper.fetchers import IndexFetcher
from finscraper.storage import CSVStorage

def job():
    fetcher = IndexFetcher()
    storage = CSVStorage()
    data = fetcher.fetch_spot()
    storage.save(data, f"data/index_{time.strftime('%Y%m%d')}.csv")

schedule.every().day.at("09:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Q: 内存占用过高怎么办？

**A**: 建议：

1. 分批获取数据
2. 使用 Parquet 格式（内存效率更高）
3. 及时释放不需要的数据：
   ```python
   # 处理完数据后
   del large_dataframe
   import gc
   gc.collect()
   ```

---

## 错误排查

### Q: 出现 "ModuleNotFoundError" 错误？

**A**: 检查：

1. 虚拟环境是否激活
2. 是否正确安装：`pip install -e .`
3. Python 路径是否正确

### Q: 出现 "NetworkError" 错误？

**A**: 排查步骤：

1. 检查网络连接
2. 尝试访问数据源网站
3. 检查是否需要代理
4. 增加重试次数：
   ```bash
   export FINSCRAPER_MAX_RETRIES=5
   ```

### Q: 出现 "DataParseError" 错误？

**A**: 可能原因：

1. 数据源格式变化
2. 网络传输数据不完整
3. 数据源返回错误信息

解决方案：

1. 更新到最新版本
2. 开启详细日志查看详情：
   ```bash
   finscraper -vv index spot
   ```

### Q: 出现 "PermissionError" 错误？

**A**: 检查：

1. 文件是否被其他程序占用
2. 是否有写入权限
3. 路径是否存在

```bash
# 确保目录存在
mkdir -p data

# 检查权限
ls -la data/
```

### Q: 如何报告 Bug？

**A**: 请提供以下信息：

1. 操作系统和版本
2. Python 版本
3. FinScraper 版本
4. 完整的错误信息
5. 复现步骤

提交 Issue：https://github.com/jiabai/FinScraper/issues

---

## 其他问题

### Q: FinScraper 支持哪些数据源？

**A**: 目前支持：

| 数据类型 | 数据源 |
|---------|--------|
| A 股指数 | 新浪财经、东方财富 |
| 北向资金 | 东方财富 |
| 板块数据 | 东方财富 |
| 大宗商品 | 东方财富 |
| 资金流向 | 东方财富 |
| 重要新闻 | 东方财富 |

### Q: 数据更新频率是多少？

**A**:

| 数据类型 | 更新频率 |
|---------|---------|
| 指数实时行情 | 交易时间实时 |
| 指数历史数据 | 日更新 |
| 北向资金日数据 | 交易日收盘后 |
| 北向资金日内 | 交易时间实时 |
| 板块数据 | 交易时间实时 |
| 新闻数据 | 实时更新 |

### Q: 可以用于商业用途吗？

**A**: FinScraper 使用 MIT 许可证，可以自由使用。但请注意：

1. 数据源（akshare）的使用条款
2. 数据源网站的使用协议
3. 获取的数据版权归属

### Q: 如何获取更多帮助？

**A**: 

1. 查看 [用户指南](./USER_GUIDE.md)
2. 查看 [API 参考](./API_REFERENCE.md)
3. 提交 [Issue](https://github.com/jiabai/FinScraper/issues)

---

## 没有找到答案？

如果您的问题没有在这里找到答案，欢迎：

1. 提交 [Issue](https://github.com/jiabai/FinScraper/issues)
2. 查阅 [文档](./USER_GUIDE.md)
3. 查看 [源代码](https://github.com/jiabai/FinScraper)
