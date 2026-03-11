# Cron Manager Skill

定时任务可靠性保障：健康检查 + 自动补偿

## 功能
- 查看任务状态和执行历史
- 手动补偿执行失败的任务
- 自动补偿机制（系统级cron）

## 命令
```bash
# 查看状态
python3 skills/cron-manager/monitor.py

# 手动补偿
python3 skills/cron-manager/cron_manager.py catchup <任务名>
```

## 任务配置
关键任务定义在 `config/tasks.json`
