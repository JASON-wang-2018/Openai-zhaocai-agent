#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baostock 数据获取模块
稳定获取A股日线数据
"""
import baostock as bs
import pandas as pd
from datetime import datetime, timedelta
import sys

# 登录Baostock
def login():
    """登录Baostock"""
    lg = bs.login()
    if lg.error_code != '0':
        print(f"Baostock登录失败: {lg.error_msg}")
        return False
    return True

def logout():
    """登出Baostock"""
    bs.logout()

def get_stock_daily(stock_code, days=60):
    """
    获取个股日线数据
    
    Args:
        stock_code: 股票代码，如 'sh.600519' 或 'sz.000001'
        days: 获取最近多少天的数据
    
    Returns:
        DataFrame 或 None
    """
    if not login():
        return None
    
    # 计算日期范围
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+30)).strftime('%Y-%m-%d')
    
    # 格式化股票代码
    if '.' not in stock_code:
        if stock_code.startswith('6'):
            stock_code = f'sh.{stock_code}'
        else:
            stock_code = f'sz.{stock_code}'
    
    try:
        rs = bs.query_history_k_data_plus(
            stock_code,
            'date,code,open,high,low,close,volume,amount,turn',
            start_date=start_date,
            end_date=end_date,
            frequency='d',
            adjustflag='2'  # 前复权
        )
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if not data_list:
            print(f"无数据: {stock_code}")
            bs.logout()
            return None
        
        df = pd.DataFrame(data_list, columns=rs.fields)
        
        # 转换数据类型
        numeric_cols = ['open', 'high', 'low', 'close', 'volume', 'amount', 'turn']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        bs.logout()
        return df.tail(days)  # 返回最近days天数据
        
    except Exception as e:
        print(f"获取数据失败: {e}")
        bs.logout()
        return None

def get_index_daily(index_code='sh.000001', days=60):
    """
    获取指数日线数据
    
    Args:
        index_code: 指数代码
            sh.000001 - 上证指数
            sh.000300 - 沪深300
            sz.399001 - 深证成指
            sz.399006 - 创业板指
            sh.000688 - 科创50
        days: 获取天数
    """
    return get_stock_daily(index_code, days)

def get_multiple_stocks(stock_codes, days=60):
    """
    批量获取多只股票数据
    
    Args:
        stock_codes: 股票代码列表
        days: 每只股票获取天数
    
    Returns:
        dict: {stock_code: DataFrame}
    """
    if not login():
        return {}
    
    result = {}
    for code in stock_codes:
        df = get_stock_daily(code, days)
        if df is not None and len(df) > 0:
            result[code] = df
    
    bs.logout()
    return result

def calculate_ma(df, periods=[5, 10, 20, 60, 120]):
    """计算多条均线"""
    df = df.copy()
    for p in periods:
        df[f'MA{p}'] = df['close'].rolling(window=p).mean()
    return df

# 常用指数代码映射
INDEX_CODES = {
    '上证指数': 'sh.000001',
    '沪深300': 'sh.000300',
    '深证成指': 'sz.399001',
    '创业板指': 'sz.399006',
    '科创50': 'sh.000688',
    '上证50': 'sh.000016',
    '中证500': 'sh.000905',
}

def get_main_indices(days=60):
    """获取主要指数数据"""
    if not login():
        return {}
    
    result = {}
    for name, code in INDEX_CODES.items():
        df = get_index_daily(code, days)
        if df is not None:
            result[name] = df
    
    bs.logout()
    return result

# 测试
if __name__ == '__main__':
    if len(sys.argv) > 1:
        code = sys.argv[1]
    else:
        code = 'sh.600519'  # 默认茅台
    
    print(f"获取 {code} 数据...")
    df = get_stock_daily(code, days=10)
    
    if df is not None:
        print(f"\n最近10个交易日:")
        print(df[['date', 'close', 'volume']].to_string(index=False))
    else:
        print("获取失败")
