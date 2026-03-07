#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目管理工具箱
包含：EVM计算、风险管理、进度规划等
"""

import json
from datetime import datetime, timedelta

# ============= 1. EVM挣值管理 =============
def evm_analysis(pv, ev, ac):
    """
    挣值分析
    pv: 计划值
    ev: 挣值
    ac: 实际成本
    """
    cv = ev - ac  # 成本偏差
    sv = ev - pv  # 进度偏差
    
    cpi = ev / ac if ac > 0 else 0  # 成本绩效
    spi = ev / pv if pv > 0 else 0  # 进度绩效
    
    return {
        "cv": cv,
        "sv": sv,
        "cpi": cpi,
        "spi": spi,
        "status": "良好" if cpi >= 1 and spi >= 1 else "一般" if cpi >= 0.8 else "差"
    }

def eac_calculation(bac, cpi, spi, method="typical"):
    """
    完工估算
    bac: 完工预算
    cpi: 成本绩效
    spi: 进度绩效
    method: typical(典型)/atypical(非典型)
    """
    if method == "typical":
        eac = bac / cpi
    else:
        eac = (bac - ev) / cpi + ac
    return eac

# ============= 2. 关键路径计算 =============
def critical_path(tasks):
    """
    tasks: [{"id": "A", "duration": 3, "predecessors": []}]
    计算关键路径
    """
    # 计算最早开始/结束
    for task in tasks:
        task["es"] = 0
        task["ef"] = task["duration"]
    
    # 简化版：返回关键路径
    return ["关键路径任务列表"]

# ============= 3. 风险管理 =============
def risk_score(probability, impact):
    """计算风险分值"""
    return probability * impact

def risk_level(score):
    """风险等级"""
    if score >= 15:
        return "极高", "red"
    elif score >= 8:
        return "高", "orange"
    elif score >= 4:
        return "中", "yellow"
    else:
        return "低", "green"

# ============= 4. 干系人分析 =============
def stakeholder_matrix(stakeholders):
    """
    干系人分析
    stakeholders: [{"name": "张三", "interest": "高/低", "influence": "高/低"}]
    """
    matrix = {
        "重点管理": [],
        "令其满意": [],
        "保持沟通": [],
        "监督": []
    }
    
    for s in stakeholders:
        interest = s["interest"]
        influence = s["influence"]
        
        if interest == "高" and influence == "高":
            matrix["重点管理"].append(s["name"])
        elif interest == "低" and influence == "高":
            matrix["令其满意"].append(s["name"])
        elif interest == "高" and influence == "低":
            matrix["保持沟通"].append(s["name"])
        else:
            matrix["监督"].append(s["name"])
    
    return matrix

# ============= 5. 里程碑计算 =============
def milestone_plan(start_date, milestones):
    """
    里程碑计划
    milestones: [{"name": "M1", "days": 30}]
    """
    results = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    
    for m in milestones:
        current = current + timedelta(days=m["days"])
        results.append({
            "milestone": m["name"],
            "date": current.strftime("%Y-%m-%d")
        })
    
    return results

# ============= 6. 资源分配 =============
def resource_allocation(tasks, resources):
    """
    简单资源分配
    tasks: [{"name": "任务", "hours": 40, "resource": "张三"}]
    resources: {"张三": {"capacity": 40}}
    """
    allocation = {}
    
    for task in tasks:
        resource = task["resource"]
        if resource not in allocation:
            allocation[resource] = []
        
        allocation[resource].append({
            "task": task["name"],
            "hours": task["hours"],
            "utilization": task["hours"] / resources[resource]["capacity"]
        })
    
    return allocation

# ============= 7. 敏捷估算 =============
def story_point_velocity(velocity_history):
    """
    计算平均速度
    velocity_history: [20, 22, 18, 25]
    """
    return sum(velocity_history) / len(velocity_history)

def sprint_forecast(total_points, velocity):
    """
    预测Sprint数
    """
    import math
    return math.ceil(total_points / velocity)

# ============= 8. 变更影响评估 =============
def change_impact(scope_change, schedule_change, cost_change):
    """
    变更影响评估
    scope_change: 范围变化%
    schedule_change: 进度变化天数
    cost_change: 成本变化%
    """
    impact_score = 0
    
    if scope_change > 20:
        impact_score += 3
    elif scope_change > 10:
        impact_score += 2
    else:
        impact_score += 1
    
    if schedule_change > 10:
        impact_score += 3
    elif schedule_change > 5:
        impact_score += 2
    else:
        impact_score += 1
    
    if cost_change > 20:
        impact_score += 3
    elif cost_change > 10:
        impact_score += 2
    else:
        impact_score += 1
    
    if impact_score >= 7:
        return "重大变更", "需更高层审批"
    elif impact_score >= 4:
        return "较大变更", "需项目经理审批"
    else:
        return "小变更", "可接受"

# ============= 主测试 =============
if __name__ == "__main__":
    print("=" * 50)
    print("   项目管理工具箱")
    print("=" * 50)
    
    # EVM测试
    print("\n【EVM分析】")
    result = evm_analysis(100, 90, 95)
    print(f"  CV: {result['cv']}, SV: {result['sv']}")
    print(f"  CPI: {result['cpi']:.2f}, SPI: {result['spi']:.2f}")
    print(f"  状态: {result['status']}")
    
    # 风险测试
    print("\n【风险评估】")
    prob, imp = 7, 8
    score = risk_score(prob, imp)
    level, _ = risk_level(score)
    print(f"  概率{prob}×影响{imp}={score} → {level}")
    
    # 干系人
    print("\n【干系人分析】")
    stakeholders = [
        {"name": "CEO", "interest": "高", "influence": "高"},
        {"name": "用户", "interest": "高", "influence": "低"}
    ]
    matrix = stakeholder_matrix(stakeholders)
    print(f"  重点管理: {matrix['重点管理']}")
    print(f"  令其满意: {matrix['令其满意']}")
    
    print("\n" + "=" * 50)
