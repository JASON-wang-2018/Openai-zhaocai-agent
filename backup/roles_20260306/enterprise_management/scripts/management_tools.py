#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业管理工具
包含：决策、绩效、沟通、时间管理等工具
"""

# ============= 管理决策 =============
def decision_matrix(criteria_weights, options_scores):
    """
    决策矩阵法
    criteria_weights: {"标准": 权重}
    options_scores: {"选项": {"标准": 得分}}
    """
    results = {}
    for option, scores in options_scores.items():
        total = 0
        for criteria, weight in criteria_weights.items():
            score = scores.get(criteria, 0)
            total += score * weight
        results[option] = total
    
    return results

# ============= SMART目标检查 =============
def check_smartgoal(goal):
    """
    检查目标是否SMART
    S - Specific 具体
    M - Measurable 可衡量
    A - Achievable 可达成
    R - Relevant 相关性
    T - Time-bound 时限
    """
    checks = {
        "具体(S)": len(goal) > 0,
        "可衡量(M)": "数字" in goal or "%" in goal,
        "可达成(A)": True,  # 需要上下文
        "相关性(R)": True,  # 需要上下文
        "时限(T)": "周" in goal or "月" in goal or "年" in goal
    }
    
    score = sum(checks.values()) / len(checks) * 100
    return checks, score

# ============= 绩效评估 =============
def performance_score(kpis, actuals):
    """
    计算绩效得分
    kpis: [{"name": "KPI名", "weight": 权重, "target": 目标值}]
    actuals: {"KPI名": 实际值}
    """
    total_score = 0
    total_weight = 0
    
    results = []
    for kpi in kpis:
        name = kpi["name"]
        weight = kpi["weight"]
        target = kpi["target"]
        actual = actuals.get(name, 0)
        
        # 计算达成率
        rate = actual / target if target > 0 else 0
        score = min(rate * 100, 120)  # 上限120
        
        total_score += score * weight
        total_weight += weight
        
        results.append({
            "name": name,
            "target": target,
            "actual": actual,
            "rate": f"{rate*100:.1f}%",
            "score": score
        })
    
    final_score = total_score / total_weight if total_weight > 0 else 0
    return results, final_score

# ============= 时间管理 =============
def eisenhower_matrix(tasks):
    """
    艾森豪威尔矩阵分类
    tasks: [{"name": "任务名", "important": True/False, "urgent": True/False}]
    """
    quadrants = {
        "Q1_重要紧急": [],
        "Q2_重要不紧急": [],
        "Q3_紧急不重要": [],
        "Q4_不重要不紧急": []
    }
    
    for task in tasks:
        name = task["name"]
        imp = task.get("important", False)
        urg = task.get("urgent", False)
        
        if imp and urg:
            quadrants["Q1_重要紧急"].append(name)
        elif imp and not urg:
            quadrants["Q2_重要不紧急"].append(name)
        elif not imp and urg:
            quadrants["Q3_紧急不重要"].append(name)
        else:
            quadrants["Q4_不重要不紧急"].append(name)
    
    return quadrants

# ============= 沟通风格判断 =============
def communication_style(style_type):
    """
    沟通风格类型
    - 控制型: 直接、结果导向
    - 友善型: 友好、支持
    - 表达型: 热情、创新
    - 分析型: 数据、谨慎
    """
    styles = {
        "控制型": {
            "特点": "直接、快速、结果导向",
            "沟通方式": "简洁、有数据、直奔主题",
            "避免": "闲聊、情绪化"
        },
        "友善型": {
            "特点": "友好、合作、关心人",
            "沟通方式": "温和、建立关系、关注感受",
            "避免": "太快进入主题、忽视关系"
        },
        "表达型": {
            "特点": "热情、有创意、喜欢表达",
            "沟通方式": "生动、有故事、鼓励参与",
            "避免": "太正式、限制创意"
        },
        "分析型": {
            "特点": "数据导向、谨慎、系统",
            "沟通方式": "详细、有数据、逻辑清晰",
            "避免": "太笼统、缺乏细节"
        }
    }
    return styles.get(style_type, styles["控制型"])

# ============= SWOT分析 =============
def swot_analysis(strengths, weaknesses, opportunities, threats):
    """
    SWOT分析框架
    """
    return {
        "S(优势)": strengths,
        "W(劣势)": weaknesses,
        "O(机会)": opportunities,
        "T(威胁)": threats
    }

# ============= 干系人分析 =============
def stakeholder_analysis(stakeholders):
    """
    干系人分析
    stakeholders: [{"name": "人名", "interest": 高/中/低, "influence": 高/中/低}]
    """
    matrix = {
        "高利益高影响": [],  # 重点管理
        "高利益低影响": [],  # 保持满意
        "低利益高影响": [],  # 保持沟通
        "低利益低影响": []   # 监督
    }
    
    for s in stakeholders:
        name = s["name"]
        interest = s["interest"]
        influence = s["influence"]
        
        key = (interest, influence)
        if key == ("高", "高"):
            matrix["高利益高影响"].append(name)
        elif key == ("高", "低"):
            matrix["高利益低影响"].append(name)
        elif key == ("低", "高"):
            matrix["低利益高影响"].append(name)
        else:
            matrix["低利益低影响"].append(name)
    
    return matrix

# ============= 主程序 =============
if __name__ == "__main__":
    print("=" * 50)
    print("   企业管理工具箱")
    print("=" * 50)
    
    # SMART目标检查
    print("\n【SMART目标检查】")
    goal = "Q3完成销售额100万"
    checks, score = check_smartgoal(goal)
    for k, v in checks.items():
        print(f"  {k}: {'✓' if v else '✗'}")
    print(f"  符合度: {score:.0f}%")
    
    # 绩效评估
    print("\n【绩效评估】")
    kpis = [
        {"name": "销售额", "weight": 0.4, "target": 100},
        {"name": "利润率", "weight": 0.3, "target": 15},
        {"name": "客户满意度", "weight": 0.3, "target": 90}
    ]
    actuals = {"销售额": 110, "利润率": 12, "客户满意度": 88}
    results, score = performance_score(kpis, actuals)
    for r in results:
        print(f"  {r['name']}: 目标{r['target']} 实际{r['actual']} 达成{r['rate']}")
    print(f"  综合得分: {score:.1f}")
    
    print("\n" + "=" * 50)
