#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国股票数据获取系统
支持：AKShare, Baostock, Tushare, 东方财富, 新浪财经
数据范围：2025-01-01 至今
"""

import time
from datetime import datetime, timedelta

# ============ 1. AKShare 接口 ============
def init_akshare():
    """初始化AKShare"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        print("AKShare未安装")
        return None

def get_stock_akshare(code, start_date="20250101", end_date=None):
    """获取A股历史数据"""
    ak = init_akshare()
    if not ak:
        return None
    
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    
    try:
        # 去掉 .SZ 或 .SH 后缀
        symbol = code.replace(".SZ", "").replace(".SH", "")
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                start_date=start_date, 
                                end_date=end_date)
        return df
    except Exception as e:
        print(f"AKShare获取失败 {code}: {e}")
        return None

# ============ 2. Baostock 接口 ============
def init_baostock():
    """初始化Baostock"""
    try:
        import baostock as bs
        bs.login()
        return bs
    except ImportError:
        print("Baostock未安装")
        return None

def get_stock_baostock(code, start_date="2025-01-01"):
    """获取A股历史数据"""
    bs = init_baostock()
    if not bs:
        return None
    
    try:
        # 转换为baostock格式
        bs_code = code.replace("SH", ".sh").replace("SZ", ".sz")
        rs = bs.query_history_k_data_plus(bs_code,
            "date,code,open,high,low,close,volume,amount,turn",
            start_date=start_date,
            end_date=datetime.now().strftime("%Y-%m-%d"),
            frequency="d")
        
        data_list = []
        while (error_code := rs.error_code) == '0' and rs.next():
            data_list.append(rs.get_row_data())
        
        if data_list:
            import pandas as pd
            df = pd.DataFrame(data_list, columns=rs.fields)
            return df
        return None
    except Exception as e:
        print(f"Baostock获取失败 {code}: {e}")
        return None
    finally:
        bs.logout()

# ============ 3. Tushare 接口 ============
def init_tushakey():
    """检查Tushare Token"""
    import os
    token = os.environ.get("TUSHARE_TOKEN")
    if not token:
        # 尝试读取配置
        try:
            with open(os.path.expanduser("~/.tushare_token")) as f:
                token = f.read().strip()
        except:
            pass
    return token

def get_stock_tushare(code, start_date="20250101"):
    """获取A股历史数据（需要Token）"""
    try:
        import tushare as ts
        token = init_tushakey()
        if not token:
            print("Tushare需要Token，请在环境变量设置TUSHARE_TOKEN")
            return None
        
        pro = ts.pro_api(token)
        # 去掉交易所后缀
        ts_code = code.replace(".SZ", "").replace(".SH", "")
        if code.startswith("6"):
            ts_code += ".SH"
        else:
            ts_code += ".SZ"
        
        df = pro.daily(ts_code=ts_code, start_date=start_date.replace("-", ""))
        return df
    except Exception as e:
        print(f"Tushare获取失败 {code}: {e}")
        return None

