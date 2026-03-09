#!/usr/bin/env python3
"""
A股每日分析脚本 - 双系统模型 v2.0
融合《一本书看透股市庄家》知识点
技术面 + 主力行为分析
"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def get_index_data(symbol):
    """获取指数数据"""
    try:
        df = ak.stock_zh_index_daily(symbol=symbol)
        return df
    except:
        return None

def calculate_ma(df, periods=[5, 10, 20, 60, 120]):
    """计算多条均线"""
    for p in periods:
        df[f'MA{p}'] = df['close'].rolling(window=p).mean()
    return df

def analyze_tech(df, name):
    """系统1：技术面分析"""
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # 均线多头排列
    ma5 = latest['MA5']
    ma10 = latest['MA10']
    ma20 = latest['MA20']
    ma60 = latest['MA60']
    ma120 = latest['MA120']
    
    # 趋势判断
    above_ma5 = latest['close'] > ma5
    above_ma10 = latest['close'] > ma10
    above_ma20 = latest['close'] > ma20
    above_ma60 = latest['close'] > ma60
    above_ma120 = latest['close'] > ma120
    
    # 多头排列：5>10>20>60
    bull排列 = (ma5 > ma10 > ma20 > ma60) if ma60 else False
    
    # 5日涨跌幅
    if len(df) >= 5:
        change_5d = (latest['close'] - df.iloc[-5]['close']) / df.iloc[-5]['close'] * 100
    else:
        change_5d = 0
    
    # 成交量变化
    vol_5d_avg = df['volume'].tail(5).mean()
    vol_now = latest['volume']
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
        'bull_arrange': bull排列,
        # 曹氏八线理论：10日线法则
        '10日线法则': '持股' if latest['close'] > ma10 else '持币'
    }

def analyze_mainforce(df, name):
    """系统2：主力行为分析"""
    latest = df.iloc[-1]
    
    # 换手率估算（假设流通盘与成交量关系）
    vol = latest['volume']
    
    # 量价关系分析
    if len(df) >= 10:
        avg_vol = df['volume'].tail(10).mean()
        vol_ratio = vol / avg_vol if avg_vol else 1
    else:
        vol_ratio = 1
    
    # 量价配合
    price_change = (latest['close'] - df.iloc[-2]['close']) / df.iloc[-2]['close'] * 100 if len(df) > 1 else 0
    
    # 放量上涨 = 健康
    # 放量下跌 = 危险
    # 缩量上涨 = 量价背离（可能诱多）
    # 缩量横盘 = 变盘前兆
    
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
    high_60 = df['high'].tail(60).max()
    low_60 = df['low'].tail(60).min()
    near_high = latest['close'] / high_60 > 0.95
    near_low = latest['close'] / low_60 < 1.05
    
    # 持仓量估算（换手率法）
    # 简略估算：近期换手率累积
    if len(df) >= 20:
        turnover_20d = df['volume'].tail(20).sum() / (latest['volume'] * 20) if latest['volume'] else 0
        # 估算持仓量 ≈ 换手率 × 13.3%
        estimated_holding = min(turnover_20d * 13.3 / 100, 1.0)
    else:
        estimated_holding = 0
    
    # 控盘程度判断
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
    print(f"📊 A股市场分析报告 {today}")
    print(f"{'='*60}\n")
    
    indices = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
        ('sh000688', '科创50')
    ]
    
    results = []
    
    for symbol, name in indices:
        df = get_index_data(symbol)
        if df is None or len(df) < 120:
            print(f"❌ {name}: 数据获取失败\n")
            continue
        
        df = calculate_ma(df.tail(130))
        
        tech = analyze_tech(df, name)
        mainforce = analyze_mainforce(df, name)
        
        print(f"📈 {tech['name']}")
        print(f"   收盘: {tech['close']} | 5日涨跌: {tech['change_5d']:+.2f}%")
        print(f"   成交量: {'🔺放大' if tech['vol_change'] > 10 else '🔻萎缩'} {tech['vol_change']:+.1f}%")
        print(f"   ---技术面---")
        print(f"   MA120: {tech['ma120']} | {'✅站上' if tech['above_ma120'] else '❌跌破'}")
        print(f"   10日线法则: {tech['10日线法则']}")
        print(f"   多头排列: {'✅是' if tech['bull_arrange'] else '❌否'}")
        print(f"   ---主力行为---")
        print(f"   量价信号: {mainforce['vol_price_signal']}")
        print(f"   估算持仓量: {mainforce['estimated_holding']:.1f}% ({mainforce['控盘程度']})")
        print(f"   距60日高点: {'✅接近' if mainforce['near_high'] else '否'}")
        print()
        
        results.append({'tech': tech, 'mainforce': mainforce})
    
    # 综合判断
    print(f"{'='*60}")
    print("📋 综合判断")
    print(f"{'='*60}")
    
    # 统计
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
    
    return results

if __name__ == '__main__':
    generate_report()
