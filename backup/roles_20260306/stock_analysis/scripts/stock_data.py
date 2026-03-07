#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国股票数据获取脚本
支持：AKShare, Baostock, 东方财富网页爬取
"""

import requests
import json
import time
from datetime import datetime, timedelta

# ============ 1. AKShare 接口 ============
def get_stock_akshare(code):
    """使用AKShare获取股票数据"""
    try:
        import akshare as ak
        df = ak.stock_zh_a_hist(symbol=code, period="daily", 
                                start_date="20250101", 
                                end_date=datetime.now().strftime("%Y%m%d"))
        return df
    except Exception as e:
        print(f"AKShare获取失败: {e}")
        return None

# ============ 2. 东方财富网页接口 ============
def get_stock_eastmoney(code):
    """从东方财富获取实时行情"""
    url = f"https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "invt": "2",
        "fltt": "2",
        "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f59,f60,f116,f117,f162,f167,f168,f169,f170,f171,f173,f177",
        "secid": f"1.{code}" if code.startswith('6') else f"0.{code}"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get('data'):
            d = data['data']
            return {
                'code': code,
                'name': d.get('f58'),
                'price': d.get('f43'),  # 最新价
                'change': d.get('f44'),  # 涨跌幅
                'volume': d.get('f45'),  # 成交量
                'amount': d.get('f46'),  # 成交额
                'open': d.get('f47'),   # 开盘
                'high': d.get('f48'),   # 最高
                'low': d.get('f49'),    # 最低
                'close': d.get('f43'),  # 收盘=最新
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        print(f"东方财富获取失败: {e}")
    return None

def get_realtime_quotes(codes):
    """批量获取实时行情"""
    results = []
    for code in codes:
        data = get_stock_eastmoney(code)
        if data:
            results.append(data)
        time.sleep(0.2)  # 避免请求过快
    return results

# ============ 3. 新浪财经接口 ============
def get_stock_sina(code):
    """从新浪财经获取实时行情"""
    url = f"https://hq.sinajs.cn/list={('sh' if code.startswith('6') else 'sz')}{code}"
    try:
        r = requests.get(url, timeout=10)
        content = r.text
        if content:
            data = content.split('=')[1].split(',')
            return {
                'code': code,
                'name': data[0],
                'open': float(data[1]),
                'close': float(data[2]),
                'price': float(data[3]),
                'high': float(data[4]),
                'low': float(data[5]),
                'volume': int(float(data[8])),
                'time': data[30] + ' ' + data[31]
            }
    except Exception as e:
        print(f"新浪获取失败: {e}")
    return None

# ============ 4. 资金流向 ============
def get_money_flow(code):
    """获取主力资金流向"""
    url = "https://push2.eastmoney.com/api/qt/stock/fflow/daykline/get"
    params = {
        "lmt": "10",
        "klt": "101",
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        "secid": f"1.{code}" if code.startswith('6') else f"0.{code}"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get('data') and data['data'].get('klines'):
            klines = data['data']['klines']
            results = []
            for k in klines:
                parts = k.split(',')
                results.append({
                    'date': parts[0],
                    'main_inflow': float(parts[1]),  # 主力净流入
                    'retail_inflow': float(parts[3])  # 散户净流入
                })
            return results
    except Exception as e:
        print(f"资金流向获取失败: {e}")
    return None

# ============ 5. 板块资金 ============
def get_sector_money():
    """获取板块资金流向"""
    url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "fltt": "2",
        "invt": "2",
        "fields": "f1,f2,f3,f4,f12,f13,f14",
        "pn": "1",
        "pz": "20",
        "fs": "m:90+t:2",
        "sort": "f3",  # 按涨跌幅排序
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get('data') and data['data'].get('diff'):
            results = []
            for d in data['data']['diff']:
                results.append({
                    'code': d.get('f12'),
                    'name': d.get('f14'),
                    'change': d.get('f3'),
                    'inflow': d.get('f4')  # 净流入
                })
            return results
    except Exception as e:
        print(f"板块资金获取失败: {e}")
    return None

# ============ 6. 龙虎榜 ============
def get_lhb_data(date=None):
    """获取龙虎榜数据"""
    if not date:
        date = datetime.now().strftime("%Y%m%d")
    url = "https://push2.eastmoney.com/api/qt/stock/lhb/get"
    params = {
        "date": date,
        "fields": "f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11",
        "pn": "1",
        "pz": "30"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get('data') and data['data'].get('diff'):
            results = []
            for d in data['data']['diff']:
                results.append({
                    'code': d.get('f12'),
                    'name': d.get('f14'),
                    'close': d.get('f2'),
                    'change': d.get('f3'),
                    'amount': d.get('f6'),
                    'buy': d.get('f7'),
                    'sell': d.get('f8')
                })
            return results
    except Exception as e:
        print(f"龙虎榜获取失败: {e}")
    return None

# ============ 7. 数据校验 ============
def validate_data(data):
    """数据校验"""
    if not data:
        return False, "数据为空"
    required = ['code', 'price']
    for field in required:
        if field not in data or data[field] is None:
            return False, f"缺少字段: {field}"
    # 价格合理性检查
    if data.get('price', 0) <= 0 or data.get('price', 0) > 10000:
        return False, f"价格异常: {data.get('price')}"
    return True, "数据有效"

# ============ 主函数 ============
if __name__ == "__main__":
    # 测试获取单只股票
    code = "002642"
    print(f"获取 {code} 实时数据...")
    data = get_stock_eastmoney(code)
    if data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    
    # 测试板块资金
    print("\n获取板块资金流向...")
    sectors = get_sector_money()
    if sectors:
        for s in sectors[:5]:
            print(s)
