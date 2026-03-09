#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票标准化分析脚本 v1.0
基于热点题材知识库和曹明成庄家理论

功能：
1. 基础数据分析
2. 均线系统分析
3. 成交量分析
4. 主力行为判断
5. 走势阶段评估
6. 操作建议输出

使用方法:
    python scripts/stock_analysis_template.py <股票代码> [数据文件路径]
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

# 尝试导入数据，如果没有文件则使用示例数据
def load_stock_data(code, file_path=None):
    """加载股票数据"""
    if file_path and os.path.exists(file_path):
        # 尝试多种格式读取
        for encoding in ['gbk', 'utf-8', 'gb18030']:
            try:
                # 尝试单列格式（Tab分隔）
                df = pd.read_csv(file_path, encoding=encoding, header=None)
                # 检查是否是单列Tab格式
                if len(df.columns) == 1:
                    return parse_tab_data(df)
            except Exception as e:
                print(f'Error: {e}')
                pass
        
        # 尝试普通CSV
        try:
            df = pd.read_csv(file_path, encoding='gbk')
            return df
        except:
            pass
    
    return None

def parse_tab_data(df):
    """解析Tab分隔的单列数据"""
    data_rows = []
    for idx, row in df.iterrows():
        row_str = str(row[0]).strip()
        # 跳过标题行和非数据行
        if len(row_str) < 20 or '来源' in row_str:
            continue
        if '/' not in row_str:
            continue
        
        # 使用Tab分割
        parts = row_str.split('\t')
        parts = [p.strip() for p in parts if p.strip()]
        
        if len(parts) >= 6:
            try:
                date = parts[0]
                open_p = float(parts[1])
                high = float(parts[2])
                low = float(parts[3])
                close = float(parts[4])
                volume = float(parts[5].replace(',', ''))
                data_rows.append({
                    'date': date, 'open': open_p, 'high': high, 
                    'low': low, 'close': close, 'volume': volume
                })
            except Exception as e:
                pass
    
    df_clean = pd.DataFrame(data_rows)
    if len(df_clean) > 0:
        df_clean['date'] = pd.to_datetime(df_clean['date'])
        df_clean = df_clean.sort_values('date').reset_index(drop=True)
    
    return df_clean

def parse_raw_data(df):
    """解析原始数据"""
    data_rows = []
    for idx, row in df.iterrows():
        row_str = str(row[0]).strip()
        if len(row_str) > 10 and '/' in row_str:
            parts = row_str.split()
            if len(parts) >= 6:
                try:
                    date = parts[0]
                    open_p = float(parts[1])
                    high = float(parts[2])
                    low = float(parts[3])
                    close = float(parts[4])
                    volume = float(parts[5])
                    data_rows.append({
                        'date': date, 'open': open_p, 'high': high, 
                        'low': low, 'close': close, 'volume': volume
                    })
                except:
                    pass
    
    df_clean = pd.DataFrame(data_rows)
    if len(df_clean) > 0:
        df_clean['date'] = pd.to_datetime(df_clean['date'])
        df_clean = df_clean.sort_values('date').reset_index(drop=True)
    
    return df_clean

def analyze_ma_system(df):
    """均线系统分析"""
    recent = df.tail(20).copy()
    latest = df.iloc[-1]
    
    ma5 = recent['close'].tail(5).mean()
    ma10 = recent['close'].tail(10).mean()
    ma20 = recent['close'].tail(20).mean()
    ma60 = recent['close'].tail(60).mean() if len(recent) >= 60 else ma20
    ma120 = recent['close'].tail(120).mean() if len(recent) >= 120 else ma60
    
    return {
        'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma60': ma60, 'ma120': ma120,
        'close': latest['close'],
        'above_ma5': latest['close'] > ma5,
        'above_ma10': latest['close'] > ma10,
        'above_ma20': latest['close'] > ma20,
        'above_ma60': latest['close'] > ma60,
        'above_ma120': latest['close'] > ma120,
    }

def analyze_volume(df):
    """成交量分析"""
    recent = df.tail(20).copy()
    latest = df.iloc[-1]
    
    vol_ma5 = recent['volume'].tail(5).mean()
    vol_ma20 = recent['volume'].mean()
    
    # 检测放量信号
    vol_ratio = latest['volume'] / vol_ma5 if vol_ma5 > 0 else 1
    
    return {
        'volume': latest['volume'],
        'vol_ma5': vol_ma5,
        'vol_ma20': vol_ma20,
        'vol_ratio': vol_ratio,
        'is_expanded': latest['volume'] > vol_ma5 * 1.2,
        'is_shrunk': latest['volume'] < vol_ma5 * 0.8,
    }

def detect_main_force(df):
    """主力行为检测"""
    signals = []
    
    # 检测成交量突变
    for i in range(-10, 0):
        if i < -len(df):
            continue
        vol = df.iloc[i]['volume']
        ma5 = df.iloc[max(0,i-5):i]['volume'].mean() if i > 0 else df.iloc[:i]['volume'].mean()
        
        if vol > ma5 * 2:
            signals.append(f"成交量突变: {df.iloc[i]['date']} 放量{(vol/ma5):.1f}倍")
    
    # 检测价格异动
    for i in range(-10, 0):
        if i < -len(df):
            continue
        change = (df.iloc[i]['close'] - df.iloc[i]['open']) / df.iloc[i]['open'] * 100
        if change > 7:
            signals.append(f"大阳线: {df.iloc[i]['date']} 涨幅{change:.1f}%")
        elif change < -7:
            signals.append(f"大阴线: {df.iloc[i]['date']} 跌幅{abs(change):.1f}%")
    
    return signals

