#!/usr/bin/env python3
"""
自动补偿脚本 - 每5分钟执行一次
只在指定时间段检查是否需要执行
"""
import json
import os
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = f"{SCRIPT_DIR}/config/tasks.json"
HISTORY_FILE = f"{SCRIPT_DIR}/config/history.json"
LOG_FILE = "/tmp/cron_compensate.log"

# 任务执行时间窗口 (小时)
TASK_SCHEDULE = {
    "早安天气": {"hour": 7, "minute": 30},
    "早盘股票知识": {"hour": 8, "minute": 30},
    "午间股市分析": {"hour": 12, "minute": 15},
    "每日股市分析": {"hour": 17, "minute": 30},
    "收盘股市分析": {"hour": 18, "minute": 15},
}

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {}

def save_history(h):
    with open(HISTORY_FILE, "w") as f:
        json.dump(h, f, indent=2)

def is_in_time_window(task_name, window_minutes=10):
    """检查当前时间是否在任务时间窗口内"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    if task_name not in TASK_SCHEDULE:
        return False
    
    target = TASK_SCHEDULE[task_name]
    target_hour = target["hour"]
    target_minute = target["minute"]
    
    # 检查是否在目标时间的前后window_minutes分钟内
    current_total = hour * 60 + minute
    target_total = target_hour * 60 + target_minute
    
    diff = abs(current_total - target_total)
    return diff <= window_minutes

def should_compensate(task_name, history):
    """检查是否需要补偿"""
    now = datetime.now()
    
    # 不在时间窗口内，不需要执行
    if not is_in_time_window(task_name, window_minutes=15):
        return False
    
    if task_name not in history:
        return True  # 从未执行过
    
    last = history[task_name]
    last_time = datetime.fromisoformat(last["time"])
    
    # 检查是否是今天的时间窗口
    if last_time.date() != now.date():
        return True  # 昨天或更早，今天还没执行
    
    # 今天已执行过，跳过
    return False

def run_task(script):
    """执行任务脚本"""
    ws = "/home/admin/.openclaw/workspace"
    cmd = f"cd {ws} && python3 {script} 2>&1"
    result = os.system(cmd)
    return result == 0

def main():
    now = datetime.now()
    log(f"=== 自动补偿检查开始 ({now.strftime('%H:%M')}) ===")
    
    config = load_config()
    history = load_history()
    
    executed = False
    
    for name, cfg in config["tasks"].items():
        if not cfg.get("enabled", True):
            continue
        
        if should_compensate(name, history):
            log(f"▶ 执行任务: {name}")
            success = run_task(cfg["script"])
            history[name] = {
                "time": now.isoformat(),
                "status": "success" if success else "failed",
                "script": cfg["script"]
            }
            log(f"✓ {name}: {'成功' if success else '失败'}")
            executed = True
        else:
            # 不在时间窗口，不提示跳过
            pass
    
    if not executed:
        log("⏰ 当前无任务需执行")
    
    save_history(history)
    log("=== 自动补偿检查完成 ===")

if __name__ == "__main__":
    main()
