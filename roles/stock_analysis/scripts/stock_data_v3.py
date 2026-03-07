#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国股票数据获取系统 v3.0
支持：AKShare, Baostock, Tushare, 东方财富, 新浪财经
数据范围：2025-01-01 至今
新增：多源数据校验、数据质量检查
"""

import time
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import pandas as pd
import requests

# ============ 配置 ============
DATA_START_DATE = "2025-01-01"  # 数据起始日期

# ============ 1. AKShare 接口 ============
def init_akshare():
    """初始化AKShare"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        print("⚠️ AKShare未安装")
        return None

def get_stock_akshare(code: str, start_date: str = DATA_START_DATE, 
                       end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
    """获取A股历史数据 (AKShare)"""
    ak = init_akshare()
    if not ak:
        return None
    
    if not end_date:
        end_date = datetime.now().strftime("%Y%m%d")
    start_date = start_date.replace("-", "")
    
    try:
        symbol = code.replace(".SZ", "").replace(".SH", "").replace("60", "")
        # 处理不同交易所
        if code.startswith("6"):
            symbol = code  # 上海
        else:
            symbol = code  # 深圳
        
        df = ak.stock_zh_a_hist(
            symbol=code.replace(".", ""),
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust="qfq"  # 前复权
        )
        
        if df is not None and not df.empty:
            df = df.rename(columns={
                '日期': 'date', '股票代码': 'code', '开盘': 'open',
                '收盘': 'close', '最高': 'high', '最低': 'low',
                '成交量': 'volume', '成交额': 'amount', '振幅': 'amplitude',
                '涨跌幅': 'change_pct', '涨跌额': 'change', '换手率': 'turn'
            })
            df['source'] = 'akshare'
        return df
    except Exception as e:
        print(f"⚠️ AKShare获取失败 {code}: {e}")
        return None

# ============ 2. Baostock 接口 ============
_bs_instance = None

def init_baostock():
    """初始化Baostock（单例）"""
    global _bs_instance
    if _bs_instance is not None:
        return _bs_instance
    
    try:
        import baostock as bs
        bs.login()
        _bs_instance = bs
        return bs
    except ImportError:
        print("⚠️ Baostock未安装")
        return None

def get_stock_baostock(code: str, start_date: str = DATA_START_DATE,
                        end_date: Optional[str] = None) -> Optional[pd.DataFrame]:
    """获取A股历史数据 (Baostock)"""
    bs = init_baostock()
    if not bs:
        return None
    
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # 转换代码格式
        bs_code = code.replace("SH", ".sh").replace("SZ", ".sz")
        if not bs_code.startswith("sh") and not bs_code.startswith("sz"):
            if code.startswith("6"):
                bs_code = f"sh{code}"
            else:
                bs_code = f"sz{code}"
        
        rs = bs.query_history_k_data_plus(
            bs_code,
            "date,code,open,high,low,close,volume,amount,turn,pctChg",
            start_date=start_date.replace("-", ""),
            end_date=end_date.replace("-", ""),
            frequency="d",
            adjustflag="2"  # 前复权
        )
        
        data_list = []
        while rs.error_code == '0' and rs.next():
            data_list.append(rs.get_row_data())
        
        if data_list:
            df = pd.DataFrame(data_list, columns=rs.fields)
            df = df.rename(columns={'pctChg': 'change_pct'})
            df['source'] = 'baostock'
            return df
        return None
    except Exception as e:
        print(f"⚠️ Baostock获取失败 {code}: {e}")
        return None

# ============ 3. Tushare 接口 ============
def init_tushare() -> Optional[object]:
    """初始化Tushare"""
    import os
    try:
        import tushare as ts
        token = os.environ.get("TUSHARE_TOKEN")
        if not token:
            try:
                with open(os.path.expanduser("~/.tushare_token")) as f:
                    token = f.read().strip()
            except:
                pass
        if token:
            ts.set_token(token)
            return ts.pro_api(token)
        return None
    except ImportError:
        return None

def get_stock_tushare(code: str, start_date: str = DATA_START_DATE) -> Optional[pd.DataFrame]:
    """获取A股历史数据 (Tushare)"""
    pro = init_tushare()
    if not pro:
        print("⚠️ Tushare未配置Token")
        return None
    
    try:
        ts_code = code.replace(".", "")
        if code.startswith("6"):
            ts_code += ".SH"
        else:
            ts_code += ".SZ"
        
        df = pro.daily(
            ts_code=ts_code,
            start_date=start_date.replace("-", ""),
            end_date=datetime.now().strftime("%Y%m%d")
        )
        
        if df is not None and not df.empty:
            df = df.sort_values('trade_date')
            df['source'] = 'tushare'
        return df
    except Exception as e:
        print(f"⚠️ Tushare获取失败 {code}: {e}")
        return None

# ============ 4. 东方财富实时 ============
def get_realtime_eastmoney(code: str) -> Optional[Dict]:
    """获取实时行情（东方财富）"""
    if code.startswith("6"):
        secid = f"1.{code}"
    else:
        secid = f"0.{code}"
    
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "invt": "2",
        "fltt": "2",
        "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f57,f58,f60,f116,f117,f162,f167,f168,f169,f170,f171,f173,f177",
        "secid": secid
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        
        if data.get("data"):
            d = data["data"]
            result = {
                "code": code,
                "name": d.get("f58"),
                "price": d.get("f43"),
                "change_pct": d.get("f44"),
                "change": d.get("f169"),
                "open": d.get("f47"),
                "high": d.get("f48"),
                "low": d.get("f49"),
                "close": d.get("f170"),  # 昨收
                "volume": d.get("f45"),
                "amount": d.get("f46"),
                "turn": d.get("f50"),
                "pe": d.get("f162"),
                "pb": d.get("f167"),
                "market_cap": d.get("f116"),  # 总市值
                "float_cap": d.get("f117"),   # 流通市值
                "high_limit": d.get("f171"),
                "low_limit": d.get("f173"),
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "eastmoney"
            }
            return result
    except Exception as e:
        print(f"⚠️ 东方财富获取失败 {code}: {e}")
    return None

# ============ 5. 新浪财经实时 ============
def get_realtime_sina(code: str) -> Optional[Dict]:
    """获取实时行情（新浪财经 - 备用）"""
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
                    "amount": float(data[9]) * 10000 if data[9] else None,
                    "time": f"{data[30]} {data[31]}" if len(data) > 31 else None,
                    "source": "sina"
                }
    except Exception as e:
        print(f"⚠️ 新浪获取失败 {code}: {e}")
    return None

