#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪周期分析模型
基于市场情绪、板块轮动、涨停家数等判断当前周期阶段
"""

# ============ 情绪周期定义 ============
EMOTION_CYCLE = {
    "冰点": {
        "特征": ["涨停家数少", "亏钱效应强", "高度板低"],
        "策略": "休息/轻仓试错",
        "仓位": "10%"
    },
    "修复": {
        "特征": ["跌停减少", "有反包股", "恐慌缓解"],
        "策略": "尝试买入",
        "仓位": "20%"
    },
    "启动": {
        "特征": ["出现2板", "有明确主线", "赚钱效应恢复"],
        "策略": "积极做多",
        "仓位": "40%"
    },
    "发酵": {
        "特征": ["板块效应", "跟风股多", "持续性好"],
        "策略": "重仓干龙头",
        "仓位": "60%"
    },
    "高潮": {
        "特征": ["涨停潮", "加速上涨", "一致性最强"],
        "策略": "持股待涨/分批卖",
        "仓位": "80%"
    },
    "分歧": {
        "特征": ["龙头开板", "跟风下跌", "高位震荡"],
        "策略": "边打边撤",
        "仓位": "40%"
    },
    "退潮": {
        "特征": ["亏钱效应", "高位股补跌", "空间压缩"],
        "策略": "坚决空仓",
        "仓位": "0%"
    }
}

# ============ 游资战法库 ============
TRADING_METHODS = {
    "炒股养家": {
        "核心理念": "情绪周期",
        "核心战法": ["核按钮", "情绪周期", "题材预判"],
        "口诀": "别人贪婪时我更贪婪，别人恐慌时我更恐慌",
        "风格": "快进快出，止损果断"
    },
    "赵老哥": {
        "核心理念": "龙头战法",
        "核心战法": ["二板定龙头", "只做龙头", "板块效应"],
        "口诀": "二板定龙头，一板能看出个毛",
        "风格": "打板介入，持股待涨"
    },
    "作手新一": {
        "核心理念": "趋势+情绪",
        "核心战法": ["首板介入", "分歧买入", "板块联动"],
        "风格": "敢买高位，注重基本面"
    },
    "北京炒家": {
        "核心理念": "首板模式",
        "核心战法": ["打首板", "回封买入", "量价配合"],
        "风格": "不做2板以下，只做首板"
    },
    "陈小群": {
        "核心理念": "情绪合力+做T",
        "核心战法": ["分歧买入", "极致做T", "主线聚焦"],
        "风格": "做T降本，仓位管理"
    },
    "章盟主": {
        "核心理念": "资金为王",
        "核心战法": ["大资金运作", "趋势为王", "分批建仓"],
        "风格": "偏好大盘股，操作周期长"
    }
}

# ============ 形态识别 ============
PATTERNS = {
    "分歧转一致": {
        "形态": "烂板/炸板 → 隔日弱转强",
        "买入": "分歧日尾盘/次日开盘",
        "卖出": "一致高潮后"
    },
    "弱转强": {
        "形态": "平开/低开 → 快速拉涨停",
        "买入": "打板确认",
        "要点": "超预期高开"
    },
    "加速": {
        "形态": "连续缩量涨停",
        "策略": "持股不动",
        "卖点": "量能放大、炸板"
    },
    "反包": {
        "形态": "首阴/跌停 → 次日涨停",
        "买入": "跌停撬板/低吸",
        "要点": "只做龙头反包"
    },
    "地天板": {
        "形态": "跌停 → 涨停",
        "买入": "撬跌停",
        "风险": "极高"
    }
}

# ============ 主力行为识别 ============
def identify_main_force_behavior(kline_data):
    """识别主力行为阶段"""
    signals = []
    
    # 1. 建仓特征
    if kline_data.get("volume_trend") == "decreasing" and kline_data.get("price_range") < 0.15:
        signals.append(("建仓嫌疑", "缩量横盘"))
    
    # 2. 试盘特征  
    if kline_data.get("upper_shadow") and kline_data.get("volume") > 1.5 * kline_data.get("avg_volume"):
        signals.append(("试盘嫌疑", "放量上影线"))
    
    # 3. 洗盘特征
    if kline_data.get("pullback") and kline_data.get("volume") < 0.5 * kline_data.get("avg_volume"):
        signals.append(("洗盘嫌疑", "缩量回调"))
    
    # 4. 拉升特征
    if kline_data.get("break_high") and kline_data.get("volume") > 2 * kline_data.get("avg_volume"):
        signals.append(("拉升嫌疑", "放量突破"))
    
    # 5. 出货特征
    if kline_data.get("high_position") and kline_data.get("volume") > 1.5 * kline_data.get("avg_volume"):
        if kline_data.get("price_change") < 3:  # 放量不涨
            signals.append(("出货嫌疑", "放量滞涨"))
    
    return signals

# ============ 情绪判断 ============
def judge_emotion(limit_up_count, limit_down_count, avg_height, money_flow):
    """
    判断当前情绪周期
    limit_up_count: 涨停家数
    limit_down_count: 跌停家数
    avg_height: 平均高度（最高连板）
    money_flow: 资金流向（正/负）
    """
    # 冰点
    if limit_up_count < 20 and limit_down_count > 30:
        return "冰点", EMOTION_CYCLE["冰点"]
    
    # 修复
    if limit_up_count > 30 and limit_down_count < 15:
        return "修复", EMOTION_CYCLE["修复"]
    
    # 启动
    if limit_up_count > 50 and avg_height >= 3:
        return "启动", EMOTION_CYCLE["启动"]
    
    # 发酵
    if limit_up_count > 80 and avg_height >= 4 and money_flow > 0:
        return "发酵", EMOTION_CYCLE["发酵"]
    
    # 高潮
    if limit_up_count > 100 and avg_height >= 5:
        return "高潮", EMOTION_CYCLE["高潮"]
    
    # 分歧
    if limit_up_count < 80 and limit_down_count > 20:
        return "分歧", EMOTION_CYCLE["分歧"]
    
    # 退潮
    if limit_up_count < 40 and avg_height <= 2:
        return "退潮", EMOTION_CYCLE["退潮"]
    
    return "震荡", {"策略": "观望", "仓位": "30%"}

# ============ 选股模型 ============
def select_stock(sector_data, emotion_stage):
    """根据情绪阶段选股"""
    if emotion_stage in ["冰点", "退潮"]:
        return []
    
    if emotion_stage in ["启动", "发酵", "高潮"]:
        # 做龙头
        return sector_data.get("leaders", [])
    
    if emotion_stage == "分歧":
        # 做反包
        return sector_data.get("反包标的", [])
    
    if emotion_stage == "修复":
        # 做超跌反弹
        return sector_data.get("超跌股", [])
    
    return []

# ============ 主函数 ============
if __name__ == "__main__":
    # 测试
    print("=== 情绪周期 ===")
    for stage, info in EMOTION_CYCLE.items():
        print(f"{stage}: {info['策略']}, 仓位{info['仓位']}")
    
    print("\n=== 游资手法 ===")
    for name, method in TRADING_METHODS.items():
        print(f"{name}: {method['核心理念']}")
    
    print("\n=== 形态识别 ===")
    for pattern, info in PATTERNS.items():
        print(f"{pattern}: {info['形态']}")
