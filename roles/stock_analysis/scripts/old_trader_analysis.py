#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老股民法个股分析系统
基于多维技术分析的主力意图判断

使用方法:
    python3 old_trader_analysis.py <股票代码>
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============ 1. 数据获取 ============
def get_stock_data(code: str, days: int = 120):
    """获取股票数据"""
    try:
        from stock_data_v3 import get_stock_history
        df, source = get_stock_history(code, "2025-01-01")
        
        if df is not None and not df.empty:
            # 处理列名
            df = df.rename(columns={
                'date': 'date', 'open': 'open', 'high': 'high',
                'low': 'low', 'close': 'close', 'volume': 'volume',
                'amount': 'amount', 'turn': 'turn', 'pctChg': 'change_pct'
            })
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').tail(days)
            return df, source
    except Exception as e:
        print(f"数据获取失败: {e}")
    return None, "none"

# ============ 2. 均线分析 ============
def analyze_ma(df: pd.DataFrame):
    """均线结构分析"""
    df = df.copy()
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean() if len(df) >= 60 else df['ma20']
    
    latest = df.iloc[-1]
    
    # 均线结构判断
    ma_struct = "震荡"
    if (latest['ma5'] > latest['ma10'] > latest['ma20'] and 
        latest['ma20'] > latest['ma60']):
        ma_struct = "多头"
    elif (latest['ma5'] < latest['ma10'] < latest['ma20'] and 
          latest['ma20'] < latest['ma60']):
        ma_struct = "空头"
    
    # 均线斜率
    ma20_slope = (latest['ma20'] - df['ma20'].iloc[-5]) / df['ma20'].iloc[-5] * 100 if len(df) >= 5 else 0
    
    return {
        "structure": ma_struct,
        "ma5": latest['ma5'],
        "ma10": latest['ma10'],
        "ma20": latest['ma20'],
        "ma60": latest['ma60'],
        "slope": ma20_slope,
        "current_price": latest['close'],
        "price_vs_ma5": (latest['close'] - latest['ma5']) / latest['ma5'] * 100
    }

# ============ 3. 量价关系分析 ============
def analyze_volume_price(df: pd.DataFrame):
    """量价关系分析"""
    df = df.copy()
    df['vol_ma5'] = df['volume'].rolling(5).mean()
    df['vol_ma20'] = df['volume'].rolling(20).mean()
    
    latest = df.iloc[-1]
    
    # 放量/缩量判断
    vol_ratio = latest['volume'] / latest['vol_ma5'] if latest['vol_ma5'] > 0 else 1
    
    # 近期量价配合
    recent = df.tail(10)
    up_days = recent[recent['change_pct'] > 0]
    down_days = recent[recent['change_pct'] < 0]
    
    up_vol_avg = up_days['volume'].mean() if len(up_days) > 0 else 0
    down_vol_avg = down_days['volume'].mean() if len(down_days) > 0 else 0
    
    # 量价健康度
    if up_vol_avg > down_vol_avg * 1.2:
        vol_price_health = "健康（上涨放量，下跌缩量）"
        health_score = 25
    elif up_vol_avg < down_vol_avg * 0.8:
        vol_price_health = "异常（上涨缩量，下跌放量）"
        health_score = 10
    else:
        vol_price_health = "一般"
        health_score = 15
    
    return {
        "vol_ratio": vol_ratio,
        "up_vol": up_vol_avg,
        "down_vol": down_vol_avg,
        "health": vol_price_health,
        "score": health_score
    }

# ============ 4. K线形态分析 ============
def analyze_kline(df: pd.DataFrame):
    """K线形态分析"""
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    signals = []
    score = 0
    
    # 实体大小
    body = abs(latest['close'] - latest['open'])
    range_ = latest['high'] - latest['low']
    body_ratio = body / range_ if range_ > 0 else 0
    
    if body_ratio > 0.8:
        signals.append("大阳线/大阴线")
        if latest['change_pct'] > 5:
            signals.append("强势信号")
            score += 5
    
    # 上下影线
    upper_shadow = latest['high'] - max(latest['open'], latest['close'])
    lower_shadow = min(latest['open'], latest['close']) - latest['low']
    
    if upper_shadow > body * 0.5:
        signals.append("长上影线（试盘/压力）")
        score -= 3
    if lower_shadow > body * 0.5:
        signals.append("长下影线（支撑/吸筹）")
        score += 3
    
    # 连续K线
    if len(df) >= 3:
        recent3 = df.tail(3)
        if all(recent3['close'] > recent3['open']):
            signals.append("连续上涨")
            score += 5
        elif all(recent3['close'] < recent3['open']):
            signals.append("连续下跌")
            score -= 3
    
    return {
        "signals": signals,
        "body_ratio": body_ratio,
        "score": max(0, min(15, score))
    }

