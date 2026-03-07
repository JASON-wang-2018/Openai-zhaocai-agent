#!/bin/bash
# knowledge_learner.sh - 知识学习
# 每日整合learnings/到MEMORY.md

LEARNINGS_DIR="/home/admin/.openclaw/workspace/learnings"
MEMORY_FILE="/home/admin/.openclaw/workspace/MEMORY.md"

echo "=== 知识学习 ==="
echo "整合 learnings/ 到 MEMORY.md"
echo ""

# 检查是否有新学习内容
learnings_count=$(find "$LEARNINGS_DIR" -name "*.md" 2>/dev/null | wc -l)
echo "发现 $learnings_count 个学习文件"

if [ $learnings_count -gt 0 ]; then
    echo ""
    echo "【最新学习内容】"
    find "$LEARNINGS_DIR" -name "*.md" -type f -exec ls -lt {} \; | head -3 | while read line; do
        file=$(echo "$line" | awk '{print $NF}')
        echo "- $(basename $file)"
    done
    
    echo ""
    echo "【待整合】"
    echo "请运行后手动合并到 MEMORY.md"
else
    echo "无新学习内容"
fi
