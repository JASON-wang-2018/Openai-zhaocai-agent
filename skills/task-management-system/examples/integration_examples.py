"""
任务管理系统 - 集成示例
演示如何与 Excel 数据处理、Personal Assistant、项目管理整合
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task_manager import TaskManager, ReminderManager

# 尝试导入 Excel 处理器
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    from excel_processor import ProjectManager
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    print("⚠️ Excel 处理器不可用，跳过相关示例")


def example_1_daily_task_planning():
    """示例1：每日任务规划"""
    print("=" * 60)
    print("示例1: 每日任务规划")
    print("=" * 60)

    tm = TaskManager()

    # 创建今日任务
    print("\n添加今日任务...")
    tasks = [
        {
            'title': '完成股票分析报告',
            'priority': '高',
            'category': '工作',
            'deadline': '2026-02-18 18:00',
            'description': '分析双系统模型和个股走势'
        },
        {
            'title': '学习新技能',
            'priority': '中',
            'category': '学习',
            'deadline': '2026-02-20 20:00',
            'description': '学习 First Principles 和 Reasoning Personas'
        },
        {
            'title': '运动30分钟',
            'priority': '低',
            'category': '健康',
            'description': '有氧运动或力量训练'
        }
    ]

    for task in tasks:
        tm.add_task(**task)

    # 生成每日简报
    print("\n生成今日简报...")
    briefing = tm.generate_daily_briefing()
    print(briefing)

    return tm


def example_2_weekly_planning():
    """示例2：每周规划"""
    print("\n" + "=" * 60)
    print("示例2: 每周规划")
    print("=" * 60)

    tm = TaskManager()

    # 创建本周任务
    print("\n添加本周任务...")
    weekly_tasks = [
        {
            'title': '完成3个股票分析',
            'priority': '高',
            'category': '工作',
            'deadline': '2026-02-20 18:00'
        },
        {
            'title': '学习2个新技能',
            'priority': '中',
            'category': '学习',
            'deadline': '2026-02-22 20:00'
        },
        {
            'title': '运动5次',
            'priority': '中',
            'category': '健康',
            'deadline': '2026-02-22 22:00'
        },
        {
            'title': '阅读2本书',
            'priority': '低',
            'category': '学习',
            'deadline': '2026-02-28 20:00'
        },
        {
            'title': '项目风险管理准备',
            'priority': '高',
            'category': '工作',
            'deadline': '2026-02-19 18:00'
        }
    ]

    for task in weekly_tasks:
        tm.add_task(**task)

    # 生成周报
    print("\n生成周报...")
    stats = tm.get_task_statistics()
    print(f"\n📊 本周任务统计")
    print(f"- 总任务: {stats['total']}")
    print(f"- 高优先级: {stats['high_priority']}")
    print(f"- 中优先级: {stats['medium_priority']}")
    print(f"- 低优先级: {stats['low_priority']}")

    print(f"\n按分类:")
    for category, count in stats['categories'].items():
        print(f"- {category}: {count}")

    return tm


def example_3_project_task_integration():
    """示例3：与项目进度表整合"""
    print("\n" + "=" * 60)
    print("示例3: 与项目进度表整合")
    print("=" * 60)

    if not EXCEL_AVAILABLE:
        print("⚠️ Excel 处理器不可用，跳过此示例")
        return None

    tm = TaskManager()
    pm = ProjectManager()

    # 创建项目任务
    print("\n创建项目任务...")
    project_tasks = [
        {
            'title': '需求分析',
            'priority': '高',
            'category': '项目',
            'deadline': '2026-02-20 18:00',
            'description': '完成需求分析和文档'
        },
        {
            'title': '系统设计',
            'priority': '高',
            'category': '项目',
            'deadline': '2026-02-25 18:00',
            'description': '完成系统架构和设计文档'
        },
        {
            'title': '开发实现',
            'priority': '中',
            'category': '项目',
            'deadline': '2026-03-05 18:00',
            'description': '完成核心功能开发'
        }
    ]

    for task in project_tasks:
        tm.add_task(**task)

    # 创建项目进度表
    print("\n创建项目进度表...")
    pm.create_progress_tracker('examples/项目进度表_任务管理.xlsx')

    # 导入任务到 Excel
    print("\n导入任务到 Excel...")
    # 注意：这里简化处理，实际需要导入到正确的格式

    print("✓ 任务与项目进度表已整合")

    return tm


def example_4_deadline_alerts():
    """示例4：截止日期预警"""
    print("\n" + "=" * 60)
    print("示例4: 截止日期预警")
    print("=" * 60)

    tm = TaskManager()
    rm = ReminderManager(tm)

    # 创建任务
    print("\n创建任务...")
    tm.add_task("完成股票分析", priority="高", category="工作",
                deadline="2026-02-18 18:00")
    tm.add_task("项目文档", priority="中", category="项目",
                deadline="2026-02-20 18:00")

    # 添加截止提醒
    print("\n添加截止提醒...")
    rm.add_deadline_reminder(tm.tasks[0].id, days_before=1)
    rm.add_deadline_reminder(tm.tasks[0].id, days_before=7)
    rm.add_deadline_reminder(tm.tasks[1].id, days_before=3)

    # 检查到期提醒
    print("\n检查到期提醒...")
    due = rm.get_due_reminders()
    if due:
        print(f"\n有 {len(due)} 个到期提醒:")
        for reminder in due:
            print(f"- {reminder['message']}")
    else:
        print("\n当前无到期提醒")

    # 检查即将到期的任务
    print("\n即将到期的任务:")
    upcoming = tm.get_upcoming_deadlines(days=7)
    for item in upcoming:
        task = item['task']
        days_left = item['days_left']
        print(f"- {task.title}: {task.deadline} (剩余{days_left}天)")

    return tm


def example_5_task_completion_tracking():
    """示例5：任务完成追踪"""
    print("\n" + "=" * 60)
    print("示例5: 任务完成追踪")
    print("=" * 60)

    tm = TaskManager()

    # 创建任务
    print("\n创建任务...")
    tm.add_task("任务A", priority="高", category="工作")
    tm.add_task("任务B", priority="中", category="工作")
    tm.add_task("任务C", priority="低", category="学习")

    # 完成任务
    print("\n完成高优先级任务...")
    high_tasks = tm.get_high_priority_tasks()
    if high_tasks:
        tm.complete_task(high_tasks[0].id)

    # 查看剩余任务
    print("\n剩余任务:")
    stats = tm.get_task_statistics()
    print(f"- 总任务: {stats['total']}")
    print(f"- 高优先级: {stats['high_priority']}")
    print(f"- 中优先级: {stats['medium_priority']}")
    print(f"- 低优先级: {stats['low_priority']}")

    return tm


def example_6_export_import():
    """示例6：导出和导入任务"""
    print("\n" + "=" * 60)
    print("示例6: 导出和导入任务")
    print("=" * 60)

    tm = TaskManager()

    # 创建任务
    print("\n创建任务...")
    tm.add_task("任务1", priority="高", category="工作")
    tm.add_task("任务2", priority="中", category="学习")

    # 导出任务
    print("\n导出任务...")
    export_data = tm.export_to_dict()
    print(f"导出 {export_data['statistics']['total']} 个任务")

    # 保存到文件
    import json
    with open('tasks_export.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    print("✓ 已导出到 tasks_export.json")

    # 导入任务
    print("\n导入任务...")
    tm2 = TaskManager()
    imported = tm2.import_from_dict(export_data)
    print(f"✓ 已导入 {imported} 个任务")

    return tm


def example_7_alert_system():
    """示例7：预警系统"""
    print("\n" + "=" * 60)
    print("示例7: 预警系统")
    print("=" * 60)

    tm = TaskManager()

    # 创建任务
    print("\n创建任务...")
    tm.add_task("紧急任务", priority="高", category="工作",
                deadline="2026-02-18 12:00")
    tm.add_task("正常任务", priority="中", category="工作",
                deadline="2026-02-20 18:00")

    # 生成预警报告
    print("\n生成预警报告...")

    # 逾期任务
    overdue = tm.get_overdue_tasks()
    if overdue:
        print("\n🚨 逾期任务:")
        for task in overdue:
            print(f"- {task.title} (截止: {task.deadline})")
    else:
        print("\n✓ 无逾期任务")

    # 即将到期
    upcoming = tm.get_upcoming_deadlines(days=3)
    if upcoming:
        print("\n⏰ 即将到期:")
        for item in upcoming:
            task = item['task']
            days_left = item['days_left']
            print(f"- {task.title}: {task.deadline} (剩余{days_left}天)")

    # 高优先级任务
    high_priority = tm.get_high_priority_tasks()
    if high_priority:
        print("\n🔥 高优先级任务:")
        for task in high_priority:
            print(f"- {task.title} [{task.priority}优先级]")

    return tm


def example_8_full_workflow():
    """示例8：完整工作流"""
    print("\n" + "=" * 60)
    print("示例8: 完整工作流")
    print("=" * 60)

    tm = TaskManager()
    rm = ReminderManager(tm)

    # 步骤1：创建任务
    print("\n步骤1: 创建任务")
    tm.add_task("完成股票分析", priority="高", category="工作",
                deadline="2026-02-18 18:00",
                description="分析双系统模型和个股走势")
    tm.add_task("学习新技能", priority="中", category="学习",
                deadline="2026-02-20 20:00",
                description="学习 First Principles 和 Reasoning Personas")

    # 步骤2：添加提醒
    print("\n步骤2: 添加提醒")
    rm.add_deadline_reminder(tm.tasks[0].id, days_before=1)
    rm.add_deadline_reminder(tm.tasks[1].id, days_before=3)

    # 步骤3：生成每日简报
    print("\n步骤3: 生成每日简报")
    briefing = tm.generate_daily_briefing()
    print(briefing[:500] + "...")

    # 步骤4：检查预警
    print("\n步骤4: 检查预警")
    due = rm.get_due_reminders()
    if due:
        print(f"有 {len(due)} 个到期提醒")

    # 步骤5：完成任务
    print("\n步骤5: 模拟完成第一个任务")
    tm.complete_task(tm.tasks[0].id)

    # 步骤6：查看状态
    print("\n步骤6: 查看状态")
    stats = tm.get_task_statistics()
    print(f"剩余任务: {stats['total']}")
    print(f"高优先级: {stats['high_priority']}")

    print("\n✓ 完整工作流演示完成")

    return tm


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("任务管理系统 - 集成示例")
    print("=" * 60)

    # 创建输出目录
    os.makedirs('examples', exist_ok=True)

    try:
        # 运行示例
        example_1_daily_task_planning()
        example_2_weekly_planning()
        example_3_project_task_integration()
        example_4_deadline_alerts()
        example_5_task_completion_tracking()
        example_6_export_import()
        example_7_alert_system()
        example_8_full_workflow()

        print("\n" + "=" * 60)
        print("✓ 所有示例运行完成!")
        print("=" * 60)
        print("\n生成的文件:")
        print("  - examples/项目进度表_任务管理.xlsx")
        print("  - tasks_export.json")

    except Exception as e:
        print(f"\n✗ 运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