# ============ 6. 腾讯财经实时 ============
def get_realtime_tencent(code: str) -> Optional[Dict]:
    """获取实时行情（腾讯财经 - 备用）"""
    if code.startswith("6"):
        tencent_code = f"sh{code}"
    else:
        tencent_code = f"sz{code}"
    
    url = f"https://qt.gtimg.cn/q={tencent_code}"
    
    try:
        r = requests.get(url, timeout=10)
        data = r.text.split("~")
        
        if len(data) > 30:
            return {
                "code": code,
                "name": data[1],
                "price": float(data[3]) if data[3] else None,
                "close": float(data[4]) if data[4] else None,
                "open": float(data[5]) if data[5] else None,
                "volume": int(data[6]) if data[6] else None,
                "high": float(data[7]) if data[7] else None,
                "low": float(data[8]) if data[8] else None,
                "change_pct": float(data[31]) if data[31] else None,
                "time": data[30],
                "source": "tencent"
            }
    except Exception as e:
        print(f"⚠️ 腾讯获取失败 {code}: {e}")
    return None

# ============ 7. 数据校验 ============
def validate_price(price: float, prev_close: float = None, 
                   high_limit: float = None, low_limit: float = None) -> Tuple[bool, str]:
    """价格合理性校验"""
    if price is None or price <= 0:
        return False, "价格无效"
    
    if price > 10000:  # 极端价格检查
        return False, f"价格异常高: {price}"
    
    # 检查涨跌停
    if prev_close and high_limit and low_limit:
        if price > high_limit * 1.01:  # 略超涨跌停
            return False, f"价格超过涨停: {price} > {high_limit}"
        if price < low_limit * 0.99:
            return False, f"价格低于跌停: {price} < {low_limit}"
    
    return True, "OK"

