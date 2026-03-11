# Cron Jobs 备份
# 生成时间: 2026-03-11 20:36
# 用于新服务器恢复定时任务

## 恢复方法
# 在新服务器上，使用 cron add 命令逐个添加以下 job

---

### 1. heartbeat_120min
- ID: 3eb3d94e-31c6-4e75-ab04-20489b19aa65
- 周期: 每120分钟
- 类型: systemEvent
- 内容: heartbeat poll - 120分钟周期

---

### 2. 开启勿扰模式
- 调度: 0 23 * * * (每天23:00)
- 类型: systemEvent
- 内容: 勿扰模式：写入 .do_not_disturb=true

---

### 3. 关闭勿扰模式
- 调度: 0 6 * * * (每天6:00)
- 类型: systemEvent
- 内容: 勿扰模式：写入 .do_not_disturb=false

---

### 4. 生活助理-早安问候
- 调度: 30 7 * * * (每天7:30)
- 类型: agentTurn (isolated)
- 内容: 请执行脚本: python3 /home/admin/.openclaw/workspace/scripts/life_assistant.py 并返回执行结果
- 推送: feishu

---

### 5. Daily Weather + English Article
- 调度: 50 7 * * * (每天7:50)
- 类型: agentTurn (isolated)
- 内容: 请先检查当前时间（北京时间），如果是23:00-06:00之间则跳过发送。否则获取苏州天气并生成一篇英文短文，然后发送到飞书给用户
- 推送: announce

---

### 6. 早盘股票知识推送
- 调度: 30 8 * * * (每天8:30)
- 类型: agentTurn (isolated)
- 内容: 执行脚本: python3 /home/admin/.openclaw/workspace/scripts/morning_stock_tips.py
- 推送: feishu

---

### 7. 午间股市分析
- 调度: 15 12 * * * (每天12:15)
- 类型: agentTurn (isolated)
- 内容: 执行脚本: python3 /home/admin/.openclaw/workspace/scripts/market_analysis.py noon
- 推送: feishu

---

### 8. 每日股市分析报告
- 调度: 30 17 * * * (每天17:30)
- 类型: agentTurn (isolated)
- 内容: 请执行以下任务：
  1. 运行 python3 /home/admin/.openclaw/workspace/scripts/stock_analysis_baostock.py 获取五大指数数据
  2. 用双系统模型（技术面+主力行为）生成分析报告
  3. 发送到飞书给用户
  4. 如果是23:00-06:00之间则跳过
- 推送: announce

---

### 9. 收盘股市分析
- 调度: 15 18 * * * (每天18:15)
- 类型: agentTurn (isolated)
- 内容: 执行脚本: python3 /home/admin/.openclaw/workspace/scripts/market_analysis.py close
- 推送: feishu

---

### 10. 周三Git+本地备份
- 调度: 0 0 * * 3 (每周三0:00)
- 类型: agentTurn (isolated)
- 内容: 请执行以下备份操作：
  1. 进入 /home/admin/.openclaw/workspace 目录
  2. 执行 git add -A && git commit -m '自动备份 $(date +%Y-%m-%d)' && git push
  3. 创建 /home/admin/backup 目录（如果不存在）
  4. 打包workspace: tar -czf /home/admin/backup/backup_$(date +%Y%m%d).tar.gz /home/admin/.openclaw/workspace
  5. 完成后汇报结果
- 推送: announce
