#!/bin/bash
# daily_summary.sh - 每日汇总
# 读取当日日志→提取完成/问题/风险/计划→输出摘要

DATE_DIR="/home/admin/.openclaw/workspace/memory"
today=$(date +%Y-%m-%d)

echo "=== 每日汇总 $today ==="
echo ""

if [ -f "$DATE_DIR/$today.md" ]; then
    echo "【完成事项】"
    grep -A 20 "## 完成" "$DATE_DIR/$today.md" 2>/dev/null || echo "  (无记录)"
    
    echo ""
    echo "【问题】"
    grep -A 10 "## 问题" "$DATE_DIR/$today.md" 2>/dev/null || echo "  (无记录)"
    
    echo ""
    echo "【风险】"
    grep -A 10 "## 风险" "$DATE_DIR/$today.md" 2>/dev/null || echo "  (无记录)"
    
    echo ""
    echo "【明日计划】"
    grep -A 10 "## 计划" "$DATE_DIR/$today.md" 2>/dev/null || echo "  (无记录)"
else
    echo "今日无日志"
fi
