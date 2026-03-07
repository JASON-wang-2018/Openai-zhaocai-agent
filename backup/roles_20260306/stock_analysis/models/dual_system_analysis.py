#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双系统复盘分析模型
市场状态诊断 + 机会识别 + 操作纪律
"""

import numpy as np
from datetime import datetime

# ============ 1. 市场状态诊断 ============
def diagnose_market(index_df, emotion_data):
    """
    诊断市场状态
    返回: A(主升)/B(冰点)/C(混沌)
    """
    if index_df is None or len(index_df) < 60:
        return "C", "数据不足"
    
    closes = index_df['close'].astype(float).values
    ma20 = np.mean(closes[-20:])
    ma60 = np.mean(closes[-60:])
    ma10 = np.mean(closes[-10:])
    
    # 指数趋势判断
    index_trend = (ma20 > ma60) and (closes[-1] > ma10)
    
    # 情绪数据
    limit_up = emotion_data.get('limit_up', 50)  # 涨停家数
    limit_down = emotion_data.get('limit_down', 10)  # 跌停家数
    highest板 = emotion_data.get('highest板', 5)  # 最高连板
    炸板率 = emotion_data.get('炸板率', 30)  # 炸板率
    
    # 判断逻辑
    # A. 强趋势主升市
    if index_trend and limit_up >= 60 and highest板 >= 5:
        return "A", "强趋势主升市"
    
    # B. 情绪冰点反转市
    if limit_up < 30 and highest板 <= 2 and 炸板率 > 60:
        return "B", "情绪冰点反转市"
    
    # C. 混沌观望期
    return "C", "混沌观望期"

# ============ 2. 主升系统验证 ============
def verify_main_rise(index_df, sector_data, stock_list):
    """
    验证主升系统信号
    """
    result = {
        "指数强趋势": False,
        "板块共振": False,
        "个股信号": False,
        "失败压制": False,
        "最终信号": False
    }
    
    # 1. 指数强趋势
    if index_df and len(index_df) >= 60:
        closes = index_df['close'].astype(float).values
        ma20 = np.mean(closes[-20:])
        ma60 = np.mean(closes[-60:])
        ma10 = np.mean(closes[-10:])
        result["指数强趋势"] = (ma20 > ma60) and (closes[-1] > ma10)
    
    # 2. 板块共振（简化判断）
    if sector_data:
        # 有板块涨幅 > 5%
        strong_sectors = [s for s in sector_data if s.get('涨幅', 0) > 5]
        result["板块共振"] = len(strong_sectors) > 0
    
    # 3. 个股信号（简化判断）
    if stock_list:
        # 有符合龙头特征的股票
        leaders = [s for s in stock_list if s.get('is_leader', False)]
        result["个股信号"] = len(leaders) > 0
    
    # 4. 失败压制（简化判断）
    # 无高位巨量阴等
    result["失败压制"] = True
    
    # 最终信号：全部通过
    result["最终信号"] = all([
        result["指数强趋势"],
        result["板块共振"],
        result["个股信号"],
        result["失败压制"]
    ])
    
    return result

# ============ 3. 冰点系统验证 ============
def verify_ice_reversal(emotion_data, first_board_stock):
    """
    验证冰点系统信号
    """
    result = {
        "情绪冰点": False,
        "逆势首板": False,
        "强逻辑": False,
        "转强确认": False,
        "最终信号": False
    }
    
    # 1. 情绪冰点
    limit_up = emotion_data.get('limit_up', 50)
    highest板 = emotion_data.get('highest板', 5)
    炸板率 = emotion_data.get('炸板率', 30)
    
    result["情绪冰点"] = (limit_up < 30) and (highest板 <= 2) and (炸板率 > 60)
    
    # 2. 逆势首板
    result["逆势首板"] = first_board_stock is not None
    
    # 3. 强逻辑（需要基本面/政策催化）
    if first_board_stock:
        result["强逻辑"] = first_board_stock.get('has催化剂', False)
    
    # 4. 转强确认
    if first_board_stock:
        result["转强确认"] = first_board_stock.get('can_fuban', False)
    
    # 最终信号
    result["最终信号"] = result["情绪冰点"] and result["逆势首板"]
    
    return result

# ============ 4. 生成报告 ============
def generate_report(market_status, rise_result=None, ice_result=None):
    """
    生成复盘分析报告
    """
    report = []
    report.append("=" * 50)
    report.append("双系统复盘分析报告")
    report.append(f"时间: {datetime.now().strftime('%Y-%m-%d')}")
    report.append("=" * 50)
    
    # 第一步：市场诊断
    status, desc = market_status
    report.append(f"\n【第一步：市场状态诊断】")
    report.append(f"当前状态: {status} - {desc}")
    
    if status == "A":
        report.append("\n【第二步：主升系统验证】")
        if rise_result:
            report.append(f"1. 指数强趋势: {'是' if rise_result.get('指数强趋势') else '否'}")
            report.append(f"2. 板块共振: {'是' if rise_result.get('板块共振') else '否'}")
            report.append(f"3. 个股信号: {'是' if rise_result.get('个股信号') else '否'}")
            report.append(f"4. 失败压制: {'是' if rise_result.get('失败压制') else '否'}")
            signal = "是" if rise_result.get('最终信号') else "否"
            report.append(f"\n→ 主升系统信号: {signal}")
        
        report.append("\n【第三步：机会清单】")
        report.append("主升机会（按系统筛选）:")
        report.append("代码 | 名称 | 逻辑 | 买点")
        report.append("-" * 40)
        
        report.append("\n【第四步：明日操作纪律】")
        report.append("可开仓，重点观察XX股，止损位设于XX")
        
    elif status == "B":
        report.append("\n【第二步：冰点系统验证】")
        if ice_result:
            report.append(f"1. 情绪冰点: {'是' if ice_result.get('情绪冰点') else '否'}")
            report.append(f"2. 逆势首板: {'是' if ice_result.get('逆势首板') else '否'}")
            report.append(f"3. 强逻辑: {'是' if ice_result.get('强逻辑') else '否'}")
            report.append(f"4. 转强确认: {'是' if ice_result.get('转强确认') else '否'}")
            signal = "是" if ice_result.get('最终信号') else "否"
            report.append(f"\n→ 冰点系统信号: {signal}")
        
        report.append("\n【第三步：机会清单】")
        report.append("冰点机会（轻仓试错）:")
        report.append("代码 | 名称 | 先锋属性 | 仓位")
        report.append("-" * 40)
        
        report.append("\n【第四步：明日操作纪律】")
        report.append("轻仓试错XX股，若开盘<-3%则放弃")
        
    else:
        report.append("\n【第二步~第四步】")
        report.append("混沌观望期，双系统均不触发")
        report.append("\n【操作纪律】")
        report.append("空仓等待，市场明朗后再操作")
    
    report.append("\n【第五步：风险提示】")
    report.append("1. (待根据实际数据分析)")
    report.append("2. (待根据实际数据分析)")
    
    report.append("\n" + "=" * 50)
    
    return "\n".join(report)

# ============ 主测试 ============
if __name__ == "__main__":
    # 模拟数据测试
    print("=== 双系统复盘分析模型 ===\n")
    
    # 模拟市场诊断
    market_status = ("A", "强趋势主升市")
    print(generate_report(market_status))
    
    print("\n使用方法:")
    print("from models.dual_system import diagnose_market, generate_report")
    print("status, desc = diagnose_market(index_df, emotion_data)")
    print("report = generate_report((status, desc), rise_result, ice_result)")
