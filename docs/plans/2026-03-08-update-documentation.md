# 文档更新计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 更新 PROJECT_SPEC.md 文档，使其与当前代码实现保持一致

**Architecture:** 仅修改 PROJECT_SPEC.md 文件，更新 API 引用、CLI 命令结构和数据源说明

**Tech Stack:** Markdown

---

## Task 1: 更新 API 引用

**Files:**
- Modify: `d:\Code\FinScraper\docs\PROJECT_SPEC.md`

**Step 1: 更新 A 股指数 API 引用**

查找并替换：
- `ak.index_zh_a_spot_em()` → `ak.stock_zh_index_spot_sina()`
- 更新相关说明，说明数据源已从东方财富改为新浪财经

**Step 2: 更新北向资金 API 引用**

查找并替换：
- `ak.stock_em_hsgt_north_net_flow_in_em()` → `ak.stock_hsgt_fund_flow_summary_em()`（日数据）
- 添加 `ak.stock_hsgt_fund_min_em()`（日内数据）说明

**Step 3: 更新板块 API 引用**

查找并替换：
- `ak.stock_board_industry_name_em()` 等 → `ak.stock_sector_spot()`
- 更新说明，说明只保留实时行情命令

**Step 4: 保存文件**

---

## Task 2: 更新 CLI 命令结构

**Files:**
- Modify: `d:\Code\FinScraper\docs\PROJECT_SPEC.md`

**Step 1: 更新板块命令结构**

查找并修改：
- 移除 `sector list` 和 `sector stocks` 命令
- 只保留 `sector spot` 命令
- 更新命令说明

**Step 2: 保存文件**

---

## Task 3: 更新数据源说明

**Files:**
- Modify: `d:\Code\FinScraper\docs\PROJECT_SPEC.md`

**Step 1: 更新数据类型表格**

查找并修改：
- 将 A 股指数的数据源从「东方财富」改为「新浪财经」

**Step 2: 更新相关说明**

在文档中添加说明，解释 API 变更的原因

**Step 3: 保存文件**

---

## Summary

本计划完成文档更新：

1. ✅ 更新 API 引用
2. ✅ 更新 CLI 命令结构
3. ✅ 更新数据源说明
