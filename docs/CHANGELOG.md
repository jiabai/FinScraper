# 变更日志 (Changelog)

本文档记录 FinScraper 项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### 计划中
- 实时数据推送功能
- Web 界面
- 更多数据源支持

---

## [1.0.1] - 2026-03-08

### 新增
- 添加专题新闻筛选功能 (`news topic` 命令)
- 支持按关键词筛选特定主题新闻
- 内置多个常用专题：中东地缘、全国两会、美联储、人工智能、新能源、房地产

### 改进
- 优化日志输出格式
- 改进错误提示信息

---

## [1.0.0] - 2026-03-07

### 新增

#### 核心功能
- A 股指数数据获取
  - 实时行情数据
  - 历史数据（日/周/月线）
  - 指数列表查询
- 北向资金数据获取
  - 日级别数据
  - 日内分时数据
- 板块数据获取
  - 板块列表
  - 板块实时行情
  - 板块成分股
- 大宗商品数据获取
  - 商品列表
  - 实时行情
  - 历史数据
- 资金流向数据获取
  - 个股资金流向
  - 板块资金流向
  - 市场资金流向
- 重要新闻数据获取
  - 全球财经新闻
  - A 股公告快讯
  - 个股相关新闻

#### CLI 工具
- 完整的命令行工具 (`finscraper`)
- 支持多种输出格式（CSV、JSON、Parquet、SQLite）
- 全局选项支持（版本、帮助、详细日志、安静模式）
- 各数据类型的子命令

#### Python API
- 简洁的 Python API
- 类型安全的接口
- 完整的类型注解

#### 存储功能
- CSV 存储
- JSON 存储
- Parquet 存储
- SQLite 存储

#### 其他功能
- 自动重试机制
- 完善的日志系统
- 配置文件支持
- 环境变量配置

### 文档
- 项目规格说明 (PROJECT_SPEC.md)
- 用户指南 (USER_GUIDE.md)
- 编码规范 (CODING_STANDARDS.md)
- 发布说明 (RELEASE_NOTES_v1.0.0.md)

### 测试
- 单元测试覆盖
- 集成测试
- 测试覆盖率 > 80%

---

## [0.7.0] - 2026-03-08

### 新增
- Phase 7 完善与优化
- 改进错误处理
- 优化代码结构

### 修复
- 修复 EM 接口数据解析问题
- 修复日志配置问题

---

## [0.6.0] - 2026-03-07

### 新增
- 完整的数据获取器实现
- 所有 6 种数据类型的 Fetcher
- 数据清洗和转换功能

---

## [0.5.0] - 2026-03-07

### 新增
- 基础数据获取器
- IndexFetcher 基础实现
- NorthFlowFetcher 基础实现

---

## [0.4.0] - 2026-03-07

### 新增
- CLI 命令框架
- 各数据类型的命令实现
- 命令行参数解析

---

## [0.3.0] - 2026-03-07

### 新增
- CLI 框架搭建
- Typer 集成
- 基础命令结构

---

## [0.2.0] - 2026-03-07

### 新增
- 核心框架实现
- AkShareClient 封装
- DataCleaner 数据清洗
- 日志系统
- 重试机制
- 异常定义

---

## [0.1.0] - 2026-03-07

### 新增
- 项目初始化
- 基础项目结构
- 配置文件
- 依赖管理

---

## 版本说明

### 版本号格式

遵循语义化版本规范：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的问题修复

### 变更类型

- **新增 (Added)**: 新功能
- **变更 (Changed)**: 现有功能的变更
- **弃用 (Deprecated)**: 即将移除的功能
- **移除 (Removed)**: 已移除的功能
- **修复 (Fixed)**: Bug 修复
- **安全 (Security)**: 安全相关的修复

---

[Unreleased]: https://github.com/jiabai/FinScraper/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/jiabai/FinScraper/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jiabai/FinScraper/releases/tag/v1.0.0
[0.7.0]: https://github.com/jiabai/FinScraper/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/jiabai/FinScraper/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/jiabai/FinScraper/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/jiabai/FinScraper/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/jiabai/FinScraper/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/jiabai/FinScraper/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/jiabai/FinScraper/releases/tag/v0.1.0
