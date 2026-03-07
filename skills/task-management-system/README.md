# 任务管理与预警系统

> **版本**: 1.0
> **功能**: 计划规划、任务管理、重点提醒、预警功能

---

## 🎯 核心功能

### 1. 任务管理
- ✅ 创建任务（标题、描述、优先级、截止日期）
- ✅ 编辑任务
- ✅ 删除任务
- ✅ 标记完成
- ✅ 任务分类（工作、个人、学习、健康等）
- ✅ 优先级管理（高、中、低）

### 2. 计划规划
- 📅 每日任务规划
- 📅 每周目标设定
- 📅 季度目标追踪
- 📅 任务统计分析

### 3. 重点提醒
- 🔥 Top 3 高优先级任务
- 🔥 今日必做任务
- 🔥 截止日期提醒
- 🔥 优先级紧急提醒

### 4. 预警系统
- ⏰ 截止日期预警（提前1天、3天、7天）
- ⏰ 逾期任务提醒
- ⏰ 高优先级任务提醒
- ⏰ 自定义提醒

---

## 🚀 快速开始

### 1. 创建任务管理器
```python
from task_manager import TaskManager

tm = TaskManager()

# 添加任务
tm.add_task(
    title="完成股票分析报告",
    priority="高",
    category="工作",
    deadline="2026-02-18 18:00",
    description="分析双系统模型和个股走势"
)

tm.add_task(
    title="学习新技能",
    priority="中",
    category="学习",
    deadline="2026-02-20 20:00"
)
```

### 2. 生成每日简报
```python
briefing = tm.generate_daily_briefing()
print(briefing)
```

输出：
```
📋 今日任务简报 - 2026-02-17 (Tuesday)

🔥 今日重点 (Top 3)
1. 完成股票分析报告 [高优先级] [截止: 2026-02-18 18:00]
2. 学习新技能 [中优先级]
3. 运动30分钟 [低优先级]

⏰ 截止提醒
- 完成股票分析报告: 2026-02-18 18:00 (剩余1天)

📊 任务统计
- 总任务: 3
- 高优先级: 1
- 中优先级: 1
- 低优先级: 1

💡 建议
- 优先完成高优先级任务
- 预留时间应对紧急任务
```

### 3. 添加截止提醒
```python
from task_manager import ReminderManager

rm = ReminderManager(tm)

# 提前1天提醒
rm.add_deadline_reminder(task_id, days_before=1)

# 提前3天提醒
rm.add_deadline_reminder(task_id, days_before=3)
```

---

## 📊 任务优先级

### 高优先级（🔴）
- 今天必须完成
- 影响项目进度
- 涉及重要决策
- 有截止日期压力

### 中优先级（🟡）
- 本周内完成
- 影响次要目标
- 需要持续关注

### 低优先级（🟢）
- 有空再做
- 长期目标
- 运动/学习等

---

## 🔄 与其他技能整合

### 与 Personal Assistant 整合
```python
from task_manager import TaskManager
from skills.personal_assistant.scripts.daily_briefing import DailyBriefing

# 生成每日简报
tm = TaskManager()
tasks_briefing = tm.generate_daily_briefing()

# 合并到 Personal Assistant
personal_briefing = DailyBriefing.generate()
personal_briefing['sections'].append({
    'title': '📋 今日任务',
    'content': tasks_briefing,
    'type': 'tasks'
})
```

### 与 Excel 数据处理整合
```python
from task_manager import TaskManager
from excel_processor import ProjectManager

tm = TaskManager()
pm = ProjectManager()

# 创建项目进度表
pm.create_progress_tracker('项目进度表.xlsx')

# 导入任务到 Excel
tasks = tm.get_all_tasks()
# 转换为 Excel 格式并导入
```

### 与项目风险管理整合
```python
from task_manager import TaskManager
from risk_manager import RiskManager

tm = TaskManager()
rm = RiskManager()

# 创建任务时自动识别风险
task = tm.add_task("新技术开发", priority="高")

# 生成风险
risks = identify_task_risks(task)
rm.add_risks(risks)
```

