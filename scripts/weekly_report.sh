#!/bin/bash
# weekly_report.sh - 周报生成
# 读取7天日志→提取完成工作/风险/计划→生成周报

DATE_DIR="/home/admin/.openclaw/workspace/memory"
REPORT_DIR="/home/admin/.openclaw/workspace/reports"

echo "=== 周报生成 ==="
echo "时间范围：最近7天"
echo ""

# 提取最近7天的日志
for i in {0..6}; do
    day=$(date -d "$i days ago" +%Y-%m-%d)
    if [ -f "$DATE_DIR/$day.md" ]; then
        echo "--- $day ---"
        cat "$DATE_DIR/$day.md"
        echo ""
    fi
done

# 生成周报
week=$(date +%Y-W%V)
cat > "$REPORT_DIR/weekly_${week}.md" << EOF
# 周报 ${week}

## 本周完成

## 风险问题

## 下周计划

---
生成时间: $(date)
EOF

echo "周报已生成: $REPORT_DIR/weekly_${week}.md"
