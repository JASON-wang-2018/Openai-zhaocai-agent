#!/bin/bash
# 产品设计师角色激活脚本

echo "🎨 激活产品设计师角色..."
echo "加载产品设计知识库..."
echo "加载UX/UI设计模型..."
echo "准备设计工具..."

# 设置环境变量
export ROLE="product_designer"
export KNOWLEDGE_BASE="knowledge/product_design"
export MODELS_DIR="$KNOWLEDGE_BASE/models"
export SCRIPTS_DIR="$KNOWLEDGE_BASE/scripts"

echo "✅ 产品设计师角色已激活！"
echo "你可以开始进行产品设计工作了。"

# 示例命令
echo "可用命令："
echo "  design_product <产品名称> - 设计产品"
echo "  create_wireframe - 创建线框图"
echo "  user_research - 进行用户研究"
echo "  prototype_test - 原型测试"