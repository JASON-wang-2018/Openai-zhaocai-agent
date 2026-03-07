#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双系统市场复盘分析
基于"高胜率优先"原则，判断市场状态并给出操作建议

使用方法:
    python3 dual_system_review.py
"""

import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============ 数据获取 ============
def get_market_data():
    """获取市场核心指标"""
    try:
        from stock_data_v3 import get_index_stocks, get_stock_history
    except:
        pass
    
    data = {
        "index_data": {},
        "market_stats": {},
        "板块": [],
        "opportunity": []
    }
    
    # 尝试获取指数数据
    try:
        import baostock as bs
        bs.login()
        
        # 上证指数
        rs = bs.query_history_k_data_plus(
            "sh.000001",
            "date,code,open,high,low,close,volume,amount,pctChg",
            start_date=(datetime.now() - timedelta(30)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d"),
            frequency="d"
        )
        
        index_data = []
        while rs.error_code == '0' and rs.next():
            index_data.append(rs.get_row_data())
        
        if index_data:
            df = pd.DataFrame(index_data, columns=rs.fields)
            df['date'] = pd.to_datetime(df['date'])
            data["index_data"]["上证指数"] = df
            
        bs.logout()
    except Exception as e:
        print(f"获取指数数据失败: {e}")
    
    return data

def calculate_ma(df: pd.DataFrame, col: str = 'close'):
    """计算均线"""
    df = df.copy()
    df['ma5'] = df[col].rolling(5).mean()
    df['ma10'] = df[col].rolling(10).mean()
    df['ma20'] = df[col].rolling(20).mean()
    df['ma60'] = df[col].rolling(60).mean()
    return df

# ============ 1. 市场状态诊断 ============
def diagnose_market(df_index):
    """诊断市场状态"""
    if df_index is None or df_index.empty:
        return "C", "数据不足"
    
    df = calculate_ma(df_index)
    latest = df.iloc[-1]
    
    # 转换数值
    latest['close'] = float(latest['close'])
    latest['ma20'] = float(latest['ma20']) if pd.notna(latest['ma20']) else 0
    latest['ma60'] = float(latest['ma60']) if pd.notna(latest['ma60']) else 0
    latest['ma10'] = float(latest['ma10']) if pd.notna(latest['ma10']) else 0
    
    # 条件A: 强趋势主升
    cond_a = (latest['ma20'] > latest['ma60'] and 
              latest['close'] > latest['ma10'])
    
    # 条件B: 情绪冰点（简化判断）
    cond_b = latest['close'] < latest['ma20']  # 跌破MA20
    
    if cond_a:
        return "A", "强趋势主升市"
    elif cond_b:
        return "B", "情绪冰点反转市"
    else:
        return "C", "混沌观望期"

# ============ 2. 主升系统验证 ============
def verify_main_rise(df_index):
    """验证主升系统信号"""
    result = {
        "signal": False,
        "checks": [],
        "details": {}
    }
    
    if df_index is None or df_index.empty:
        result["checks"].append(("指数数据", False, "数据不足"))
        return result
    
    df = calculate_ma(df_index)
    latest = df.iloc[-1]
    
    # 检查1: 指数强趋势
    ma20 = float(latest['ma20']) if pd.notna(latest['ma20']) else 0
    ma60 = float(latest['ma60']) if pd.notna(latest['ma60']) else 0
    ma10 = float(latest['ma10']) if pd.notna(latest['ma10']) else 0
    close = float(latest['close'])
    
    check1 = ma20 > ma60 and close > ma10
    result["checks"].append(("1.指数强趋势(MA20>MA60 且 收盘>MA10)", check1, 
                           f"MA20={ma20:.2f},MA60={ma60:.2f},close={close:.2f}"))
    
    # 检查2: 板块共振（简化：涨幅）
    change_pct = float(latest['pctChg']) if latest['pctChg'] else 0
    check2 = change_pct > 0.5  # 大盘涨幅>0.5%
    result["checks"].append(("2.市场有涨幅", check2, f"涨幅{change_pct:.2f}%"))
    
    # 检查3: 风险因素
    check3 = change_pct < 9  # 未涨停（简化）
    result["checks"].append(("3.无极端风险", check3, ""))
    
    # 综合判断
    result["signal"] = check1 and check2
    result["details"] = {
        "ma20": ma20,
        "ma60": ma60,
        "close": close,
        "change_pct": change_pct
    }
    
    return result

# ============ 3. 冰点系统验证 ============
def verify_ice_point(df_index):
    """验证冰点系统信号"""
    result = {
        "signal": False,
        "checks": [],
        "details": {}
    }
    
    if df_index is None or df_index.empty:
        result["checks"].append(("指数数据", False, "数据不足"))
        return result
    
    df = calculate_ma(df_index)
    latest = df.iloc[-1]
    
    close = float(latest['close']) if latest['close'] else 0
    ma20 = float(latest['ma20']) if pd.notna(latest['ma20']) else 0
    ma60 = float(latest['ma60']) if pd.notna(latest['ma60']) else 0
    
    # 冰点条件
    check1 = close < ma20  # 跌破MA20
    result["checks"].append(("1.指数在MA20下(弱势)", check1, f"收盘{close:.2f}<MA20{ma20:.2f}"))
    
    check2 = ma20 < ma60  # 均线空头
    result["checks"].append(("2.均线空头排列", check2, ""))
    
    # 近期跌幅
    if len(df) >= 5:
        change_5d = (float(latest['close']) - float(df.iloc[-5]['close'])) / float(df.iloc[-5]['close']) * 100
    else:
        change_5d = 0
    check3 = change_5d < -3  # 5日跌幅>3%
    result["checks"].append(("3.近期有明显跌幅", check3, f"5日跌幅{change_5d:.1f}%"))
    
    result["signal"] = check1 and check2
    result["details"] = {
        "close": close,
        "ma20": ma20,
        "ma60": ma60,
        "change_5d": change_5d
    }
    
    return result

# ============ 4. 生成报告 ============
def generate_report(market_type, reason, main_rise_result, ice_point_result):
    """生成双系统复盘报告"""
    print("\n" + "="*70)
    print("  双系统市场复盘分析")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("="*70)
    
    # 第一步：市场诊断
    print(f"\n【第一步：市场状态诊断】")
    print(f"诊断结果: {market_type} - {reason}")
    
    if market_type == "A":
        print(f"  → 启用【主升系统 v3.0】")
    elif market_type == "B":
        print(f"  → 启用【冰点系统 v1.0】")
    else:
        print(f"  → 双系统均不触发，进入观望")
    
    # 第二步：信号验证
    print(f"\n【第二步：系统信号验证】")
    
    if market_type == "A":
        print(f"\n▶ 主升系统验证:")
        for check_name, passed, detail in main_rise_result["checks"]:
            status = "✅" if passed else "❌"
            detail_str = f" ({detail})" if detail else ""
            print(f"  {status} {check_name}{detail_str}")
        
        signal = "✅ 是" if main_rise_result["signal"] else "❌ 否"
        print(f"\n  → 主升系统信号: {signal}")
        
    elif market_type == "B":
        print(f"\n▶ 冰点系统验证:")
        for check_name, passed, detail in ice_point_result["checks"]:
            status = "✅" if passed else "❌"
            detail_str = f" ({detail})" if detail else ""
            print(f"  {status} {check_name}{detail_str}")
        
        signal = "✅ 是" if ice_point_result["signal"] else "❌ 否"
        print(f"\n  → 冰点系统信号: {signal}")
    
    # 第三步：机会清单
    print(f"\n【第三步：机会清单】")
    
    if market_type == "A" and main_rise_result["signal"]:
        print("▶ 主升机会:")
        print("  (需结合实时板块热度、龙头股筛选)")
        print("  选股要点: 龙头特征 + 量价强一致 + 分歧转强")
    elif market_type == "B" and ice_point_result["signal"]:
        print("▶ 冰点机会:")
        print("  (轻仓试错为主)")
        print("  选股要点: 逆势首板 + 强逻辑 + 筹码干净")
        print("  建议仓位: ≤30%")
    else:
        print("▶ 当前无明确机会信号")
    
    # 第四步：明日操作
    print(f"\n【第四步：明日操作纪律】")
    
    if market_type == "A" and main_rise_result["signal"]:
        print("  ✅ 可开仓，重点关注主线龙头")
        print("  ⚠️ 止损位: 跌破关键均线或-5%")
    elif market_type == "B" and ice_point_result["signal"]:
        print("  ⚠️ 轻仓试错，建议≤30%")
        print("  ⚠️ 若开盘<-3%则放弃")
    else:
        print("  🚫 空仓等待，市场不明朗")
    
    # 第五步：风险提示
    print(f"\n【第五步：风险提示】")
    
    risks = []
    if market_type == "A":
        risks.append("⚠️ 追高风险: 已有一定涨幅，不宜盲目追涨")
        risks.append("⚠️ 板块轮动: 热点切换快，注意及时止盈")
    elif market_type == "B":
        risks.append("⚠️ 冰点难预判: 可能继续下跌")
        risks.append("⚠️ 流动性风险: 成交萎缩时难出货")
    else:
        risks.append("⚠️ 观望为主: 等待明确信号")
    
    for risk in risks:
        print(f"  {risk}")
    
    print("\n" + "="*70)
    print("【最终结论】")
    
    if market_type == "A" and main_rise_result["signal"]:
        print("  🎯 主升信号触发，可积极做多")
    elif market_type == "B" and ice_point_result["signal"]:
        print("  🎯 冰点信号触发，可轻仓试错")
    else:
        print("  🎯 无信号，建议空仓等待")
    
    print("="*70 + "\n")

# ============ 主程序 ============
def main():
    print("正在获取市场数据...")
    
    # 获取数据
    data = get_market_data()
    df_index = data.get("index_data", {}).get("上证指数")
    
    # 诊断市场状态
    market_type, reason = diagnose_market(df_index)
    
    # 验证各系统
    main_rise_result = verify_main_rise(df_index)
    ice_point_result = verify_ice_point(df_index)
    
    # 生成报告
    generate_report(market_type, reason, main_rise_result, ice_point_result)

if __name__ == "__main__":
    main()
