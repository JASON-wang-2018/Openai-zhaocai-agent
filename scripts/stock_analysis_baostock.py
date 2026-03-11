#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股每日分析脚本 - Baostock版 v3.0
稳定获取数据，技术面 + 主力行为分析
"""
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/scripts')
import baostock_data as bd
from datetime import datetime

def analyze_tech(df, name):
    """系统1：技术面分析"""
    if df is None or len(df) < 120:
        return None
    
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # 计算均线
    df_with_ma = bd.calculate_ma(df, periods=[5, 10, 20, 60, 120])
    
    ma5 = df_with_ma.iloc[-1]['MA5']
    ma10 = df_with_ma.iloc[-1]['MA10']
    ma20 = df_with_ma.iloc[-1]['MA20']
    ma60 = df_with_ma.iloc[-1]['MA60']
    ma120 = df_with_ma.iloc[-1]['MA120']
    
    # 趋势判断
    above_ma5 = df_with_ma.iloc[-1]['close'] > ma5
    above_ma10 = df_with_ma.iloc[-1]['close'] > ma10
    above_ma20 = df_with_ma.iloc[-1]['close'] > ma20
    above_ma60 = df_with_ma.iloc[-1]['close'] > ma60
    above_ma120 = df_with_ma.iloc[-1]['close'] > ma120
    
    # 多头排列：5>10>20>60
    bull_arrange = (ma5 > ma10 > ma20 > ma60) if ma60 else False
    
    # 5日涨跌幅
    if len(df_with_ma) >= 5:
        change_5d = (df_with_ma.iloc[-1]['close'] - df_with_ma.iloc[-5]['close']) / df_with_ma.iloc[-5]['close'] * 100
    else:
        change_5d = 0
    
    # 成交量变化
    vol_5d_avg = df_with_ma['volume'].tail(5).mean()
    vol_now = df_with_ma.iloc[-1]['volume']
    vol_change = (vol_now - vol_5d_avg) / vol_5d_avg * 100 if vol_5d_avg else 0
    
    return {
        'name': name,
        'close': round(latest['close'], 2),
        'volume': latest['volume'],
        'change_5d': round(change_5d, 2),
        'vol_change': round(vol_change, 1),
        'ma5': round(ma5, 2),
        'ma10': round(ma10, 2),
        'ma20': round(ma20, 2),
        'ma60': round(ma60, 2),
        'ma120': round(ma120, 2),
        'above_ma5': above_ma5,
        'above_ma10': above_ma10,
        'above_ma20': above_ma20,
        'above_ma60': above_ma60,
        'above_ma120': above_ma120,
        'bull_arrange': bull_arrange,
        '10日线法则': '持股' if df_with_ma.iloc[-1]['close'] > ma10 else '持币'
    }

def analyze_mainforce(df, name):
    """系统2：主力行为分析"""
    if df is None or len(df) < 10:
        return None
    
    latest = df.iloc[-1]
    vol_now = latest['volume']
    
    # 量价关系分析
    if len(df) >= 10:
        avg_vol = df['volume'].tail(10).mean()
        vol_ratio = vol_now / avg_vol if avg_vol else 1
    else:
        vol_ratio = 1
    
    # 涨跌幅
    price_change = (latest['close'] - df.iloc[-2]['close']) / df.iloc[-2]['close'] * 100 if len(df) > 1 else 0
    
    # 量价信号
    if vol_ratio > 1.2 and price_change > 0:
        vol_price_signal = '放量上涨 ✅'
    elif vol_ratio > 1.2 and price_change < 0:
        vol_price_signal = '放量下跌 ⚠️'
    elif vol_ratio < 0.8 and price_change > 0:
        vol_price_signal = '缩量上涨 ⚠️量价背离'
    elif vol_ratio < 0.8 and price_change < 0:
        vol_price_signal = '缩量下跌 📉'
    else:
        vol_price_signal = '横盘整理 ➡️'
    
    # 创新高/新低
    high_60 = df['high'].tail(60).max() if len(df) >= 60 else df['high'].max()
    low_60 = df['low'].tail(60).min() if len(df) >= 60 else df['low'].min()
    near_high = latest['close'] / high_60 > 0.95 if high_60 else False
    near_low = latest['close'] / low_60 < 1.05 if low_60 else False
    
    # 持仓量估算
    if len(df) >= 20:
        turnover_20d = df['volume'].tail(20).sum() / (latest['volume'] * 20) if latest['volume'] else 0
        estimated_holding = min(turnover_20d * 13.3 / 100, 1.0)
    else:
        estimated_holding = 0
    
    # 控盘程度
    if estimated_holding < 0.2:
        控盘程度 = '无行情'
    elif estimated_holding < 0.4:
        控盘程度 = '短线活跃'
    elif estimated_holding < 0.6:
        控盘程度 = '中线拉升期 ⭐'
    else:
        控盘程度 = '长线控盘 🐴'
    
    return {
        'vol_ratio': round(vol_ratio, 2),
        'price_change': round(price_change, 2),
        'vol_price_signal': vol_price_signal,
        'near_high': near_high,
        'near_low': near_low,
        'estimated_holding': round(estimated_holding * 100, 1),
        '控盘程度': 控盘程度
    }

def generate_report():
    """生成完整分析报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n{'='*60}")
    print(f"📊 A股市场分析报告 {today} (Baostock)")
    print(f"{'='*60}\n")
    
    # 主要指数（科创50数据较少，改用上证50）
    indices = [
        ('sh.000001', '上证指数'),
        ('sh.000300', '沪深300'),
        ('sz.399001', '深证成指'),
        ('sz.399006', '创业板指'),
        ('sh.000016', '上证50')
    ]
    
    results = []
    
    for code, name in indices:
        print(f"📈 {name}...", end=" ", flush=True)
        df = bd.get_index_daily(code, days=200)
        
        if df is None or len(df) < 120:
            print("❌ 数据获取失败")
            continue
        
        tech = analyze_tech(df, name)
        mainforce = analyze_mainforce(df, name)
        
        if tech and mainforce:
            print(f"✅ {tech['close']}")
            
            print(f"   收盘: {tech['close']} | 5日涨跌: {tech['change_5d']:+.2f}%")
            print(f"   成交量: {'🔺放大' if tech['vol_change'] > 10 else '🔻萎缩'} {tech['vol_change']:+.1f}%")
            print(f"   ---技术面---")
            print(f"   MA120: {tech['ma120']} | {'✅站上' if tech['above_ma120'] else '❌跌破'}")
            print(f"   10日线法则: {tech['10日线法则']}")
            print(f"   多头排列: {'✅是' if tech['bull_arrange'] else '❌否'}")
            print(f"   ---主力行为---")
            print(f"   量价信号: {mainforce['vol_price_signal']}")
            print(f"   估算持仓量: {mainforce['estimated_holding']:.1f}% ({mainforce['控盘程度']})")
            print()
            
            results.append({'tech': tech, 'mainforce': mainforce})
    
    # 综合判断
    print(f"{'='*60}")
    print("📋 综合判断")
    print(f"{'='*60}")
    
    if results:
        above_ma120_count = sum(1 for r in results if r['tech']['above_ma120'])
        bull_count = sum(1 for r in results if r['tech']['bull_arrange'])
        
        print(f"  • 站上MA120: {above_ma120_count}/{len(results)}")
        print(f"  • 多头排列: {bull_count}/{len(results)}")
        
        # 风险提示
        warning_signs = []
        for r in results:
            if '⚠️' in r['mainforce']['vol_price_signal']:
                warning_signs.append(f"{r['tech']['name']}量价背离")
            if r['tech']['change_5d'] < -5:
                warning_signs.append(f"{r['tech']['name']}本周跌超5%")
        
        if warning_signs:
            print(f"\n⚠️ 风险提示:")
            for w in warning_signs:
                print(f"  - {w}")
    
    print(f"\n{'='*60}")
    print("数据来源: Baostock (完全免费)")
    
    return results

if __name__ == '__main__':
    generate_report()
