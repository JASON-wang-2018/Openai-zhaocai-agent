#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高胜率选股模型 v3.0
主升 + 冰点反转 双系统
"""

import numpy as np
import pandas as pd
from datetime import datetime

# ============ 1. 市场环境判断 ============
def check_market_trend(index_data):
    """
    第一层：市场强趋势确认
    返回: (是否符合, 趋势描述)
    """
    if index_data is None or len(index_data) < 60:
        return False, "数据不足"
    
    closes = index_data['close'].astype(float).values
    ma20 = np.mean(closes[-20:])
    ma60 = np.mean(closes[-60:])
    ma10 = np.mean(closes[-10:])
    prev_ma20 = np.mean(closes[-21:-1])
    
    # 条件1: MA20 > MA60
    cond1 = ma20 > ma60
    # 条件2: MA20向上
    cond2 = ma20 > prev_ma20
    # 条件3: 价格在MA10之上
    cond3 = closes[-1] > ma10
    
    if cond1 and cond2 and cond3:
        return True, "强上升趋势"
    elif cond1 and not cond2:
        return False, "震荡整理"
    else:
        return False, "下降趋势"

# ============ 2. 板块强度判断 ============
def check_sector_strength(stock_data, index_data):
    """
    第二层：主线板块锁定
    返回: (板块强度得分, 0-100)
    """
    if stock_data is None or index_data is None:
        return 0
    
    stock_change = stock_data.get('change_pct', 0)
    index_change = index_data.get('change_pct', 0)
    
    # 强于指数 5%
    strength = (stock_change - index_change) * 10  # 超过5%得50分
    
    return max(0, min(100, 50 + strength))

# ============ 3. 龙头特征判断 ============
def check_leader特征(df):
    """
    第三层：龙头优先机制
    返回: (是否符合, 特征描述)
    """
    if df is None or len(df) < 5:
        return False, "数据不足"
    
    closes = df['收盘'].astype(float).values
    highs = df['最高'].astype(float).values
    volumes = df['成交量'].astype(float).values
    
    # 近5日新高
    high_5 = np.max(highs[-5:])
    is_new_high = closes[-1] >= high_5
    
    # 涨停强度（5日内有涨停）
    # 简单判断：涨幅>9%视为涨停
    has_limit_up = any((closes[i]/closes[i-1] - 1) > 0.095 for i in range(1, len(closes)))
    
    if is_new_high and has_limit_up:
        return True, "龙头特征"
    elif is_new_high:
        return True, "新高股"
    elif has_limit_up:
        return True, "涨停股"
    
    return False, "普通股"

# ============ 4. 量价强一致 ============
def check_volume_price(df):
    """
    第四层：量价强一致
    放量突破 + 回调缩量
    """
    if df is None or len(df) < 10:
        return False, "数据不足"
    
    closes = df['收盘'].astype(float).values
    volumes = df['成交量'].astype(float).values
    
    # 放量突破10日高点
    high_10 = np.max(highs[-10:]) if '最高' in df.columns else np.max(closes[-10:])
    vol_ma10 = np.mean(volumes[-10:])
    
    cond1 = closes[-1] > high_10  # 突破
    cond2 = volumes[-1] > vol_ma10 * 1.5  # 放量
    
    # 回调缩量（近3日有回调且缩量）
    cond3 = False
    for i in range(-3, 0):
        if closes[i] < closes[i-1] and volumes[i] < vol_ma10 * 0.7:
            cond3 = True
            break
    
    if cond1 and cond2:
        if cond3:
            return True, "量价强一致"
        else:
            return True, "放量突破"
    
    return False, "量价一般"

# ============ 5. 分歧转强判断 ============
def check_divergence_confirm(df):
    """
    第五层：分歧确认买点
    第一天分歧，第二天转强
    """
    if df is None or len(df) < 3:
        return False, "数据不足"
    
    closes = df['收盘'].astype(float).values
    highs = df['最高'].astype(float).values if '最高' in df.columns else closes
    volumes = df['成交量'].astype(float).values
    
    vol_ma10 = np.mean(volumes[-10:])
    
    # 昨天：分歧日（冲高回落）
    yesterday_up = closes[-2] > closes[-3]  # 上涨
    yesterday_high_retrace = highs[-2] > closes[-2] * 1.02  # 上影线
    yesterday_vol = volumes[-2] > vol_ma10 * 1.2  # 放量
    
    is_divergence = yesterday_up and yesterday_high_retrace and yesterday_vol
    
    # 今天：转强（突破昨日高点）
    today_break = closes[-1] > highs[-2]
    today_above_ma5 = closes[-1] > np.mean(closes[-5:])
    
    is_confirm = today_break and today_above_ma5
    
    if is_divergence and is_confirm:
        return True, "分歧转强确认"
    elif is_divergence:
        return True, "分歧日（待确认）"
    
    return False, "非分歧结构"

# ============ 6. 失败压制过滤 ============
def check_failure_filters(df):
    """
    第六层：失败压制过滤
    三条硬杀规则
    """
    if df is None or len(df) < 5:
        return True, "数据不足，无法过滤"
    
    closes = df['收盘'].astype(float).values
    volumes = df['成交量'].astype(float).values
    vol_ma10 = np.mean(volumes[-10:])
    
    # 规则1: 连续3日放量滞涨
    cond1 = True
    for i in range(-3, 0):
        if not (volumes[i] > vol_ma10 and abs(closes[i] - closes[i-1]) < closes[i-1] * 0.02):
            cond1 = False
            break
    
    # 规则2: 高位加速过大（位置>80%）
    price_range = max(closes[-20:]) - min(closes[-20:])
    position = (closes[-1] - min(closes[-20:])) / price_range * 100 if price_range > 0 else 50
    cond2 = position > 80
    
    # 规则3: 单日巨量阴
    cond3 = volumes[-1] > vol_ma10 * 2 and closes[-1] < closes[-2]
    
    if cond1:
        return False, "失败过滤: 连续3日放量滞涨"
    if cond2:
        return False, "失败过滤: 高位加速过大"
    if cond3:
        return False, "失败过滤: 单日巨量阴"
    
    return True, "通过过滤"

# ============ 7. 综合选股评分 ============
def comprehensive_score(stock_data, df, index_data=None):
    """
    综合评分（100分制）
    """
    score = 0
    reasons = []
    
    # 第一层：市场环境（20分）
    market_ok, market_desc = check_market_trend(index_data)
    if market_ok:
        score += 20
        reasons.append(f"市场:{market_desc}")
    
    # 第二层：板块强度（15分）
    sector_score = check_sector_strength(stock_data, index_data)
    score += int(sector_score * 0.15)
    if sector_score > 60:
        reasons.append(f"板块强:{sector_score:.0f}")
    
    # 第三层：龙头特征（20分）
    leader_ok, leader_desc = check_leader特征(df)
    if leader_ok:
        score += 20
        reasons.append(f"龙头:{leader_desc}")
    
    # 第四层：量价（15分）
    vp_ok, vp_desc = check_volume_price(df)
    if vp_ok:
        score += 15
        reasons.append(f"量价:{vp_desc}")
    
    # 第五层：分歧确认（20分）
    div_ok, div_desc = check_divergence_confirm(df)
    if div_ok:
        score += 20
        reasons.append(f"买点:{div_desc}")
    
    # 第六层：过滤（扣分）
    filter_ok, filter_desc = check_failure_filters(df)
    if not filter_ok:
        score = 0
        reasons.append(f"过滤:{filter_desc}")
    
    return score, reasons

# ============ 8. 冰点反转模型 ============
def check_ice_reversal(ice_data):
    """
    冰点反转条件
    适用于弱势市场
    """
    if ice_data is None:
        return False, "无冰点数据"
    
    limit_up = ice_data.get('limit_up_count', 100)
    limit_down = ice_data.get('limit_down_count', 0)
    highest板 = ice_data.get('highest连板', 10)
    
    # 冰点条件
    is_ice = limit_up < 20 and limit_down > 30
    
    # 反转条件
    if is_ice:
        # 超跌反弹
        return True, "冰点反转机会"
    
    return False, "非冰点"

# ============ 主测试 ============
if __name__ == "__main__":
    # 模拟测试
    print("=== 高胜率选股模型 v3.0 ===")
    print("各模块待接入实时数据后运行")
    print("\n使用方法:")
    print("from models.high_winrate import comprehensive_score")
    print("score, reasons = comprehensive_score(stock_data, kline_df, index_data)")
