#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双系统复盘分析 - 完整版
运行: python3 dual_system_review.py
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============= 配置 =============
INDEX_CODES = {
    '上证指数': '1.000001',
    '深证成指': '0.399001', 
    '创业板指': '0.399006'
}

# ============= 1. 获取大盘指数 =============
def get_index_realtime():
    """获取实时指数"""
    results = {}
    for name, code in INDEX_CODES.items():
        url = f"https://push2.eastmoney.com/api/qt/stock/get"
        params = {
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f51,f52",
            "secid": code
        }
        try:
            r = requests.get(url, params=params, timeout=5)
            data = r.json().get('data', {})
            results[name] = {
                'price': data.get('f43'),
                'change': data.get('f44'),
                'volume': data.get('f45'),
                'amount': data.get('f46'),
                'open': data.get('f47'),
                'high': data.get('f48'),
                'low': data.get('f49')
            }
        except Exception as e:
            print(f"获取{name}失败: {e}")
    return results

# ============= 2. 获取市场情绪 =============
def get_market_emotion():
    """获取市场情绪数据"""
    # 涨停家数
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "fltt": "2",
        "fields": "f2,f3,f4,f12,f13,f14",
        "pn": "1",
        "pz": "50",
        "fs": "m:0+t:80",  # 涨停
        "sort": "f3",
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json().get('data', {})
        diff = data.get('diff', [])
        limit_up = len(diff)
        
        # 跌停家数
        params['fs'] = "m:0+t:81"
        r2 = requests.get(url, params=params, timeout=5)
        data2 = r2.json().get('data', {})
        limit_down = len(data2.get('diff', []))
        
        return {
            'limit_up': limit_up,
            'limit_down': limit_down,
            'emotion': '强' if limit_up > 60 else ('弱' if limit_up < 30 else '中性')
        }
    except:
        return {'limit_up': 0, 'limit_down': 0, 'emotion': '未知'}

# ============= 3. 获取板块排行 =============
def get_sector_rank():
    """获取板块涨幅排行"""
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "fltt": "2",
        "fields": "f2,f3,f4,f12,f13,f14",
        "pn": "1",
        "pz": "20",
        "fs": "m:90+t:2",  # 行业板块
        "sort": "f3",
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json().get('data', {})
        sectors = []
        for d in data.get('diff', [])[:10]:
            sectors.append({
                'name': d.get('f14'),
                'change': d.get('f3')
            })
        return sectors
    except:
        return []

# ============= 4. 诊断市场状态 =============
def diagnose(index_data, emotion_data, sectors):
    """诊断市场状态"""
    # 检查指数
    index_strong = False
    for name, data in index_data.items():
        if data.get('change', 0) > 0.5:  # 涨幅>0.5%
            index_strong = True
    
    limit_up = emotion_data.get('limit_up', 0)
    limit_down = emotion_data.get('limit_down', 0)
    
    # 判断
    if index_strong and limit_up >= 50:
        return "A", "强趋势主升市"
    elif limit_up < 30 and limit_down > 20:
        return "B", "情绪冰点反转市"
    else:
        return "C", "混沌观望期"

# ============= 5. 生成报告 =============
def generate_report():
    """生成完整复盘报告"""
    print("=" * 60)
    print(f"   双系统复盘分析报告 - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    # 获取数据
    print("\n【数据获取中...】")
    index_data = get_index_realtime()
    emotion_data = get_market_emotion()
    sectors = get_sector_rank()
    
    # 显示数据
    print("\n【一、大盘指数】")
    for name, data in index_data.items():
        change = data.get('change', 0)
        print(f"  {name}: {data.get('price')} ({change:+.2f}%)")
    
    print("\n【二、市场情绪】")
    print(f"  涨停家数: {emotion_data.get('limit_up')}")
    print(f"  跌停家数: {emotion_data.get('limit_down')}")
    print(f"  市场情绪: {emotion_data.get('emotion')}")
    
    print("\n【三、板块排行（前10）】")
    for s in sectors:
        print(f"  {s['name']}: {s.get('change', 0):+.2f}%")
    
    # 诊断
    status, desc = diagnose(index_data, emotion_data, sectors)
    print(f"\n【四、市场诊断】")
    print(f"  当前状态: {status} - {desc}")
    
    # 系统信号
    print(f"\n【五、系统信号】")
    if status == "A":
        print("  → 启用主升系统 v3.0")
        print("  → 建议: 寻找符合'龙头特征+量价强一致'的个股")
    elif status == "B":
        print("  → 启用冰点系统 v1.0")
        print("  → 建议: 轻仓试错逆势首板")
    else:
        print("  → 双系统均不触发")
        print("  → 建议: 空仓等待")
    
    print("\n" + "=" * 60)

# ============= 主程序 =============
if __name__ == "__main__":
    generate_report()
