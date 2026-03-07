"""
任务管理与预警系统
支持任务管理、计划规划、重点提醒、预警功能
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class Task:
    """任务类"""

    def __init__(self, title: str, priority: str = "中", 
                 category: str = "工作", deadline: Optional[str] = None,
                 description: str = "", completed: bool = False):
        self.id = f"T{int(datetime.now().timestamp())}"
        self.title = title
        self.priority = priority  # 高、中、低
        self.category = category  # 工作、个人、学习、健康等
        self.deadline = deadline  # 格式: "YYYY-MM-DD" 或 "YYYY-MM-DD HH:MM"
        self.description = description
        self.completed = completed
        self.created_at = datetime.now().isoformat()
        self.completed_at = None

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'category': self.category,
            'deadline': self.deadline,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建任务"""
        task = cls(
            title=data['title'],
            priority=data.get('priority', '中'),
            category=data.get('category', '工作'),
            deadline=data.get('deadline'),
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        task.id = data['id']
        task.created_at = data.get('created_at', datetime.now().isoformat())
        task.completed_at = data.get('completed_at')
        return task


class TaskManager:
    """任务管理器"""

    def __init__(self, data_dir: str = None):
        """初始化任务管理器"""
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')

        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

        self.tasks_file = os.path.join(data_dir, 'tasks.json')
        self.completed_file = os.path.join(data_dir, 'completed_tasks.json')
        self.reminders_file = os.path.join(data_dir, 'reminders.json')

        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """加载任务"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in tasks_data]

    def save_tasks(self):
        """保存任务"""
        tasks_data = [task.to_dict() for task in self.tasks]
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, indent=2, ensure_ascii=False)
        print(f"✓ 任务已保存: {len(self.tasks)} 个")

    def add_task(self, title: str, priority: str = "中",
                category: str = "工作", deadline: str = None,
                description: str = "") -> Task:
        """添加任务"""
        task = Task(title, priority, category, deadline, description)
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ 任务已添加: {task.title} [{task.priority}优先级]")
        return task

    def add_tasks(self, tasks_list: List[Dict]) -> List[Task]:
        """批量添加任务"""
        added_tasks = []
        for task_data in tasks_list:
            task = self.add_task(**task_data)
            added_tasks.append(task)
        return added_tasks

    def complete_task(self, task_id: str):
        """标记任务完成"""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                task.completed_at = datetime.now().isoformat()

                # 保存到已完成文件
                self.save_completed_task(task)

                # 从当前任务列表移除
                self.tasks.remove(task)
                self.save_tasks()

                print(f"✓ 任务已完成: {task.title}")
                return True
        print(f"✗ 未找到任务: {task_id}")
        return False

    def delete_task(self, task_id: str):
        """删除任务"""
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                print(f"✓ 任务已删除: {task.title}")
                return True
        print(f"✗ 未找到任务: {task_id}")
        return False

    def get_daily_tasks(self) -> List[Task]:
        """获取今日任务"""
        today = datetime.now().date()
        daily_tasks = []

        for task in self.tasks:
            if task.deadline:
                deadline_date = datetime.strptime(task.deadline.split()[0], '%Y-%m-%d').date()
                if deadline_date <= today:
                    daily_tasks.append(task)

        return daily_tasks

    def get_urgent_tasks(self) -> List[Task]:
        """获取紧急任务（高优先级）"""
        return [task for task in self.tasks if task.priority == "高" and not task.completed]

    def get_high_priority_tasks(self) -> List[Task]:
        """获取高优先级任务"""
        return [task for task in self.tasks if task.priority == "高" and not task.completed]

    def get_medium_priority_tasks(self) -> List[Task]:
        """获取中优先级任务"""
        return [task for task in self.tasks if task.priority == "中" and not task.completed]

    def get_low_priority_tasks(self) -> List[Task]:
        """获取低优先级任务"""
        return [task for task in self.tasks if task.priority == "低" and not task.completed]

    def get_overdue_tasks(self) -> List[Task]:
        """获取逾期任务"""
        now = datetime.now()
        overdue_tasks = []

        for task in self.tasks:
            if task.deadline and not task.completed:
                deadline = datetime.strptime(task.deadline, '%Y-%m-%d %H:%M')
                if deadline < now:
                    overdue_tasks.append(task)

        return overdue_tasks

    def get_upcoming_deadlines(self, days: int = 3) -> List[Dict]:
        """获取即将到期的任务"""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        upcoming = []

        for task in self.tasks:
            if task.deadline and not task.completed:
                deadline = datetime.strptime(task.deadline, '%Y-%m-%d %H:%M')
                if now <= deadline <= cutoff:
                    days_left = (deadline - now).days
                    upcoming.append({
                        'task': task,
                        'days_left': days_left
                    })

        # 按到期时间排序
        upcoming.sort(key=lambda x: x['days_left'])
        return upcoming

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """按分类获取任务"""
        return [task for task in self.tasks if task.category == category and not task.completed]

    def get_task_statistics(self) -> Dict:
        """获取任务统计"""
        total = len(self.tasks)
        high = len(self.get_high_priority_tasks())
        medium = len(self.get_medium_priority_tasks())
        low = len(self.get_low_priority_tasks())
        overdue = len(self.get_overdue_tasks())

        categories = {}
        for task in self.tasks:
            cat = task.category
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1

        return {
            'total': total,
            'high_priority': high,
            'medium_priority': medium,
            'low_priority': low,
            'overdue': overdue,
            'categories': categories
        }

    def generate_daily_briefing(self) -> str:
        """生成每日任务简报"""
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        weekday = now.strftime('%A')

        brief = f"📋 今日任务简报 - {today} ({weekday})\n\n"

        # 今日重点（Top 3 高优先级）
        high_priority = self.get_high_priority_tasks()[:3]
        brief += "🔥 今日重点 (Top 3)\n"
        if high_priority:
            for i, task in enumerate(high_priority, 1):
                deadline_info = f" [截止: {task.deadline}]" if task.deadline else ""
                brief += f"{i}. {task.title} [{task.priority}优先级]{deadline_info}\n"
        else:
            brief += "  无高优先级任务\n"

        brief += "\n"

        # 截止提醒
        upcoming = self.get_upcoming_deadlines(days=7)
        if upcoming:
            brief += "⏰ 截止提醒\n"
            for item in upcoming:
                task = item['task']
                days_left = item['days_left']
                brief += f"- {task.title}: {task.deadline} (剩余{days_left}天)\n"
            brief += "\n"

        # 任务统计
        stats = self.get_task_statistics()
        brief += f"📊 任务统计\n"
        brief += f"- 总任务: {stats['total']}\n"
        brief += f"- 高优先级: {stats['high_priority']}\n"
        brief += f"- 中优先级: {stats['medium_priority']}\n"
        brief += f"- 低优先级: {stats['low_priority']}\n"
        brief += f"- 逾期: {stats['overdue']}\n"

        # 逾期警告
        if stats['overdue'] > 0:
            overdue_tasks = self.get_overdue_tasks()
            brief += "\n"
            brief += "🚨 逾期警告\n"
            for task in overdue_tasks:
                brief += f"- {task.title} (截止: {task.deadline})\n"

        brief += "\n"
        brief += "💡 建议\n"
        brief += "- 优先完成高优先级任务\n"
        brief += "- 预留时间应对紧急任务\n"
        brief += "- 定期回顾任务完成情况\n"

        return brief

    def save_completed_task(self, task: Task):
        """保存已完成的任务"""
        completed_tasks = []
        if os.path.exists(self.completed_file):
            with open(self.completed_file, 'r', encoding='utf-8') as f:
                completed_tasks = json.load(f)

        completed_tasks.append(task.to_dict())

        with open(self.completed_file, 'w', encoding='utf-8') as f:
            json.dump(completed_tasks, f, indent=2, ensure_ascii=False)

    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        return self.tasks

    def export_to_dict(self) -> Dict:
        """导出为字典格式"""
        return {
            'tasks': [task.to_dict() for task in self.tasks],
            'statistics': self.get_task_statistics(),
            'exported_at': datetime.now().isoformat()
        }

    def import_from_dict(self, data: Dict):
        """从字典导入任务"""
        tasks_data = data.get('tasks', [])
        imported = 0
        for task_data in tasks_data:
            task = Task.from_dict(task_data)
            self.tasks.append(task)
            imported += 1

        self.save_tasks()
        print(f"✓ 已导入 {imported} 个任务")
        return imported


class Reminder:
    """提醒类"""

    def __init__(self, task_id: str, remind_at: str, message: str):
        self.id = f"R{int(datetime.now().timestamp())}"
        self.task_id = task_id
        self.remind_at = remind_at  # 格式: "YYYY-MM-DD HH:MM"
        self.message = message
        self.created_at = datetime.now().isoformat()
        self.sent = False

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'remind_at': self.remind_at,
            'message': self.message,
            'created_at': self.created_at,
            'sent': self.sent
        }


class ReminderManager:
    """提醒管理器"""

    def __init__(self, task_manager: TaskManager, data_dir: str = None):
        """初始化提醒管理器"""
        self.tm = task_manager
        if data_dir is None:
            data_dir = task_manager.data_dir

        self.reminders_file = os.path.join(data_dir, 'reminders.json')
        self.reminders = []
        self.load_reminders()

    def load_reminders(self):
        """加载提醒"""
        if os.path.exists(self.reminders_file):
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                self.reminders = json.load(f)

    def save_reminders(self):
        """保存提醒"""
        with open(self.reminders_file, 'w', encoding='utf-8') as f:
            json.dump(self.reminders, f, indent=2, ensure_ascii=False)

    def add_deadline_reminder(self, task_id: str, days_before: int = 1):
        """添加截止日期提醒"""
        task = next((t for t in self.tm.tasks if t.id == task_id), None)
        if not task or not task.deadline:
            print(f"✗ 任务不存在或没有截止日期: {task_id}")
            return None

        deadline = datetime.strptime(task.deadline, '%Y-%m-%d %H:%M')
        remind_at = deadline - timedelta(days=days_before)
        remind_str = remind_at.strftime('%Y-%m-%d %H:%M')

        message = f"任务 '{task.title}' 将在 {days_before} 天后到期"
        reminder = Reminder(task_id, remind_str, message)

        self.reminders.append(reminder.to_dict())
        self.save_reminders()
        print(f"✓ 已添加截止提醒: {task.title} - 提前{days_before}天")
        return reminder

    def get_due_reminders(self) -> List[Dict]:
        """获取到期提醒"""
        now = datetime.now()
        due_reminders = []

        for reminder in self.reminders:
            if not reminder['sent']:
                remind_at = datetime.strptime(reminder['remind_at'], '%Y-%m-%d %H:%M')
                if remind_at <= now:
                    due_reminders.append(reminder)

        return due_reminders

    def mark_sent(self, reminder_id: str):
        """标记提醒已发送"""
        for reminder in self.reminders:
            if reminder['id'] == reminder_id:
                reminder['sent'] = True
                self.save_reminders()
                return True
        return False


def main():
    """测试代码"""
    print("=" * 60)
    print("任务管理与预警系统")
    print("=" * 60)

    # 创建任务管理器
    tm = TaskManager()

    # 添加示例任务
    print("\n添加示例任务...")
    tm.add_task("完成股票分析报告", priority="高", category="工作",
                deadline="2026-02-18 18:00",
                description="分析双系统模型和个股走势")
    tm.add_task("学习新技能", priority="中", category="学习",
                deadline="2026-02-20 20:00",
                description="学习 First Principles 和 Reasoning Personas")
    tm.add_task("运动30分钟", priority="低", category="健康",
                description="有氧运动或力量训练")

    # 生成每日简报
    print("\n" + "=" * 60)
    briefing = tm.generate_daily_briefing()
    print(briefing)

    # 创建提醒管理器
    rm = ReminderManager(tm)

    # 添加截止提醒
    print("\n添加截止提醒...")
    rm.add_deadline_reminder(tm.tasks[0].id, days_before=1)
    rm.add_deadline_reminder(tm.tasks[1].id, days_before=3)

    # 检查到期提醒
    print("\n" + "=" * 60)
    due = rm.get_due_reminders()
    if due:
        print(f"有 {len(due)} 个到期提醒:")
        for reminder in due:
            print(f"- {reminder['message']}")
    else:
        print("当前无到期提醒")

    print("\n" + "=" * 60)
    print("✓ 测试完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