# ============ 4. 东方财富网页 ============
def get_realtime_eastmoney(code):
    """获取实时行情"""
    import requests
    
    # 判断交易所
    if code.startswith("6"):
        secid = f"1.{code}"
    else:
        secid = f"0.{code}"
    
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "invt": "2",
        "fltt": "2",
        "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f57,f58,f60,f116,f117,f162,f167,f168",
        "secid": secid
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        if data.get("data"):
            d = data["data"]
            return {
                "code": code,
                "name": d.get("f58"),
                "price": d.get("f43"),
                "change_pct": d.get("f44"),
                "open": d.get("f47"),
                "high": d.get("f48"),
                "low": d.get("f49"),
                "volume": d.get("f45"),
                "amount": d.get("f46"),
                "turn": d.get("f50"),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        print(f"东方财富获取失败 {code}: {e}")
    return None

# ============ 5. 新浪财经 ============
def get_realtime_sina(code):
    """获取实时行情（备用）"""
    import requests
    
    # 判断交易所
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
            return {
                "code": code,
                "name": data[0],
                "price": float(data[1]) if data[1] else None,
                "open": float(data[2]) if data[2] else None,
                "high": float(data[4]) if data[4] else None,
                "low": float(data[5]) if data[5] else None,
                "volume": int(float(data[8])) if data[8] else None,
                "time": data[30] + " " + data[31] if len(data) > 31 else None
            }
    except Exception as e:
        print(f"新浪获取失败 {code}: {e}")
    return None

# ============ 6. 批量获取 ============
def get_realtime_batch(codes, source="eastmoney"):
    """批量获取实时行情"""
    results = []
    for code in codes:
        if source == "eastmoney":
            data = get_realtime_eastmoney(code)
        else:
            data = get_realtime_sina(code)
        
        if data:
            results.append(data)
        
        time.sleep(0.3)  # 避免请求过快
    
    return results

# ============ 7. 数据校验 ============
def validate_data(data, source):
    """多源数据校验"""
    if not data:
        return False, "数据为空"
    
    # 检查必需字段
    required = ["code", "price"]
    for field in required:
        if field not in data or data[field] is None:
            return False, f"缺少字段: {field}"
    
    # 价格合理性
    price = float(data.get("price", 0))
    if price <= 0 or price > 10000:
        return False, f"价格异常: {price}"
    
    # 涨跌幅合理性
    change_pct = data.get("change_pct", 0)
    if change_pct and (change_pct > 20 or change_pct < -20):
        return False, f"涨跌幅异常: {change_pct}"
    
    return True, f"{source}数据有效"

# ============ 8. 多源数据获取 + 校验 ============
def get_stock_data(code, use_multiple=True):
    """
    获取股票数据（多源校验）
    返回: (主数据, 校验结果)
    """
    # 优先使用东方财富
    data = get_realtime_eastmoney(code)
    if data:
        valid, msg = validate_data(data, "东方财富")
        if valid:
            return data, {"status": "ok", "source": "eastmoney"}
    
    # 备用：新浪
    if not data:
        data = get_realtime_sina(code)
        if data:
            valid, msg = validate_data(data, "新浪")
            if valid:
                return data, {"status": "ok", "source": "sina"}
    
    return data, {"status": "error" if not data else "warning", "source": None}

# ============ 9. 历史数据获取 ============
def get_history_data(code, start_date="2025-01-01"):
    """获取历史K线数据"""
    # 优先使用Baostock（免费且稳定）
    df = get_stock_baostock(code, start_date)
    if df is not None and not df.empty:
        return df, "baostock"
    
    # 备用：AKShare
    df = get_stock_akshare(code, start_date.replace("-", ""))
    if df is not None and not df.empty:
        return df, "akshare"
    
    return None, "none"

# ============ 10. 自选股池 ============
def get_index_stocks(index_code="000300"):
    """获取指数成分股"""
    ak = init_akshare()
    if not ak:
        return []
    
    try:
        if index_code == "000300":
            # 沪深300
            df = ak.index_stock_cons_csindex(symbol="000300")
        elif index_code == "000001":
            # 上证50
            df = ak.index_stock_cons_csindex(symbol="000016")
        else:
            return []
        return df["成分券代码"].tolist() if df is not None else []
    except Exception as e:
        print(f"获取指数成分股失败: {e}")
        return []

# ============ 测试 ============
if __name__ == "__main__":
    # 测试单只股票
    code = "002642"
    print(f"=== 获取 {code} 实时数据 ===")
    
    data, status = get_stock_data(code)
    if data:
        print(f"数据源: {status['source']}")
        print(f"名称: {data.get('name')}")
        print(f"价格: {data.get('price')}")
        print(f"涨跌幅: {data.get('change_pct')}%")
        print(f"成交量: {data.get('volume')}")
    
    print("\n=== 获取历史数据 ===")
    df, source = get_history_data(code)
    if df is not None:
        print(f"数据源: {source}")
        print(f"数据量: {len(df)} 条")
        print(df.tail())