---

## ⏰ 定时提醒设置

### 使用 OpenClaw Cron
```bash
# 每天早上7点：生成今日任务简报
openclaw cron add \
  --schedule "0 7 * * *" \
  --tz "Asia/Shanghai" \
  --message "生成今日任务简报"

# 每小时：检查逾期任务
openclaw cron add \
  --schedule "0 * * * *" \
  --tz "Asia/Shanghai" \
  --message "检查逾期任务"

# 每天晚上9点：生成晚间复盘
openclaw cron add \
  --schedule "0 21 * * *" \
  --tz "Asia/Shanghai" \
  --message "生成晚间任务复盘"
```

### 使用 Python APScheduler
```python
from apscheduler.schedulers.blocking import BlockingScheduler
from task_manager import TaskManager

tm = TaskManager()
scheduler = BlockingScheduler()

# 每天早上7点：生成今日简报
@scheduler.scheduled_job('cron', hour=7, minute=0, timezone='Asia/Shanghai')
def daily_briefing():
    briefing = tm.generate_daily_briefing()
    print(briefing)

# 每小时：检查逾期任务
@scheduler.scheduled_job('cron', minute=0, timezone='Asia/Shanghai')
def check_overdue():
    overdue = tm.get_overdue_tasks()
    if overdue:
        print(f"🚨 逾期任务 ({len(overdue)}):")
        for task in overdue:
            print(f"  - {task['title']} (截止: {task['deadline']})")

scheduler.start()
```

---

## 📝 数据存储

### 文件结构
```
task-management-system/
├── task_manager.py         # 核心类
├── data/
│   ├── tasks.json          # 任务数据
│   ├── completed_tasks.json # 已完成任务
│   └── reminders.json     # 提醒数据
└── examples/
    └── integration_examples.py  # 集成示例
```

### 数据格式
```json
{
  "id": "T1234567890",
  "title": "完成股票分析报告",
  "priority": "高",
  "category": "工作",
  "deadline": "2026-02-18 18:00",
  "description": "分析双系统模型和个股走势",
  "completed": false,
  "created_at": "2026-02-17T10:00:00",
  "completed_at": null
}
```

---

## 🎨 使用场景

### 场景1：每日规划
```python
from task_manager import TaskManager

tm = TaskManager()

# 创建今日任务
tm.add_task("完成股票分析", priority="高", category="工作")
tm.add_task("学习技能", priority="中", category="学习")
tm.add_task("运动30分钟", priority="低", category="健康")

# 生成今日简报
briefing = tm.generate_daily_briefing()
print(briefing)
```

### 场景2：每周规划
```python
from task_manager import TaskManager

tm = TaskManager()

# 设定每周目标
weekly_tasks = [
    {"title": "完成3个股票分析", "priority": "高", "category": "工作"},
    {"title": "学习2个新技能", "priority": "中", "category": "学习"},
    {"title": "运动5次", "priority": "中", "category": "健康"},
    {"title": "阅读2本书", "priority": "低", "category": "学习"}
]

for task in weekly_tasks:
    tm.add_task(**task)

# 生成周报
stats = tm.get_task_statistics()
print(f"本周任务: {stats['total']} 个")
```

### 场景3：项目任务管理
```python
from task_manager import TaskManager
from excel_processor import ProjectManager

tm = TaskManager()
pm = ProjectManager()

# 为项目创建任务
project_tasks = [
    {"title": "需求分析", "priority": "高", "category": "项目", "deadline": "2026-02-20"},
    {"title": "系统设计", "priority": "高", "category": "项目", "deadline": "2026-02-25"},
    {"title": "开发实现", "priority": "中", "category": "项目", "deadline": "2026-03-05"}
]

for task in project_tasks:
    tm.add_task(**task)

# 创建项目进度表
pm.create_progress_tracker('项目进度表.xlsx')

# 查看项目进度
stats = tm.get_task_statistics()
print(f"项目进度: {stats['total']} 个任务")
```

