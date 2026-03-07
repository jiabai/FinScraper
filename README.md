# FinScraper

金融数据爬虫项目

## 项目结构

```
FinScraper/
├── finscraper/          # 主代码包
│   ├── spiders/         # 爬虫模块
│   ├── utils/           # 工具函数
│   ├── models/          # 数据模型
│   └── config/          # 配置文件
├── tests/               # 测试代码
├── data/                # 数据文件（不提交到Git）
├── docs/                # 文档
├── scripts/             # 脚本文件
├── pyproject.toml       # 项目配置
└── README.md            # 项目说明
```

## 安装依赖

```bash
pip install -e .[dev]
```

## 代码规范

### 代码格式化

```bash
# 格式化代码
black .
isort .
```

### 代码检查

```bash
# 运行所有检查
pylint finscraper/
flake8 finscraper/
mypy finscraper/
```

### 运行测试

```bash
pytest
```

## 开发流程

1. 创建新分支进行开发
2. 编写代码和测试
3. 运行格式化和检查工具
4. 提交代码
