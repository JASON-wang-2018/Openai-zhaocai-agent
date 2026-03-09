#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
早盘股票知识推送
每天8:30 推送股票知识点或新闻
"""

import requests
import json
import random
from datetime import datetime

# 飞书Webhook
WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/bb8f81ed-2228-400b-9cb6-f15f22c4efaa"

# 股票知识点库
STOCK_KNOWLEDGE = [
    """📈 **【均线技巧】均线多头排列**

当5日均线 > 10日均线 > 20日均线时，形成多头排列，表明短期趋势向上。

**操作要点：**
- 回调到均线附近可考虑买入
- 跌破均线及时止损""",

    """📈 **【量价关系】价涨量增**

健康的上涨形态：价格上涨时成交量同步放大。

**信号解读：**
- 增量资金入场，看涨
- 可考虑顺势而为""",

    """📈 **【K线形态】红三兵**

连续三天收阳线，每一天收盘价高于前一天。

**技术含义：**
- 短期上涨信号
- 可考虑回踩买入""",

    """📈 **【主力行为】放量突破**

成交量放大配合价格突破重要压力位，是强势启动信号。

**操作建议：**
- 突破时买入
- 跌破量能需谨慎""",

    """📈 **【止损纪律】8%止损线**

买入后亏损8%必须止损！

**原因：**
- 截断亏损，让利润奔跑
- 保护本金不被套牢""",

    """📈 **【板块轮动】热点持续性**

热点板块一般持续3-5天，之后会轮动。

**策略：**
- 买在启动初期
- 高潮后及时卖出""",

    """📈 **【龙头战法】二板定龙头**

第二板还能封住的股票，很可能就是龙头。

**要点：**
- 龙头股会带动板块
- 买龙头不如买跟风""",

    """📈 **【情绪周期】冰点转折**

市场情绪冰点时，往往是转折点。

**信号：**
- 涨停家数 < 20
- 跌停家数 > 50
- 龙头股补跌""",

    """📈 **【筹码分布】低位密集**

股价在低位横盘，成交量萎缩，筹码高度集中。

**含义：**
- 主力建仓完毕
- 等待拉升""",

    """📈 **【趋势线】支撑与压力**

股价上涨触及趋势线回落，形成压力；下跌触及反弹，形成支撑。

**用法：**
- 突破压力变支撑
- 跌破支撑变压力"""
]

def get_stock_news():
    """获取简要新闻（模拟）"""
    news_tips = [
        "📰 关注今日新能源板块政策动向",
        "📰 留意人工智能板块持续性",
        "📰 注意券商板块异动",
        "📰 关注消费板块复苏预期",
        "📰 科技成长仍是主线",
        "📰 关注北向资金流向",
        "📰 注意外围市场影响"
    ]
    return random.choice(news_tips)

def send_message(message):
    """发送到飞书"""
    headers = {"Content-Type": "application/json"}
    data = {
        "msg_type": "text",
        "content": {"text": message}
    }
    
    try:
        r = requests.post(WEBHOOK, headers=headers, data=json.dumps(data), timeout=10)
        result = r.json()
        return result.get('code') == 0
    except:
        return False

def main():
    now = datetime.now()
    
    # 随机选择一个知识点
    knowledge = random.choice(STOCK_KNOWLEDGE)
    news = get_stock_news()
    
    message = f"""🌅 早上好！{now.strftime('%Y年%m月%d日')} 8:30

【今日知识点】
{knowledge}

【市场提示】
{news}

祝您今日盈利！💰"""

    print(message)
    print("-" * 30)
    
    if send_message(message):
        print("✅ 发送成功")
    else:
        print("❌ 发送失败")

if __name__ == "__main__":
    main()
