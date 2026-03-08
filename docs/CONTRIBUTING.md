# 贡献指南

感谢您对 FinScraper 项目的关注！本文档将帮助您了解如何为项目做出贡献。

---

## 目录

1. [行为准则](#行为准则)
2. [如何贡献](#如何贡献)
3. [开发环境设置](#开发环境设置)
4. [代码规范](#代码规范)
5. [提交规范](#提交规范)
6. [Pull Request 流程](#pull-request-流程)
7. [报告问题](#报告问题)
8. [功能建议](#功能建议)

---

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺让参与项目的每个人都能享受到无骚扰的体验，无论其年龄、体型、残疾、种族、性别认同和表达、经验水平、教育程度、社会经济地位、国籍、外貌、种族、宗教或性取向如何。

### 我们的标准

积极行为的示例包括：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

---

## 如何贡献

### 贡献方式

您可以通过以下方式为 FinScraper 做出贡献：

1. **报告 Bug** - 提交详细的问题报告
2. **建议功能** - 提出新功能想法
3. **改进文档** - 修复错别字、改进说明
4. **编写代码** - 修复 Bug 或实现新功能
5. **代码审查** - 审查 Pull Request

### 贡献流程

```
1. Fork 项目
   ↓
2. 创建特性分支 (git checkout -b feature/amazing-feature)
   ↓
3. 进行更改
   ↓
4. 运行测试和代码检查
   ↓
5. 提交更改 (git commit -m 'feat: add amazing feature')
   ↓
6. 推送到分支 (git push origin feature/amazing-feature)
   ↓
7. 创建 Pull Request
```

---

## 开发环境设置

### 系统要求

- Python 3.10+
- Git
- pip 或 uv

### 设置步骤

```bash
# 1. Fork 并克隆项目
git clone https://github.com/YOUR_USERNAME/FinScraper.git
cd FinScraper

# 2. 创建虚拟环境
python -m venv venv

# Windows 激活
venv\Scripts\activate

# macOS/Linux 激活
source venv/bin/activate

# 3. 安装开发依赖
pip install -e ".[dev]"

# 4. 验证安装
finscraper --version
pytest --version
```

### 项目结构

```
FinScraper/
├── finscraper/          # 主代码包
│   ├── cli/             # CLI 命令
│   ├── core/            # 核心模块
│   ├── fetchers/        # 数据获取器
│   ├── filters/         # 数据筛选器
│   ├── models/          # 数据模型
│   ├── storage/         # 存储模块
│   └── config/          # 配置
├── tests/               # 测试代码
├── docs/                # 文档
├── scripts/             # 脚本
└── pyproject.toml       # 项目配置
```

---

## 代码规范

### 代码风格

我们使用以下工具确保代码质量：

| 工具 | 用途 | 配置文件 |
|-----|------|---------|
| Black | 代码格式化 | pyproject.toml |
| isort | 导入排序 | pyproject.toml |
| Pylint | 代码检查 | pyproject.toml |
| Flake8 | 代码检查 | pyproject.toml |
| mypy | 类型检查 | pyproject.toml |

### 格式化代码

```bash
# 格式化代码
black .

# 排序导入
isort .

# 或同时运行
black . && isort .
```

### 代码检查

```bash
# 运行所有检查
pylint finscraper/
flake8 finscraper/
mypy finscraper/
```

### 命名规范

| 类型 | 规范 | 示例 |
|-----|------|------|
| 模块 | 小写，下划线分隔 | `data_parser.py` |
| 类 | 大驼峰 | `IndexFetcher` |
| 函数 | 小写，下划线分隔 | `fetch_spot_data` |
| 变量 | 小写，下划线分隔 | `stock_price` |
| 常量 | 大写，下划线分隔 | `MAX_RETRIES` |

### 类型注解

所有公共函数必须添加类型注解：

```python
from typing import Optional
import pandas as pd

def fetch_data(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """获取数据"""
    pass
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def fetch_index_spot(symbols: Optional[list[str]] = None) -> pd.DataFrame:
    """获取指数实时行情数据。

    Args:
        symbols: 指数代码列表，如 ['sh000001', 'sz399001']。
            如果为 None，则获取所有指数。

    Returns:
        包含指数实时行情的 DataFrame，包含以下列：
            - symbol: 指数代码
            - name: 指数名称
            - price: 最新价
            - change: 涨跌额
            - change_percent: 涨跌幅

    Raises:
        NetworkError: 网络请求失败时抛出。
        DataParseError: 数据解析失败时抛出。

    Example:
        >>> fetcher = IndexFetcher()
        >>> data = fetcher.fetch_spot(['sh000001'])
        >>> print(data.head())
    """
    pass
```

### 测试规范

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_fetchers/test_index.py

# 运行特定测试
pytest tests/test_fetchers/test_index.py::TestIndexFetcher::test_fetch_spot

# 查看测试覆盖率
pytest --cov=finscraper --cov-report=html
```

测试命名规范：

```python
class TestIndexFetcher:
    """IndexFetcher 测试类"""

    def test_fetch_spot_success(self):
        """测试成功获取实时行情"""
        pass

    def test_fetch_spot_with_symbols(self):
        """测试使用指定代码获取行情"""
        pass

    def test_fetch_spot_network_error(self):
        """测试网络错误处理"""
        pass
```

---

## 提交规范

### 提交信息格式

我们遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型 (type)

| 类型 | 说明 | 示例 |
|-----|------|------|
| feat | 新功能 | feat(index): add support for real-time data |
| fix | Bug 修复 | fix(north-flow): fix date parsing error |
| docs | 文档更新 | docs: update installation guide |
| style | 代码格式（不影响功能） | style: format code with black |
| refactor | 重构 | refactor(storage): simplify save logic |
| test | 测试相关 | test(index): add unit tests for fetch_spot |
| chore | 构建/工具相关 | chore: update dependencies |

### 范围 (scope)

常用的范围：

- `index` - 指数相关
- `north-flow` - 北向资金相关
- `sector` - 板块相关
- `commodity` - 大宗商品相关
- `money-flow` - 资金流向相关
- `news` - 新闻相关
- `cli` - CLI 相关
- `storage` - 存储相关
- `core` - 核心模块

### 提交示例

```bash
# 新功能
git commit -m "feat(index): add support for index history data"

# Bug 修复
git commit -m "fix(north-flow): fix intraday data parsing error"

# 文档更新
git commit -m "docs: add API reference documentation"

# 多行提交信息
git commit -m "feat(sector): add sector constituent stocks fetcher

- Implement fetch_stocks method
- Add unit tests
- Update documentation

Closes #123"
```

---

## Pull Request 流程

### 创建 PR 前的检查清单

- [ ] 代码通过所有测试
- [ ] 代码通过 lint 检查
- [ ] 代码已格式化
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 提交信息符合规范

### PR 标题格式

PR 标题应遵循与提交信息相同的格式：

```
feat(index): add support for real-time data streaming
```

### PR 描述模板

```markdown
## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 重构
- [ ] 文档更新
- [ ] 其他

## 变更说明
[描述本次变更的内容和原因]

## 相关 Issue
Closes #xxx

## 测试
- [ ] 已添加单元测试
- [ ] 已添加集成测试
- [ ] 已手动测试

## 截图（如适用）
[添加截图]

## 其他说明
[其他需要说明的内容]
```

### 代码审查

所有 PR 都需要至少一位维护者审查后才能合并。审查时会关注：

1. **代码质量** - 是否符合编码规范
2. **测试覆盖** - 是否有足够的测试
3. **文档完整** - 是否更新了相关文档
4. **向后兼容** - 是否破坏了现有 API

---

## 报告问题

### Bug 报告模板

```markdown
**Bug 描述**
[清晰简洁地描述 Bug]

**复现步骤**
1. 运行命令 `finscraper index spot`
2. 查看输出
3. 发现错误

**期望行为**
[描述您期望发生什么]

**实际行为**
[描述实际发生了什么]

**环境信息**
- OS: [如 Windows 11]
- Python: [如 3.11.0]
- FinScraper: [如 1.0.0]

**日志输出**
```
[粘贴相关日志]
```

**其他信息**
[其他有助于解决问题的信息]
```

---

## 功能建议

### 功能建议模板

```markdown
**功能描述**
[清晰描述您希望添加的功能]

**使用场景**
[描述这个功能解决什么问题]

**建议实现**
[可选：描述您认为应该如何实现]

**替代方案**
[可选：描述您考虑过的其他方案]

**其他信息**
[其他相关信息]
```

---

## 获取帮助

如果您有任何问题，可以通过以下方式获取帮助：

1. 查看 [文档](./USER_GUIDE.md)
2. 查看 [FAQ](./FAQ.md)
3. 提交 [Issue](https://github.com/jiabai/FinScraper/issues)

---

再次感谢您对 FinScraper 的贡献！🎉
