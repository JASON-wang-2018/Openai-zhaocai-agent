#!/bin/bash
# 项目管理示例脚本

echo "📋 项目管理示例"
echo "================"

# 加载敏捷模型
source knowledge/project_management/models/agile_models.py

# 创建项目
project=$(Project "示例项目" "2024-01-01" "2024-03-31")
echo "项目创建成功：${project.name}"

# 添加任务
task1=$(Task "需求分析" "收集和分析用户需求" "high")
task2=$(Task "系统设计" "设计系统架构" "high")
task3=$(Task "开发实现" "实现核心功能" "medium")
task4=$(Task "测试验证" "进行系统测试" "medium")

project.add_task(task1)
project.add_task(task2)
project.add_task(task3)
project.add_task(task4)

echo "任务添加成功："
for task in "${project.tasks[@]}"; do
    echo "  - ${task.name}"
done

# 分配任务
member1=$(TeamMember "张三" "开发工程师")
member2=$(TeamMember "李四" "测试工程师")

project.assign_task(task1, member1)
project.assign_task(task2, member1)
project.assign_task(task3, member1)
project.assign_task(task4, member2)

echo ""
echo "任务分配成功："
for member in "${project.team_members[@]}"; do
    echo "  ${member.name} (${member.role}):"
    for task in "${member.tasks[@]}"; do
        echo "    - ${task.name}"
    done
done

# 计算项目进度
progress=$(project.calculate_progress)
echo ""
echo "项目进度：${progress}%"

# 创建冲刺计划
sprint_plan=$(create_sprint_plan project 14)
echo ""
echo "冲刺计划："
echo "  冲刺时长：${sprint_plan['sprint_duration']}天"
echo "  任务数量：${#sprint_plan['tasks']}个"
echo "  团队成员：${#sprint_plan['team_members']}人"

echo ""
echo "📊 项目管理建议："
if [ "$progress" -lt 50 ]; then
    echo "建议：加快项目进度，关注关键路径"
else
    echo "建议：保持良好进度，继续执行计划"
fi

echo ""
echo "💡 提示：这只是示例项目管理，实际项目请根据具体情况调整！"