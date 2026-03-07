#!/bin/bash
# 项目经理角色激活脚本

echo "📋 激活项目经理角色..."
echo "加载项目管理知识库..."
echo "加载敏捷开发模型..."
echo "准备项目管理工具..."

# 设置环境变量
export ROLE="project_manager"
export KNOWLEDGE_BASE="knowledge/project_management"
export MODELS_DIR="$KNOWLEDGE_BASE/models"
export SCRIPTS_DIR="$KNOWLEDGE_BASE/scripts"

echo "✅ 项目经理角色已激活！"
echo "你可以开始进行项目管理工作了。"

# 示例命令
echo "可用命令："
echo "  create_project <项目名称> - 创建新项目"
echo "  assign_task <任务名称> - 分配任务"
echo "  track_progress - 跟踪项目进度"
echo "  generate_report - 生成项目报告"