#!/bin/bash
# 产品设计示例脚本

echo "🎨 产品设计示例"
echo "================"

# 加载UX模型
source knowledge/product_design/models/ux_models.py

# 创建用户画像
user_data=(
    "张三,25,软件工程师,['提高工作效率','学习新技术'],['复杂的界面','缺乏文档']"
    "李四,30,产品经理,['更好的数据分析工具','直观的界面'],['响应慢','功能不完整']"
)

echo "用户研究数据："
for data in "${user_data[@]}"; do
    IFS=',' read -r name age occupation goals pain_points <<< "$data"
    goals_array=($(echo "$goals" | tr -d "['']" | tr ',' ' '))
    pain_points_array=($(echo "$pain_points" | tr -d "['']" | tr ',' ' '))
    
    user=$(UserPersona "$name" "$age" "$occupation" "$goals_array" "$pain_points_array")
    research=$(conduct_user_research [user])
    echo "  $name ($age岁, $occupation):"
    echo "    目标：${goals_array[@]}"
    echo "    痛点：${pain_points_array[@]}"
done

echo ""
# 创建线框图
wireframe=$(Wireframe "示例应用" ["首页", "产品页面", "用户中心"])
wireframe_result=$(wireframe.generate_wireframe)
echo "线框图创建成功："
echo "  名称：${wireframe_result['name']}"
echo "  页面数量：${#wireframe_result['pages']}个"
echo "  结构：${wireframe_result['structure']}"

echo ""
# 创建原型
interactions=("点击按钮跳转", "滚动加载更多", "搜索功能")
prototype=$(Prototype wireframe interactions)
prototype_result=$(prototype.create_prototype)
echo "原型创建成功："
echo "  线框图页面：${#prototype_result['wireframe']['pages']}个"
echo "  交互功能：${#prototype_result['interactions']}个"
echo "  测试要求：${prototype_result['testing_requirements']}"

echo ""
echo "🎨 设计建议："
echo "  1. 根据用户研究结果优化产品设计"
echo "  2. 确保线框图结构清晰"
echo "  3. 原型测试是关键环节"

echo ""
echo "💡 提示：这只是示例产品设计，实际设计请考虑更多用户需求！"