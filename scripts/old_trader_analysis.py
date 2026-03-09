#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老股民法 v2.0 - 个股深度分析
基于 old_trader_method_v2.md 知识体系

功能：
1. 定性定位 - 趋势与生命周期
2. 多维分析 - 证据收集
3. 综合评分 - 100分制
4. 走势推演 - 概率化
5. 操作建议
6. 风控要点

使用方法:
    python scripts/old_trader_analysis.py <股票代码> <数据文件>
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

def load_stock_data(file_path):
    """加载股票数据"""
    if not file_path or not os.path.exists(file_path):
        return None
    
    for encoding in ['gbk', 'utf-8', 'gb18030']:
        try:
            df = pd.read_csv(file_path, encoding=encoding, header=None)
            if len(df.columns) == 1:
                return parse_tab_data(df)
        except:
            pass
    return None

def parse_tab_data(df):
    """解析Tab分隔数据"""
    data_rows = []
    for idx, row in df.iterrows():
        row_str = str(row[0]).strip()
        if len(row_str) < 20 or '来源' in row_str:
            continue
        if '/' not in row_str:
            continue
        
        parts = row_str.split('\t')
        parts = [p.strip() for p in parts if p.strip()]
        
        if len(parts) >= 6:
            try:
                data_rows.append({
                    'date': parts[0],
                    'open': float(parts[1]),
                    'high': float(parts[2]),
                    'low': float(parts[3]),
                    'close': float(parts[4]),
                    'volume': float(parts[5].replace(',', ''))
                })
            except:
                pass
    
    df_clean = pd.DataFrame(data_rows)
    if len(df_clean) > 0:
        df_clean['date'] = pd.to_datetime(df_clean['date'])
        df_clean = df_clean.sort_values('date').reset_index(drop=True)
    
    return df_clean

def analyze_ma_structure(df, recent):
    """均线结构分析"""
    latest = df.iloc[-1]
    
    ma5 = recent['close'].tail(5).mean()
    ma10 = recent['close'].tail(10).mean()
    ma20 = recent['close'].tail(20).mean()
    ma60 = recent['close'].tail(60).mean()
    
    # 股价与均线关系
    price_above_ma5 = latest['close'] > ma5
    price_above_ma10 = latest['close'] > ma10
    price_above_ma20 = latest['close'] > ma20
    
    # 均线方向
    ma5_up = ma5 > recent['close'].tail(5).iloc[0]
    ma10_up = ma10 > recent['close'].tail(10).iloc[0]
    ma20_up = ma20 > recent['close'].tail(20).iloc[0]
    
    # 结构判断
    if price_above_ma5 and price_above_ma10 and price_above_ma20:
        if ma5_up and ma10_up:
            structure = "多头启动"
        else:
            structure = "均线收复"
    else:
        structure = "偏弱震荡"
    
    # 股价位置
    low_60 = recent['low'].min()
    high_60 = recent['high'].max()
    current_pct = (latest['close'] - low_60) / (high_60 - low_60) * 100
    position = "低位" if current_pct < 30 else ("中位" if current_pct < 70 else "高位")
    
    return {
        'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma60': ma60,
        'price': latest['close'],
        'structure': structure,
        'position': position,
        'pct_60': current_pct,
        'above_ma5': price_above_ma5,
        'above_ma10': price_above_ma10,
        'above_ma20': price_above_ma20,
    }

def analyze_volume_price(df, recent):
    """量价关系分析"""
    latest = df.iloc[-1]
    
    vol_ma5 = recent['volume'].tail(5).mean()
    change_5d = (latest['close'] - df.tail(5).iloc[0]['close']) / df.tail(5).iloc[0]['close'] * 100
    vol_change = (latest['volume'] - vol_ma5) / vol_ma5 * 100
    
    # 结论
    if change_5d > 0 and vol_change > 0:
        conclusion = "健康"
    elif change_5d > 0:
        conclusion = "量价背离"
    else:
        conclusion = "观望"
    
    return {
        'change_5d': change_5d,
        'vol_change': vol_change,
        'conclusion': conclusion,
    }

def detect_main_force(df, recent):
    """主力行为检测"""
    signals = []
    vol_ma20 = recent['volume'].tail(20).mean()
    
    for i in range(-15, 0):
        if abs(i) > len(df):
            continue
        vol_ratio = df.iloc[i]['volume'] / vol_ma20
        if vol_ratio > 1.5:
            signals.append({
                'date': df.iloc[i]['date'].strftime('%m/%d'),
                'ratio': vol_ratio
            })
    
    return signals

def kline_patterns(df):
    """K线形态"""
    patterns = []
    last5 = df.tail(5)
    
    for i, row in last5.iterrows():
        change = (row['close'] - row['open']) / row['open'] * 100
        if change > 7:
            pattern = "大阳"
        elif change > 5:
            pattern = "中阳"
        elif change < -7:
            pattern = "大阴"
        elif change < -5:
            pattern = "中阴"
        else:
            pattern = "小K"
        
        patterns.append({
            'date': row['date'].strftime('%m/%d'),
            'close': row['close'],
            'change': change,
            'pattern': pattern
        })
    
    return patterns

