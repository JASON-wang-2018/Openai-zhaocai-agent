#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股数据获取系统
数据范围: 2025-01-01 至今

数据源:
- 历史数据: Baostock (首选，稳定免费)
- 实时数据: 腾讯财经 (备用: 新浪)

验证机制:
- 价格合理性检查
- 多源数据对比
- 数据完整性验证
"""

import requests
import pandas as pd
import baostock as bs
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import time

# 配置
DATA_START_DATE = "2025-01-01"

# ============= Baostock 历史数据 =============
def init_baostock():
    """初始化Baostock"""
    bs.login()

def close_baostock():
    """关闭连接"""
    bs.logout()

def get_index_history(code: str = "sh.000001", 
                     start: str = DATA_START_DATE) -> Optional[pd.DataFrame]:
    """
    获取指数历史数据
    
    Args:
        code: 指数代码 (sh.000001=上证指数)
        start: 开始日期
    
    Returns:
        DataFrame or None
    """
    init_baostock()
    
    try:
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount,pctChg",
            start_date=start,  # Baostock accepts YYYY-MM-DD
            end_date=datetime.now().strftime("%Y-%m-%d"),
            frequency="d",
            adjustflag="2"  # 前复权
        )
        
        data = []
        while rs.error_code == '0' and rs.next():
            data.append(rs.get_row_data())
        
        if data:
            df = pd.DataFrame(data, columns=rs.fields)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        return None
    finally:
        close_baostock()

def get_stock_history(code: str,
                      start: str = DATA_START_DATE) -> Optional[pd.DataFrame]:
    """
    获取个股历史数据
    
    Args:
        code: 股票代码 (600519, 000001)
        start: 开始日期
    
    Returns:
        DataFrame or None
    """
    # 转换代码格式
    if code.startswith("6"):
        bs_code = f"sh.{code}"
    else:
        bs_code = f"sz.{code}"
    
    init_baostock()
    
    try:
        rs = bs.query_history_k_data_plus(
            bs_code,
            "date,code,open,high,low,close,volume,amount,pctChg,turn",
            start_date=start,  # Baostock accepts YYYY-MM-DD
            end_date=datetime.now().strftime("%Y-%m-%d"),
            frequency="d",
            adjustflag="2"
        )
        
        data = []
        while rs.error_code == '0' and rs.next():
            data.append(rs.get_row_data())
        
        if data:
            df = pd.DataFrame(data, columns=rs.fields)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            return df
        return None
    finally:
        close_baostock()

def get_index_list() -> List[Dict]:
    """获取主要指数列表"""
    indices = [
        {"code": "sh.000001", "name": "上证指数"},
        {"code": "sz.399001", "name": "深证成指"},
        {"code": "sz.399006", "name": "创业板指"},
        {"code": "sh.000300", "name": "沪深300"},
        {"code": "sh.000016", "name": "上证50"},
    ]
    return indices

# ============= 腾讯财经实时数据 =============
def get_realtime_tencent(code: str) -> Optional[Dict]:
    """
    获取实时行情 (腾讯财经)
    
    Args:
        code: 股票代码 (600519, 000001)
    
    Returns:
        dict or None
    """
    # 转换代码格式
    if code.startswith("6"):
        tencent_code = f"sh{code}"
    else:
        tencent_code = f"sz{code}"
    
    url = f"https://qt.gtimg.cn/q={tencent_code}"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.text.split('~')
        
        if len(data) > 30 and data[0]:
            return {
                "code": code,
                "name": data[1],
                "price": float(data[3]) if data[3] else None,
                "close": float(data[4]) if data[4] else None,
                "open": float(data[5]) if data[5] else None,
                "volume": int(data[6]) if data[6] else None,
                "high": float(data[7]) if data[7] else None,
                "low": float(data[8]) if data[8] else None,
                "amount": float(data[9]) * 10000 if data[9] else None,
                "change_pct": float(data[31]) if data[31] else None,
                "time": data[30],
                "source": "tencent"
            }
    except Exception as e:
        print(f"腾讯财经获取失败: {code} - {e}")
    return None

# ============= 新浪财经实时数据 (备用) =============
def get_realtime_sina(code: str) -> Optional[Dict]:
    """获取实时行情 (新浪财经 - 备用)"""
    if code.startswith("6"):
        sina_code = f"sh{code}"
    else:
        sina_code = f"sz{code}"
    
    url = f"https://hq.sinajs.cn/list={sina_code}"
    
    try:
        r = requests.get(url, timeout=10)
        content = r.text
        if "=" in content:
            data = content.split("=")[1].split(",")
            if len(data) > 10:
                return {
                    "code": code,
                    "name": data[0],
                    "price": float(data[1]) if data[1] else None,
                    "open": float(data[2]) if data[2] else None,
                    "high": float(data[4]) if data[4] else None,
                    "low": float(data[5]) if data[5] else None,
                    "close": float(data[6]) if data[6] else None,
                    "volume": int(float(data[8])) if data[8] else None,
                    "time": f"{data[30]} {data[31]}" if len(data) > 31 else None,
                    "source": "sina"
                }
    except Exception as e:
        print(f"新浪财经获取失败: {code} - {e}")
    return None

# ============= 数据校验 =============
def validate_price(price: float, prev_close: float = None) -> Tuple[bool, str]:
    """价格合理性校验"""
    if price is None or price <= 0:
        return False, "价格无效"
    if price > 10000:
        return False, f"价格异常: {price}"
    if prev_close:
        limit_up = prev_close * 1.10  # 10%涨停
        limit_down = prev_close * 0.90
        if price > limit_up * 1.01:
            return False, f"超过涨停: {price}"
        if price < limit_down * 0.99:
            return False, f"低于跌停: {price}"
    return True, "OK"

def validate_realtime(data: Dict) -> Tuple[bool, str]:
    """实时数据校验"""
    if not data:
        return False, "数据为空"
    
    if not data.get("code") or not data.get("price"):
        return False, "缺少必填字段"
    
    valid, msg = validate_price(data.get("price"), data.get("close"))
    if not valid:
        return False, msg
    
    change_pct = data.get("change_pct")
    if change_pct and abs(change_pct) > 20:
        # 可能是新股/退市
        if abs(change_pct) > 50:
            return False, f"涨跌幅异常: {change_pct}%"
    
    return True, "校验通过"

def validate_history(df: pd.DataFrame) -> Tuple[bool, str]:
    """历史数据校验"""
    if df is None or df.empty:
        return False, "数据为空"
    
    # 检查日期范围
    date_range = (df['date'].max() - df['date'].min()).days
    if date_range < 30:
        return False, f"数据时间跨度太短: {date_range}天"
    
    # 检查价格
    prices = pd.to_numeric(df['close'], errors='coerce')
    if prices.isnull().any():
        return False, "存在无效价格"
    
    return True, f"数据有效，共{len(df)}条"

# ============= 多源数据获取 =============
def get_realtime(code: str, prefer: str = "tencent") -> Tuple[Optional[Dict], str]:
    """
    获取实时数据
    
    Args:
        code: 股票代码
        prefer: 首选数据源
    
    Returns:
        (数据, 数据源)
    """
    # 首选
    if prefer == "tencent":
        data = get_realtime_tencent(code)
        if data:
            valid, msg = validate_realtime(data)
            if valid:
                return data, "tencent"
    
    # 备用: 新浪
    data = get_realtime_sina(code)
    if data:
        valid, msg = validate_realtime(data)
        if valid:
            return data, "sina"
    
    return None, "none"

# ============= 批量获取 =============
def batch_get_realtime(codes: List[str]) -> List[Dict]:
    """批量获取实时行情"""
    results = []
    for code in codes:
        data, source = get_realtime(code)
        if data:
            results.append({**data, "fetch_source": source})
        time.sleep(0.2)  # 避免限流
    return results

# ============= 均线计算 =============
def calculate_ma(df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
    """计算均线"""
    df = df.copy()
    for p in periods:
        df[f'ma{p}'] = df['close'].rolling(p).mean()
    return df

def get_ma_status(df: pd.DataFrame) -> Dict:
    """获取均线状态"""
    latest = df.iloc[-1]
    
    ma5 = latest.get('ma5', 0)
    ma10 = latest.get('ma10', 0)
    ma20 = latest.get('ma20', 0)
    ma60 = latest.get('ma60', 0)
    close = latest['close']
    
    # 均线结构
    if ma5 > ma10 > ma20 and ma20 > ma60:
        structure = "多头"
    elif ma5 < ma10 < ma20 and ma20 < ma60:
        structure = "空头"
    else:
        structure = "震荡"
    
    return {
        "close": float(close),
        "ma5": float(ma5) if ma5 else None,
        "ma10": float(ma10) if ma10 else None,
        "ma20": float(ma20) if ma20 else None,
        "ma60": float(ma60) if ma60 else None,
        "structure": structure
    }

# ============= 主函数 =============
if __name__ == "__main__":
    print("=" * 50)
    print("  A股数据获取系统")
    print(f"  数据范围: {DATA_START_DATE} 至今")
    print("=" * 50)
    
    # 测试获取上证指数
    print("\n【上证指数】")
    df = get_index_history("sh.000001")
    if df is not None:
        df = calculate_ma(df)
        status = get_ma_status(df)
        print(f"数据量: {len(df)} 条")
        print(f"最新: {df.iloc[-1]['date'].strftime('%Y-%m-%d')}")
        print(f"收盘: {status['close']:.2f}")
        print(f"均线: MA5={status['ma5']:.2f}, MA10={status['ma10']:.2f}, MA20={status['ma20']:.2f}")
        print(f"结构: {status['structure']}")
    
    # 测试获取个股
    print("\n【茅台(600519)】")
    df = get_stock_history("600519")
    if df is not None:
        df = calculate_ma(df)
        status = get_ma_status(df)
        print(f"数据量: {len(df)} 条")
        print(f"收盘: {status['close']:.2f}")
        print(f"结构: {status['structure']}")
    
    # 测试实时数据
    print("\n【实时行情】")
    data, source = get_realtime("600519")
    if data:
        print(f"数据源: {source}")
        print(f"价格: {data['price']}")
        print(f"涨跌: {data['change_pct']}%")
    else:
        print("获取失败")
    
    print("\n" + "=" * 50)