def validate_realtime_data(data: Dict, prev_data: Dict = None) -> Tuple[bool, str]:
    """实时数据校验"""
    if not data:
        return False, "数据为空"
    
    # 必填字段
    if not data.get("code") or not data.get("price"):
        return False, "缺少必填字段"
    
    # 价格校验
    valid, msg = validate_price(
        data.get("price"), 
        data.get("close"),
        data.get("high_limit"),
        data.get("low_limit")
    )
    if not valid:
        return False, msg
    
    # 涨跌幅校验
    change_pct = data.get("change_pct")
    if change_pct and (change_pct > 20 or change_pct < -20):
        # 新股/退市等特殊情况除外
        if abs(change_pct) > 50:
            return False, f"涨跌幅异常: {change_pct}%"
    
    # 成交量校验
    volume = data.get("volume")
    if volume and volume < 0:
        return False, "成交量为负"
    
    # 与前一次数据对比（如果有）
    if prev_data:
        prev_price = prev_data.get("price")
        curr_price = data.get("price")
        if prev_price and curr_price:
            price_diff = abs(curr_price - prev_price) / prev_price * 100
            if price_diff > 10:  # 单次变化超10%需注意
                print(f"⚠️ 价格波动较大: {prev_price} -> {curr_price}")
    
    return True, "校验通过"

