#!/usr/bin/env python3
"""
自动任务提醒系统
定时生成任务简报、预警检查、自动提醒
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from task_manager import TaskManager, ReminderManager


def send_alert(message: str):
    """发送提醒（可以根据实际环境调整）"""
    print(f"\n{'='*60}")
    print(f"⏰ 任务提醒")
    print(f"{'='*60}")
    print(message)
    print(f"{'='*60}\n")


def daily_briefing():
    """每日任务简报"""
    tm = TaskManager()
    
    briefing = tm.generate_daily_briefing()
    send_alert(briefing)
    
    return briefing


def urgent_check():
    """紧急任务检查"""
    tm = TaskManager()
    
    alerts = []
    
    # 检查截止日期提醒
    upcoming = tm.get_upcoming_deadlines(days=7)
    if upcoming:
        alerts.append(f"\n⏰ 即将到期任务 ({len(upcoming)}个):")
        for item in upcoming[:5]:  # 只显示前5个
            task = item['task']
            days = item['days_left']
            alerts.append(f"  - {task.title}: {task.deadline} (剩余{days}天)")
    
    # 检查高优先级任务
    high_priority = tm.get_high_priority_tasks()
    if high_priority:
        alerts.append(f"\n🔥 高优先级任务 ({len(high_priority)}个):")
        for task in high_priority[:5]:  # 只显示前5个
            alerts.append(f"  - {task.title}")
    
    # 检查逾期任务
    overdue = tm.get_overdue_tasks()
    if overdue:
        alerts.append(f"\n🚨 逾期任务 ({len(overdue)}个):")
        for task in overdue[:5]:
            alerts.append(f"  - {task.title} (截止: {task.deadline})")
    
    if alerts:
        send_alert("\n".join(alerts))
        return "\n".join(alerts)
    
    return None


def weekly_report():
    """生成周报"""
    tm = TaskManager()
    
    stats = tm.get_task_statistics()
    
    report = []
    report.append("\n📊 本周任务统计")
    report.append(f"  总任务: {stats['total']}")
    report.append(f"  高优先级: {stats['high_priority']}")
    report.append(f"  中优先级: {stats['medium_priority']}")
    report.append(f"  低优先级: {stats['low_priority']}")
    report.append(f"  逾期: {stats['overdue']}")
    
    report_text = "\n".join(report)
    send_alert(report_text)
    
    return report_text


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动任务提醒系统')
    parser.add_argument('--mode', choices=['briefing', 'urgent', 'weekly', 'all'],
                        default='all', help='运行模式')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"📋 自动任务提醒系统")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    if args.mode == 'briefing' or args.mode == 'all':
        print("\n📅 生成每日任务简报...")
        daily_briefing()
    
    if args.mode == 'urgent' or args.mode == 'all':
        print("\n🔍 检查紧急任务...")
        urgent_check()
    
    if args.mode == 'weekly':
        print("\n📊 生成周报...")
        weekly_report()
    
    print(f"\n{'='*60}")
    print("✅ 自动任务提醒完成")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