def judge_trend_stage(ma_info, vol_info):
    """判断走势阶段"""
    latest = ma_info['close']
    
    # 统计站上均线数量
    ma_count = sum([
        ma_info['above_ma5'], ma_info['above_ma10'], 
        ma_info['above_ma20'], ma_info['above_ma60']
    ])
    
    # 判断阶段
    if ma_info['above_ma5'] and ma_info['above_ma10'] and ma_info['above_ma20']:
        if ma_info['above_ma120'] and vol_info['is_expanded']:
            stage = "启动/主升"
            desc = "放量突破，强势启动"
        elif ma_count >= 3 and vol_info['vol_ratio'] > 1:
            stage = "发酵"
            desc = "量价齐升，板块发酵"
        else:
            stage = "震荡上行"
            desc = "均线支撑，趋势向上"
    elif ma_info['above_ma5']:
        stage = "反弹"
        desc = "短线反弹，注意压力"
    else:
        stage = "调整"
        desc = "短线调整，等待企稳"
    
    return stage, desc

def generate_advice(ma_info, vol_info, stage, signals):
    """生成操作建议"""
    latest = ma_info['close']
    
    # 计算支撑压力
    support = ma_info['ma5']
    if latest > ma_info['ma10']:
        support = ma_info['ma10']
    if latest > ma_info['ma20']:
        support = min(support, ma_info['ma20'])
    
    resistance = ma_info['ma120']
    
    # 止损位
    stop_loss = ma_info['ma10'] * 0.95
    
    # 仓位建议
    if stage in ["启动/主升", "发酵"]:
        position = "5-7成"
    elif stage == "震荡上行":
        position = "3-5成"
    else:
        position = "1-3成"
    
    return {
        'support': support,
        'resistance': resistance,
        'stop_loss': stop_loss,
        'position': position,
    }

def print_report(code, df):
    """输出分析报告"""
    print("=" * 60)
    print(f"【{code}】股票标准化分析报告")
    print(f"分析日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 基础数据
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    print(f"\n📊 基础数据")
    print(f"  收盘价: {latest['close']:.2f}元")
    print(f"  涨跌幅: {(latest['close']/prev['close']-1)*100:+.2f}%")
    print(f"  成交量: {latest['volume']/10000:.0f}万")
    print(f"  成交额: {latest['volume']*latest['close']/100000000:.2f}亿")
    
    # 均线分析
    ma = analyze_ma_system(df)
    print(f"\n📈 均线系统")
    print(f"  MA5:  {ma['ma5']:.2f} {'✓' if ma['above_ma5'] else '✗'}")
    print(f"  MA10: {ma['ma10']:.2f} {'✓' if ma['above_ma10'] else '✗'}")
    print(f"  MA20: {ma['ma20']:.2f} {'✓' if ma['above_ma20'] else '✗'}")
    print(f"  MA60: {ma['ma60']:.2f} {'✓' if ma['above_ma60'] else '✗'}")
    print(f"  MA120:{ma['ma120']:.2f} {'✓' if ma['above_ma120'] else '✗'}")
    
    # 成交量
    vol = analyze_volume(df)
    print(f"\n📉 成交量分析")
    print(f"  今日量能: {vol['volume']/10000:.0f}万")
    print(f"  5日均量: {vol['vol_ma5']/10000:.0f}万")
    print(f"  量能状态: {'放量' if vol['is_expanded'] else '缩量' if vol['is_shrunk'] else '正常'}")
    
    # 主力行为
    signals = detect_main_force(df)
    print(f"\n🔍 主力行为")
    if signals:
        for s in signals[:5]:
            print(f"  • {s}")
    else:
        print("  • 无明显信号")
    
    # 走势阶段
    stage, desc = judge_trend_stage(ma, vol)
    print(f"\n🎯 走势阶段判断")
    print(f"  当前阶段: {stage}")
    print(f"  阶段描述: {desc}")
    
    # 操作建议
    advice = generate_advice(ma, vol, stage, signals)
    print(f"\n💡 操作建议")
    print(f"  支撑位: {advice['support']:.2f}元")
    print(f"  压力位: {advice['resistance']:.2f}元")
    print(f"  止损位: {advice['stop_loss']:.2f}元")
    print(f"  仓位建议: {advice['position']}")
    
    print("\n" + "=" * 60)
    
    return {
        'ma': ma, 'vol': vol, 'signals': signals,
        'stage': stage, 'advice': advice
    }

# 主函数
if __name__ == "__main__":
    if len(sys.argv) >= 3:
        code = sys.argv[1]
        file_path = sys.argv[2]
        
        print(f"加载数据: {file_path}")
        df = load_stock_data(code, file_path)
        
        if df is not None and len(df) > 0:
            print(f"成功加载 {len(df)} 条数据\n")
            print_report(code, df)
        else:
            print("数据加载失败，请检查文件格式")
    else:
        # 测试运行
        print("股票分析模板 v1.0")
        print("用法: python scripts/stock_analysis_template.py <股票代码> <数据文件>")
        print()
        print("示例:")
        print("  python scripts/stock_analysis_template.py 002642 /path/to/data.xls")