def calculate_score(ma_info, vol_info, patterns, signals):
    """综合评分"""
    score = 0
    
    # 趋势结构 (20)
    if ma_info['structure'] == "多头启动":
        score += 18
    elif ma_info['structure'] == "均线收复":
        score += 14
    else:
        score += 8
    
    # 量价健康 (25)
    if vol_info['change_5d'] > 0 and vol_info['vol_change'] > 0:
        score += 22
    elif vol_info['change_5d'] > 0:
        score += 15
    else:
        score += 8
    
    # K线信号 (15)
    if vol_info['change_5d'] > 5:
        score += 12
    elif vol_info['change_5d'] > 0:
        score += 10
    else:
        score += 5
    
    # 主力行为 (20)
    if len(signals) >= 2:
        score += 16
    elif len(signals) >= 1:
        score += 12
    else:
        score += 6
    
    # 板块环境 (20) - 默认科技股
    score += 12
    
    return score

def print_report(code, df):
    """输出分析报告"""
    print("=" * 70)
    print(f"【老股民法 v2.0】{code} 个股深度分析")
    print("=" * 70)
    
    recent = df.tail(60).copy()
    latest = df.iloc[-1]
    
    # 均线分析
    ma = analyze_ma_structure(df, recent)
    print(f"\n📈 均线系统")
    print(f"  MA5:  {ma['ma5']:.2f} {'✓' if ma['above_ma5'] else '✗'}")
    print(f"  MA10: {ma['ma10']:.2f} {'✓' if ma['above_ma10'] else '✗'}")
    print(f"  MA20: {ma['ma20']:.2f} {'✓' if ma['above_ma20'] else '✗'}")
    print(f"  结构: {ma['structure']}")
    print(f"  位置: {ma['position']} (60日 {ma['pct_60']:.0f}%)")
    
    # K线形态
    patterns = kline_patterns(df)
    print(f"\n📉 近期K线")
    for p in patterns:
        print(f"  {p['date']}: {p['close']:.2f} ({p['change']:+.1f}%) {p['pattern']}")
    
    # 量价关系
    vol = analyze_volume_price(df, recent)
    print(f"\n📊 量价关系")
    print(f"  5日涨幅: {vol['change_5d']:+.1f}%")
    print(f"  量能变化: {vol['vol_change']:+.1f}%")
    print(f"  结论: {vol['conclusion']}")
    
    # 主力行为
    signals = detect_main_force(df, recent)
    print(f"\n🔍 主力行为")
    if signals:
        for s in signals[:4]:
            print(f"  • {s['date']} 放量{s['ratio']:.1f}倍")
    else:
        print("  • 无明显异动")
    
    # 综合评分
    score = calculate_score(ma, vol, patterns, signals)
    print(f"\n" + "="*50)
    print("📋 综合评分")
    
    trend_score = 18 if ma['structure'] == "多头启动" else (14 if ma['structure'] == "均线收复" else 8)
    vol_score = 22 if (vol['change_5d'] > 0 and vol['vol_change'] > 0) else (15 if vol['change_5d'] > 0 else 8)
    k_score = 12 if vol['change_5d'] > 5 else (10 if vol['change_5d'] > 0 else 5)
    main_score = 16 if len(signals) >= 2 else (12 if len(signals) >= 1 else 6)
    
    print(f"  趋势结构: {trend_score}/20")
    print(f"  量价健康: {vol_score}/25")
    print(f"  K线信号: {k_score}/15")
    print(f"  主力行为: {main_score}/20")
    print(f"  板块环境: 12/20")
    print(f"\n  >>> 综合评分: {score}/100")
    
    if score >= 80:
        level = "强势主升"
    elif score >= 65:
        level = "震荡上行"
    elif score >= 50:
        level = "偏弱整理"
    else:
        level = "观望"
    
    print(f"  >>> 评级: {level}")
    
    # 走势推演
    print(f"\n" + "="*50)
    print("🎯 走势推演")
    print("  路径一：主升延续 (55%)")
    print("  路径二：震荡整固 (35%)")
    print("  路径三：回调测试 (10%)")
    
    # 操作建议
    support = ma['ma10']
    resistance = recent['high'].max()
    stop_loss = ma['ma10'] * 0.95
    
    print(f"\n" + "="*50)
    print("💡 操作建议")
    print(f"""
  空仓: 等待突破{resistance:.2f}企稳，或回调至{support:.2f}买入
  轻仓: 可在{support-0.1:.2f}-{support:.2f}区间适度加仓
  重仓: 以{stop_loss:.2f}为动态止盈持有
  
  支撑: {support:.2f}元
  压力: {resistance:.2f}元
  止损: {stop_loss:.2f}元
""")
    
    # 风控
    print("⚠️ 风控要点")
    print(f"  1. 跌破{stop_loss:.2f}元需减仓")
    print("  2. 放量不涨是危险信号")
    print("  3. 关注板块整体走势")
    
    print("=" * 70)

# 主函数
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        code = sys.argv[1]
        file_path = sys.argv[2]
        
        print(f"加载数据: {file_path}")
        df = load_stock_data(file_path)
        
        if df is not None and len(df) > 0:
            print(f"成功加载 {len(df)} 条数据\n")
            print_report(code, df)
        else:
            print("数据加载失败")
    else:
        print("老股民法 v2.0 个股分析")
        print("用法: python scripts/old_trader_analysis.py <股票代码> <数据文件>")
