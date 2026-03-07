# Vibe Coding 文档模板

## 项目信息
- **项目名称**: [项目名称]
- **创建日期**: [YYYY-MM-DD]
- **负责人**: [负责人姓名]
- **版本**: v1.0

---

## 1. PRD (产品需求文档)

### 1.1 项目背景
[描述项目的背景和动机，为什么要做这个项目]

### 1.2 目标用户
[描述目标用户群体]

### 1.3 核心需求

| 需求编号 | 需求名称 | 需求描述 | 优先级 |
|---------|---------|---------|--------|
| REQ-001 | [需求名称] | [详细描述] | P0/P1/P2 |
| REQ-002 | [需求名称] | [详细描述] | P0/P1/P2 |

### 1.4 功能范围
- **包含**: [列出包含的功能]
- **不包含**: [列出不包含的功能]

### 1.5 成功指标
- [指标1]
- [指标2]

---

## 2. 技术栈

### 2.1 核心技术选型

| 类别 | 技术选型 | 版本 | 选型理由 |
|-----|---------|------|---------|
| 编程语言 | [Python/TypeScript/...] | [版本号] | [理由] |
| Web框架 | [FastAPI/Flask/Express/...] | [版本号] | [理由] |
| 数据库 | [PostgreSQL/MySQL/Redis/...] | [版本号] | [理由] |
| ORM/ODM | [SQLAlchemy/Prisma/Mongoose/...] | [版本号] | [理由] |
| 数据验证 | [Pydantic/Zod/...] | [版本号] | [理由] |
| 测试框架 | [Pytest/Jest/...] | [版本号] | [理由] |
| 代码格式化 | [Black/Prettier/...] | [版本号] | [理由] |
| 代码检查 | [Pylint/ESLint/...] | [版本号] | [理由] |
| 类型检查 | [Mypy/TypeScript/...] | [版本号] | [理由] |

### 2.2 开发工具
- IDE: [VS Code/PyCharm/...]
- 版本控制: Git
- 虚拟环境: [venv/conda/npm/...]
- 任务运行: [Makefile/npm scripts/...]

### 2.3 依赖列表

#### 生产依赖
```toml
# pyproject.toml / package.json 示例
```

#### 开发依赖
```toml
# 开发工具依赖
```

---

## 3. 架构设计

### 3.1 系统架构图

```
[架构图 - 使用 Mermaid 或文字描述]
```

### 3.2 目录结构

```
project-root/
├── src/
│   ├── api/              # API 层
│   │   ├── routes/       # 路由定义
│   │   └── schemas/      # 请求/响应模式
│   ├── core/             # 核心业务逻辑
│   │   ├── services/     # 服务层
│   │   └── models/       # 数据模型
│   ├── infrastructure/   # 基础设施
│   │   ├── database/     # 数据库
│   │   └── external/     # 外部服务
│   └── utils/            # 工具函数
├── tests/                # 测试
│   ├── unit/             # 单元测试
│   └── integration/      # 集成测试
├── docs/                 # 文档
├── scripts/              # 脚本
└── config/               # 配置
```

### 3.3 分层架构

#### 3.3.1 API 层
- 职责: 处理 HTTP 请求/响应
- 包含: 路由、请求验证、响应序列化
- 示例:
  ```python
  # src/api/routes/stock.py
  from fastapi import APIRouter
  from src.api.schemas.stock import StockResponse
  from src.core.services.stock_service import StockService

  router = APIRouter()

  @router.get("/stock/{symbol}", response_model=StockResponse)
  async def get_stock(symbol: str):
      return await StockService.get_stock(symbol)
  ```

#### 3.3.2 服务层
- 职责: 业务逻辑实现
- 包含: 业务规则、流程编排
- 示例:
  ```python
  # src/core/services/stock_service.py
  from src.core.models.stock import Stock
  from src.infrastructure.database.repo import StockRepository

  class StockService:
      @staticmethod
      async def get_stock(symbol: str) -> Stock:
          return await StockRepository.get_by_symbol(symbol)
  ```

#### 3.3.3 数据访问层
- 职责: 数据持久化
- 包含: Repository 模式、数据库操作
- 示例:
  ```python
  # src/infrastructure/database/repo.py
  from sqlalchemy.ext.asyncio import AsyncSession
  from src.core.models.stock import Stock

  class StockRepository:
      @staticmethod
      async def get_by_symbol(session: AsyncSession, symbol: str) -> Stock:
          pass
  ```

### 3.4 数据模型设计

#### 3.4.1 核心实体
```python
# src/core/models/stock.py
from pydantic import BaseModel
from datetime import datetime

class Stock(BaseModel):
    id: int
    symbol: str
    name: str
    price: float
    updated_at: datetime
```

#### 3.4.2 数据库 Schema
```sql
-- migrations/001_create_stock_table.sql
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### 3.5 API 设计

#### 3.5.1 端点列表

| 方法 | 路径 | 描述 | 请求体 | 响应 |
|-----|------|------|--------|------|
| GET | `/api/stock/{symbol}` | 获取股票信息 | - | `StockResponse` |
| POST | `/api/stock` | 创建股票 | `StockCreate` | `StockResponse` |

#### 3.5.2 请求/响应示例

**请求**:
```http
GET /api/stock/AAPL
```

**响应**:
```json
{
  "id": 1,
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "price": 175.50,
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### 3.6 关键技术决策

| 决策项 | 决策 | 备选方案 | 决策理由 |
|-------|------|---------|---------|
| [决策项1] | [决策] | [备选] | [理由] |
| [决策项2] | [决策] | [备选] | [理由] |

---

## 4. 实施计划

### 4.1 里程碑

| 里程碑 | 日期 | 交付物 |
|-------|------|--------|
| M1: 项目初始化 | [日期] | 项目骨架、配置 |
| M2: 核心功能 | [日期] | 核心业务逻辑 |
| M3: API 完成 | [日期] | API 接口 |
| M4: 测试覆盖 | [日期] | 测试代码 |
| M5: 发布上线 | [日期] | 生产部署 |

### 4.2 任务分解

#### Phase 1: 项目初始化
- [ ] 创建项目结构
- [ ] 配置开发环境
- [ ] 设置 CI/CD
- [ ] 编写基础文档

#### Phase 2: 核心功能
- [ ] 实现数据模型
- [ ] 实现 Repository 层
- [ ] 实现 Service 层
- [ ] 编写单元测试

#### Phase 3: API 层
- [ ] 实现 API 路由
- [ ] 实现请求验证
- [ ] 实现错误处理
- [ ] 编写集成测试

#### Phase 4: 完善与优化
- [ ] 性能优化
- [ ] 安全加固
- [ ] 文档完善
- [ ] 代码审查

---

## 5. 风险与应对

| 风险 | 影响 | 概率 | 应对措施 |
|-----|------|------|---------|
| [风险1] | 高/中/低 | 高/中/低 | [措施] |
| [风险2] | 高/中/低 | 高/中/低 | [措施] |

---

## 6. 附录

### 6.1 参考资料
- [链接1]
- [链接2]

### 6.2 术语表
- **术语1**: [解释]
- **术语2**: [解释]

### 6.3 变更记录

| 版本 | 日期 | 修改人 | 修改内容 |
|-----|------|-------|---------|
| v1.0 | [日期] | [姓名] | 初始版本 |