def validate_history_data(df: pd.DataFrame) -> Tuple[bool, str]:
    """历史数据校验"""
    if df is None or df.empty:
        return False, "数据为空"
    
    required_cols = ['date', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            return False, f"缺少字段: {col}"
    
    # 检查日期范围
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        date_range = (df['date'].max() - df['date'].min()).days
        if date_range < 30:
            return False, f"数据时间跨度太短: {date_range}天"
    
    # 检查价格连续性
    if 'close' in df.columns:
        prices = pd.to_numeric(df['close'], errors='coerce')
        if prices.isnull().any():
            return False, "存在无效价格"
        
        # 检查是否单调递增
        if not prices.is_monotonic_increasing:
            # 允许复权导致的暂时波动
            pass
    
    return True, f"数据有效，共{len(df)}条"

# ============ 8. 多源数据对比 ============
def compare_multiple_sources(code: str) -> Dict:
    """多源数据对比"""
    results = {
        "code": code,
        "sources": {},
        "status": "error",
        "best_source": None,
        "data_hash": None
    }
    
    # 东方财富
    data1 = get_realtime_eastmoney(code)
    if data1:
        valid, msg = validate_realtime_data(data1)
        results["sources"]["eastmoney"] = {"data": data1, "valid": valid, "msg": msg}
    
    time.sleep(0.2)
    
    # 新浪
    data2 = get_realtime_sina(code)
    if data2:
        valid, msg = validate_realtime_data(data2)
        results["sources"]["sina"] = {"data": data2, "valid": valid, "msg": msg}
    
    time.sleep(0.2)
    
    # 腾讯
    data3 = get_realtime_tencent(code)
    if data3:
        valid, msg = validate_realtime_data(data3)
        results["sources"]["tencent"] = {"data": data3, "valid": valid, "msg": msg}
    
    # 选择最佳数据源
    valid_sources = [s for s, v in results["sources"].items() if v["valid"]]
    if valid_sources:
        results["status"] = "ok"
        results["best_source"] = valid_sources[0]
        results["best_data"] = results["sources"][valid_sources[0]]["data"]
        
        # 计算数据一致性hash
        if len(valid_sources) > 1:
            price1 = results["sources"][valid_sources[0]]["data"].get("price")
            price2 = results["sources"][valid_sources[1]]["data"].get("price")
            if price1 and price2:
                diff = abs(price1 - price2) / price1 * 100
                results["price_diff_pct"] = round(diff, 2)
                results["consistency"] = "high" if diff < 0.5 else "medium" if diff < 1 else "low"
    
    return results

# ============ 9. 综合数据获取 ============
def get_stock_realtime(code: str, use_multiple: bool = True) -> Tuple[Dict, Dict]:
    """
    获取实时数据（带校验）
    返回: (数据, 状态信息)
    """
    if use_multiple:
        # 多源对比
        result = compare_multiple_sources(code)
        if result["status"] == "ok":
            return result["best_data"], {
                "status": "ok",
                "source": result["best_source"],
                "multi_source": True,
                "price_diff": result.get("price_diff_pct"),
                "consistency": result.get("consistency")
            }
    
    # 单源获取（降级策略）
    data = get_realtime_eastmoney(code)
    if data:
        valid, msg = validate_realtime_data(data)
        if valid:
            return data, {"status": "ok", "source": "eastmoney"}
    
    # 备用源
    for source_func in [get_realtime_sina, get_realtime_tencent]:
        data = source_func(code)
        if data:
            valid, msg = validate_realtime_data(data)
            if valid:
                return data, {"status": "ok", "source": source_func.__name__}
    
    return None, {"status": "error", "message": "所有数据源均失败"}

def get_stock_history(code: str, start_date: str = DATA_START_DATE) -> Tuple[Optional[pd.DataFrame], str]:
    """获取历史数据（多源降级）"""
    # Baostock优先（稳定免费）
    df = get_stock_baostock(code, start_date)
    if df is not None:
        valid, msg = validate_history_data(df)
        if valid:
            return df, "baostock"
    
    # AKShare备用
    df = get_stock_akshare(code, start_date)
    if df is not None:
        valid, msg = validate_history_data(df)
        if valid:
            return df, "akshare"
    
    # Tushare备用
    df = get_stock_tushare(code, start_date)
    if df is not None:
        valid, msg = validate_history_data(df)
        if valid:
            return df, "tushare"
    
    return None, "none"

# ============ 10. 批量获取 ============
def get_batch_realtime(codes: List[str], use_multiple: bool = True) -> List[Dict]:
    """批量获取实时行情"""
    results = []
    for code in codes:
        data, status = get_stock_realtime(code, use_multiple)
        if data:
            results.append({
                **data,
                "fetch_status": status
            })
        time.sleep(0.3)  # 避免限流
    
    return results

# ============ 11. 指数成分股 ============
def get_index_stocks(index_code: str = "000300") -> List[str]:
    """获取指数成分股"""
    ak = init_akshare()
    if not ak:
        return []
    
    try:
        if index_code == "000300":  # 沪深300
            df = ak.index_stock_cons_csindex(symbol="000300")
        elif index_code == "000001":  # 上证指数（无成分股）
            return []
        elif index_code == "000016":  # 上证50
            df = ak.index_stock_cons_csindex(symbol="000016")
        elif index_code == "399001":  # 深证成指
            df = ak.index_stock_cons_csindex(symbol="399001")
        else:
            return []
        
        if df is not None:
            return df["成分券代码"].tolist()
    except Exception as e:
        print(f"⚠️ 获取指数成分股失败: {e}")
    return []

# ============ 测试 ============
if __name__ == "__main__":
    print("=" * 50)
    print("  股票数据获取系统 v3.0")
    print("=" * 50)
    
    # 测试股票
    test_codes = ["000001", "600519", "300750"]
    
    for code in test_codes:
        print(f"\n--- {code} 多源对比 ---")
        result = compare_multiple_sources(code)
        
        if result["status"] == "ok":
            data = result["best_data"]
            print(f"✅ 数据源: {result['best_source']}")
            print(f"   名称: {data.get('name')}")
            print(f"   价格: {data.get('price')}")
            print(f"   涨跌幅: {data.get('change_pct')}%")
            if result.get("price_diff"):
                print(f"   多源价差: {result['price_diff']}%")
        else:
            print(f"❌ 获取失败")
        
        time.sleep(1)
    
    print("\n--- 历史数据测试 ---")
    df, source = get_stock_history("600519")
    if df is not None:
        print(f"✅ 数据源: {source}")
        print(f"   数据量: {len(df)} 条")
        print(f"   日期范围: {df['date'].min()} ~ {df['date'].max()}")
        print(df.tail(3))
    
    print("\n" + "=" * 50)
