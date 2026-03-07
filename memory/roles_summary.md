# 角色知识库汇总 (2026-03更新)

## 更新日期: 2026-03-06

---

## 5大角色 | 30+文件

### 1. 股票分析师 (stock_analysis)
**位置**: `roles/stock_analysis/`

**知识库**:
- stock_knowledge.md - K线/技术指标/交易心理
- trading_patterns.md - 主力游资手法(经典)
- trading_patterns_2024.md - 2024-2025最新特点
- book_study.md - 书籍精华(5本)
- old_trader_method.md - 老股民法(6步工作流)
- high_winrate_model.md - 高胜率v3.0模型
- dual_system_analysis.md - 双系统复盘框架

**模型**:
- technical_analysis.py - 技术分析
- emotion_cycle.py - 情绪周期
- high_winrate_model.py - 选股模型
- dual_system_analysis.py - 市场诊断

**脚本**:
- stock_data_v2.py - 多源数据
- dual_system_review.py - 复盘分析

---

### 2. 产品设计师 (product_design)
**位置**: `roles/product_design/`

**知识库**:
- 01_triz_40_principles.md - TRIZ 40发明原理
- 02_contradiction_matrix.md - 矛盾矩阵
- 03_dfma_principles.md - DFMA 23条原则
- 04_vave.md - VAVE价值分析
- 05_dsss.md - DFSS稳健设计
- 06_lean.md - 精益生产方法

**脚本**:
- design_tool.py - TRIZ推荐/VAVE计算/DFMA评分

---

### 3. 职业经理人/项目经理 (enterprise_management)
**位置**: `roles/enterprise_management/`

**知识库**:
- 01_management_mindset.md - 四大心智+管理能力
- 02_workplace_tools.md - 职场管理工具
- 03_project_management.md - 项目管理知识
- 04_tech_pm_style.md - 科技/家电PM风格设定

**脚本**:
- management_tools.py - 决策/绩效/时间管理

---

### 4. 项目管理 (project_management)
**位置**: `roles/project_management/`

**知识库**:
- 01_pm_basics.md - 项目管理基础+十大知识领域
- 02_pm_templates.md - 实战模板
- 03_pm_tools.md - 工具详解

**脚本**:
- pm_tools.py - EVM计算/风险评估/干系人分析

---

### 5. 英语学习 (english_learning)
位置: `knowledge/english_learning/` (原有)

---

## 使用方式

```python
# 股票
from roles.stock_analysis.scripts.stock_data_v2 import get_stock_data
from roles.stock_analysis.models.dual_system_analysis import diagnose_market

# 产品设计
from roles.product_design.scripts.design_tool import triz_recommend, vave_analysis

# 企业管理
from roles.enterprise_management.scripts.management_tools import check_smartgoal

# 项目管理
from roles.project_management.scripts.pm_tools import evm_analysis, risk_score
```

## 备份位置
backup/roles_20260306/