# ============ 5. 股价位置分析 ============
def analyze_price_position(df: pd.DataFrame):
    """股价位置分析"""
    high_60 = df['high'].tail(60).max()
    low_60 = df['low'].tail(60).min()
    current = df.iloc[-1]['close']
    
    position = (current - low_60) / (high_60 - low_60) * 100 if high_60 > low_60 else 50
    
    # 位置判断
    if position < 30:
        position_status = "低位（吸筹区）"
    elif position < 70:
        position_status = "中位（换手/洗盘）"
    else:
        position_status = "高位（派发风险）"
    
    return {
        "position_pct": position,
        "status": position_status,
        "high_60": high_60,
        "low_60": low_60
    }

# ============ 6. 主力行为判断 ============
def analyze_main_force(df: pd.DataFrame):
    """主力行为定性分析"""
    recent = df.tail(20)
    
    # 资金流向估算（简单版）
    price_change = recent['close'].iloc[-1] - recent['close'].iloc[0]
    vol_change = recent['volume'].sum() / recent['volume'].iloc[:-20].sum() if len(recent) > 20 else 1
    
    # 主力行为判断
    behavior = "震荡整理"
    score = 10
    
    # 吸筹特征
    if (vol_change > 1.3 and price_change > 10):
        behavior = "吸筹/建仓"
        score = 15
    elif (vol_change > 1.5 and price_change > 20):
        behavior = "拉升开始"
        score = 20
    elif (vol_change > 1.2 and price_change < -10):
        behavior = "派发/出货"
        score = 5
    
    return {
        "behavior": behavior,
        "score": score,
        "vol_change": vol_change,
        "price_change": price_change
    }

# ============ 7. 综合评分 ============
def comprehensive_score(ma_score, vol_score, kline_score, position_score, force_score):
    """综合评分"""
    # 趋势结构: 20分
    trend_map = {"多头": 20, "震荡": 12, "空头": 5}
    trend_score = trend_map.get(ma_score["structure"], 10)
    
    # 量价健康度: 25分 (已计算)
    
    # K线信号: 15分 (已计算)
    
    # 主力行为: 20分 (已计算)
    
    # 股价位置: 20分
    pos_score = 20 - (position_score["position_pct"] / 100 * 15)  # 低位高分
    
    total = trend_score + vol_score + kline_score + pos_score + force_score
    
    if total >= 80:
        conclusion = "强势主升结构"
        action = "可积极做多"
    elif total >= 60:
        conclusion = "可操作，但需择时"
        action = "等待更好买点"
    else:
        conclusion = "观望为主"
        action = "不建议操作"
    
    return {
        "total": total,
        "trend": trend_score,
        "volume_price": vol_score,
        "kline": kline_score,
        "position": pos_score,
        "main_force": force_score,
        "conclusion": conclusion,
        "action": action
    }

# ============ 8. 输出报告 ============
def generate_report(code: str, df: pd.DataFrame):
    """生成分析报告"""
    print("\n" + "="*60)
    print(f"  老股民法个股分析 - {code}")
    print("="*60)
    
    # 各维度分析
    ma_info = analyze_ma(df)
    vol_info = analyze_volume_price(df)
    kline_info = analyze_kline(df)
    position_info = analyze_price_position(df)
    force_info = analyze_main_force(df)
    
    # 综合评分
    score_result = comprehensive_score(ma_info, vol_info, kline_info, position_info, force_info)
    
    # 输出
    print(f"\n【1. 均线结构】{ma_info['structure']}")
    print(f"  MA5: {ma_info['ma5']:.2f} MA10: {ma_info['ma10']:.2f}")
    print(f"  MA20: {ma_info['ma20']:.2f} MA60: {ma_info['ma60']:.2f}")
    print(f"  股价相对MA5: {ma_info['price_vs_ma5']:.1f}%")
    
    print(f"\n【2. 量价关系】{vol_info['health']}")
    print(f"  量比: {vol_info['vol_ratio']:.2f}")
    print(f"  上涨日均量: {vol_info['up_vol']:.0f}")
    print(f"  下跌日均量: {vol_info['down_vol']:.0f}")
    
    print(f"\n【3. K线形态】")
    print(f"  信号: {', '.join(kline_info['signals']) if kline_info['signals'] else '无明显信号'}")
    
    print(f"\n【4. 股价位置】{position_info['status']}")
    print(f"  60日区间位置: {position_info['position_pct']:.1f}%")
    
    print(f"\n【5. 主力行为】{force_info['behavior']}")
    
    print("\n" + "-"*60)
    print(f"【综合评分】{score_result['total']}/100")
    print(f"  趋势结构: {score_result['trend']}/20")
    print(f"  量价健康: {score_result['volume_price']}/25")
    print(f"  K线信号: {score_result['kline']}/15")
    print(f"  股价位置: {score_result['position']:.0f}/20")
    print(f"  主力行为: {score_result['main_force']}/20")
    
    print("\n" + "="*60)
    print(f"【结论】{score_result['conclusion']}")
    print(f"【建议】{score_result['action']}")
    print("="*60 + "\n")
    
    return score_result

# ============ 主程序 ============
if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "000001"
    
    print(f"正在分析 {code} ...")
    df, source = get_stock_data(code)
    
    if df is not None:
        print(f"数据源: {source}, 数据量: {len(df)}")
        result = generate_report(code, df)
    else:
        print("获取数据失败")
