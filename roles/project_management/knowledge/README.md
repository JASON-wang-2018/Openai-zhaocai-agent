# 项目管理知识库

## 目录

### 知识库 (knowledge/)
1. `01_pm_basics.md` - 项目管理基础与十大知识领域
2. `02_pm_templates.md` - 项目管理实战模板
3. `03_pm_tools.md` - 项目管理工具详解

### 工具 (scripts/)
1. `pm_tools.py` - 项目管理工具箱

---

## 内容概要

### 01_pm_basics.md
- 项目定义与特征
- 五大过程组
- 十大知识领域(整合/范围/进度/成本/质量/资源/沟通/风险/采购/干系人)
- 敏捷/Scrum
- 项目经理能力

### 02_pm_templates.md
- 项目启动模板(章程/干系人)
- 项目规划模板(WBS/范围/进度/风险)
- 项目执行模板(周报/变更/会议)
- 项目监控模板(状态报告/EVM/问题日志)
- 项目收尾模板(总结/经验教训)
- 敏捷/Scrum模板

### 03_pm_tools.md
- 规划工具(WBS/关键路径/资源平衡)
- 进度控制(趋势分析/关键链)
- 成本控制(EVM/FMEA)
- 风险管理(识别/评估/应对)
- 沟通管理(方式选择/干系人矩阵)
- 敏捷工具(看板/燃尽图/速度图)

---

## 使用方式

```python
from scripts.pm_tools import evm_analysis, risk_score, stakeholder_matrix

# EVM分析
result = evm_analysis(pv=100, ev=90, ac=95)

# 风险评估
level, _ = risk_level(risk_score(7, 8))

# 干系人分析
matrix = stakeholder_matrix(stakeholders)
```

---

## 常用工具速查

| 功能 | 函数 |
|------|-------|
| EVM分析 | evm_analysis() |
| 风险评估 | risk_score() |
| 干系人分析 | stakeholder_matrix() |
| 里程碑计划 | milestone_plan() |
| 资源分配 | resource_allocation() |
| 敏捷速度 | story_point_velocity() |
| 变更影响 | change_impact() |
