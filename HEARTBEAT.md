# HEARTBEAT.md - 定时任务

## 每日任务

### 20:00 每日状态汇总
- 读取当日memory/日志
- 输出完成事项/问题/计划

### 周五18:00 周报生成
- 执行 scripts/weekly_report.sh
- 输出周报到 reports/

### 01:00 知识库学习
- 执行 scripts/knowledge_learner.sh
- 整合 learnings/ 到 MEMORY.md

### 周日 23:59 Git自动备份
- 备份workspace到git