### 场景4：预警系统
```python
from task_manager import TaskManager, ReminderManager

tm = TaskManager()
rm = ReminderManager(tm)

# 检查逾期任务
overdue = tm.get_overdue_tasks()
if overdue:
    print(f"🚨 逾期任务 ({len(overdue)}):")
    for task in overdue:
        print(f"  - {task.title} (截止: {task.deadline})")

# 检查即将到期
upcoming = tm.get_upcoming_deadlines(days=7)
if upcoming:
    print(f"\n⏰ 即将到期 ({len(upcoming)}):")
    for item in upcoming:
        task = item['task']
        days_left = item['days_left']
        print(f"  - {task.title} (剩余{days_left}天)")

# 检查高优先级任务
high_priority = tm.get_high_priority_tasks()
if high_priority:
    print(f"\n🔥 高优先级任务 ({len(high_priority)}):")
    for task in high_priority:
        print(f"  - {task.title}")
```

---

## 💡 最佳实践

### 1. 每日规划
- 🌅 早上花5分钟规划今日任务
- 🎯 设定Top 3优先任务
- ⏰ 估算每个任务的时间
- 📋 留出缓冲时间应对意外

### 2. 任务执行
- 🔥 先完成高优先级任务
- ⏰ 使用番茄工作法（25分钟专注+5分钟休息）
- ✅ 完成任务立即标记
- 🚫 避免多任务并行

### 3. 定期回顾
- 📊 每周回顾完成任务情况
- 📈 分析时间使用效率
- 💡 总结经验教训
- 🎯 调整下周计划

### 4. 提前预警
- ⏰ 提前1天、3天、7天设置提醒
- 🚨 监控逾期任务
- 🔥 优先处理高优先级任务
- 📝 记录完成时间供分析

---

## 🔧 核心类说明

### Task（任务类）
```python
task = Task(
    title="任务标题",
    priority="高",  # 高/中/低
    category="工作",  # 分类
    deadline="2026-02-18 18:00",  # 截止日期
    description="任务描述",
    completed=False  # 是否完成
)
```

### TaskManager（任务管理器）
```python
tm = TaskManager()

# 添加任务
tm.add_task(title, priority, category, deadline, description)

# 批量添加
tm.add_tasks(tasks_list)

# 完成任务
tm.complete_task(task_id)

# 删除任务
tm.delete_task(task_id)

# 获取任务
tm.get_daily_tasks()  # 今日任务
tm.get_urgent_tasks()  # 紧急任务
tm.get_overdue_tasks()  # 逾期任务
tm.get_upcoming_deadlines(days=7)  # 即将到期

# 生成简报
tm.generate_daily_briefing()

# 统计
tm.get_task_statistics()
```

### ReminderManager（提醒管理器）
```python
rm = ReminderManager(tm)

# 添加截止提醒
rm.add_deadline_reminder(task_id, days_before=1)

# 检查到期提醒
rm.get_due_reminders()

# 标记已发送
rm.mark_sent(reminder_id)
```

---

## 📚 文件说明

- **task_manager.py** - 核心类（Task、TaskManager、ReminderManager）
- **SKILL.md** - 完整技能文档
- **README.md** - 本文件
- **examples/integration_examples.py** - 8个完整示例

---

## 🎯 快速命令

```python
# 创建任务
from task_manager import TaskManager
tm = TaskManager()
tm.add_task("任务标题", priority="高")

# 生成每日简报
briefing = tm.generate_daily_briefing()
print(briefing)

# 检查逾期任务
overdue = tm.get_overdue_tasks()
print(f"逾期: {len(overdue)}")

# 完成任务
tm.complete_task(task_id)
```

---

**记住：系统化的任务管理 + 智能的提醒预警 = 高效的生产力！**

---

**版本**: 1.0
**更新日期**: 2026-02-17
