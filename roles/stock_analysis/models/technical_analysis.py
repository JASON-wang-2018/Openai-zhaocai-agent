#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票技术分析模型
包含：K线形态识别、均线、RSI、MACD、量价关系分析
"""

import json
from datetime import datetime

# ============ 1. 均线系统 ============
def calculate_ma(prices, period):
    """计算移动平均线"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def analyze_ma_trend(ma5, ma10, ma20):
    """均线趋势分析"""
    if ma5 > ma10 > ma20:
        return "多头排列", "看涨"
    elif ma5 < ma10 < ma20:
        return "空头排列", "看跌"
    elif ma5 > ma20:
        return "偏多震荡", "谨慎看涨"
    else:
        return "偏空震荡", "谨慎看跌"

# ============ 2. RSI 计算 ============
def calculate_rsi(prices, period=14):
    """计算RSI指标"""
    if len(prices) < period + 1:
        return None
    
    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def analyze_rsi(rsi):
    """RSI分析"""
    if rsi > 80:
        return "超买区", "风险积累,考虑卖出"
    elif rsi < 20:
        return "超卖区", "机会显现,考虑买入"
    elif rsi > 50:
        return "偏多", "多头力量较强"
    else:
        return "偏空", "空头力量较强"

# ============ 3. MACD 计算 ============
def calculate_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD"""
    if len(prices) < slow:
        return None
    
    # 计算EMA
    def calc_ema(data, period):
        ema = [data[0]]
        multiplier = 2 / (period + 1)
        for i in range(1, len(data)):
            ema.append((data[i] - ema[-1]) * multiplier + ema[-1])
        return ema
    
    ema_fast = calc_ema(prices, fast)
    ema_slow = calc_ema(prices, slow)
    
    # DIF线
    dif = [ema_fast[i] - ema_slow[i] for i in range(len(ema_slow))]
    
    # DEA线
    dea = calc_ema(dif, signal)
    
    # MACD柱
    macd_bardif[i] - = [( dea[i]) * 2 for i in range(len(dea))]
    
    return {
        'dif': round(dif[-1], 4),
        'dea': round(dea4),
        '[-1], macd': round(macd_bar[-1], 4),
        'histogram': macd_bar[-5:]  # 最近5个
    }

def analyze_macd(macd_data):
    """MACD分析"""
    if not macd_data:
        return "数据不足"
    
    dif = macd_data['dif']
    dea = macd_data['dea']
    macd = macd_data['macd']
    
    if dif > dea > 0:
        return "多头金叉", "上涨趋势,持有"
    elif dif < dea < 0:
        return "空头死叉", "下跌趋势,观望"
    elif dif > dea:
        return "金叉初期", "可能启动,关注"
    else:
        return "死叉初期", "可能下跌,谨慎"
    
    # 背离检测
    if macd > 0 and macd > macd_data['histogram'][-2]:
        return "MACD红柱放大", "多头增强"

# ============ 4. K线形态 ============
def analyze_candle(open_price, close_price, high, low):
    """分析单根K线"""
    change_pct = (close_price - open_price) / open_price * 100
    body = abs(close_price - open_price)
    upper_shadow = high - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low
    total_range = high - low
    
    result = {
        'type': '阳线' if close > open else '阴线',
        'change_pct': round(change_pct, 2),
        'body_ratio': round(body / total_range * 100, 2) if total_range > 0 else 0,
    }
    
    # 形态识别
    if upper_shadow > body * 0.5 and lower_shadow < body * 0.3:
        result['pattern'] = '射击之星' if close < open else '倒锤线'
        result['signal'] = '看跌' if close < open else '可能反转'
    elif lower_shadow > body * 0.5 and upper_shadow < body * 0.3:
        result['pattern'] = '锤子线' if close > open else '吊颈线'
        result['signal'] = '看涨' if close > open else '可能反转'
    elif body / total_range < 0.2:
        result['pattern'] = '十字星'
        result['signal'] = '变盘信号'
    else:
        result['pattern'] = '普通K线'
        result['signal'] = '中性'
    
    return result

# ============ 5. 量价关系 ============
def analyze_volume_price(volumes, prices):
    """量价关系分析"""
    if len(volumes) < 5 or len(prices) < 5:
        return "数据不足"
    
    avg_vol = sum(volumes[-5:]) / 5
    current_vol = volumes[-1]
    vol_ratio = current_vol / avg_vol
    
    price_change = (prices[-1] - prices[-2]) / prices[-2] * 100
    
    # 量价配合分析
    if price_change > 0 and vol_ratio > 1.5:
        return "价涨量增", "健康上涨,多方积极"
    elif price_change > 0 and vol_ratio < 0.7:
        return "价涨量缩", "量价背离,可能见顶"
    elif price_change < 0 and vol_ratio > 1.5:
        return "价跌量增", "恐慌下跌,可能加速"
    elif price_change < 0 and vol_ratio < 0.7:
        return "价跌量缩", "卖盘惜售,可能见底"
    else:
        return "横盘整理", "观望为主"

# ============ 6. 综合评分模型 ============
def comprehensive_analysis(quote_data, history_data):
    """
    综合评分模型
    返回: (score, level, advice)
    score: 0-100
    level: 极差/较差/一般/良好/优秀
    """
    score = 50  # 基础分
    
    # 1. 趋势评分 (占30分)
    if len(history_data) >= 20:
        ma5 = calculate_ma(history_data['close'], 5)
        ma20 = calculate_ma(history_data['close'], 20)
        if ma5 and ma20:
            if ma5 > ma20 * 1.05:
                score += 20
                trend = "上升趋势"
            elif ma5 < ma20 * 0.95:
                score -= 15
                trend = "下降趋势"
            else:
                trend = "横盘震荡"
    
    # 2. 动量评分 (占25分)
    if len(history_data) >= 14:
        rsi = calculate_rsi(history_data['close'])
        if rsi:
            if rsi > 70:
                score -= 10
                rsi_msg = "RSI超买"
            elif rsi < 30:
                score += 15
                rsi_msg = "RSI超卖"
            else:
                rsi_msg = "RSI中性"
    
    # 3. MACD评分 (占20分)
    if len(history_data) >= 26:
        macd = calculate_macd(history_data['close'])
        if macd:
            if macd['dif'] > macd['dea'] and macd['macd'] > 0:
                score += 15
                macd_msg = "MACD金叉"
            elif macd['dif'] < macd['dea'] and macd['macd'] < 0:
                score -= 10
                macd_msg = "MACD死叉"
            else:
                macd_msg = "MACD震荡"
    
    # 4. 量价评分 (占15分)
    if len(history_data) >= 5:
        vp = analyze_volume_price(history_data['volume'][-5:], history_data['close'][-5:])
        if "价涨量增" in vp:
            score += 10
        elif "价跌量缩" in vp:
            score += 5
    
    # 5. 强度评分 (占10分)
    if quote_data.get('change_pct'):
        change = quote_data['change_pct']
        if change > 5:
            score += 5
        elif change < -5:
            score -= 5
    
    # 评级
    score = max(0, min(100, score))
    if score >= 85:
        level, advice = "优秀", "强烈买入"
    elif score >= 70:
        level, advice = "良好", "可以买入"
    elif score >= 50:
        level, advice = "一般", "观望为主"
    elif score >= 30:
        level, advice = "较差", "建议卖出"
    else:
        level, advice = "极差", "坚决卖出"
    
    return score, level, advice

# ============ 主测试 ============
if __name__ == "__main__":
    # 模拟数据测试
    prices = [10.0, 10.2, 10.1, 10.3, 10.5, 10.4, 10.6, 10.8, 11.0, 10.9,
              11.1, 11.3, 11.2, 11.5, 11.4, 11.6, 11.8, 12.0, 11.9, 12.1,
              12.3, 12.2, 12.5, 12.4, 12.6, 12.8]
    
    print("RSI:", calculate_rsi(prices))
    print("MA5:", calculate_ma(prices, 5))
    print("MA20:", calculate_ma(prices, 20))
    print("MACD:", calculate_macd(prices))
