#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
午间/收盘股市分析
每天12:15 和 18:15 推送股市分析
"""

import requests
import json
from datetime import datetime

# 飞书Webhook
WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/bb8f81ed-2228-400b-9cb6-f15f22c4efaa"

def get_market_data():
    """获取市场数据"""
    try:
        # 使用免费接口获取A股数据
        url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
        params = {
            'fltt': 2,
            'fields': 'f1,f2,f3,f4,f12,f13,f14',
            'secids': '1.000001,1.000300,0.399001',  # 上证、沪深300、深证成指
        }
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, params=params, headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if 'data' in data and 'diff' in data['data']:
                return data['data']['diff']
    except:
        pass
    
    return None

def analyze_market(data):
    """双系统模型分析"""
    if not data:
        return "市场数据获取失败"
    
    result = []
    for item in data:
        name = item.get('f14', '未知')
        price = item.get('f2', '--')
        change = item.get('f3', 0)
        
        if change == '--' or change is None:
            change = 0
        else:
            change = float(change)
        
        # 简单判断
        if change > 0.5:
            status = "📈 强势"
        elif change < -0.5:
            status = "📉 弱势"
        else:
            status = "➡️ 震荡"
        
        result.append(f"{name}: {price} ({change:+.2f}%) {status}")
    
    return "\n".join(result)

def get_pick_tips():
    """选股技巧"""
    tips = [
        """💡 **【选股技巧】回调到均线**

选择回调到10日均线附近的强势股，等待再次启动。

**要点：**
- 回调缩量
- 不破均线""",

        """💡 **【选股技巧】突破新高**

股价突破近期新高的股票，往往有持续行情。

**要点：**
- 放量突破
- 回踩不破""",

        """💡 **【选股技巧】板块龙头**

选择板块内涨幅最大的龙头股。

**要点：**
- 龙头涨幅最大
- 带动板块""",

        """💡 **【选股技巧】低位放量**

股价在低位横盘，突然放量启动。

**要点：**
- 底部横盘缩量
- 放量启动突破""",

        """💡 **【选股技巧】业绩预增**

业绩预增的股票有基本面支撑。

**要点：**
- 预告前潜伏
- 预告后卖出""",
    ]
    
    import random
    return random.choice(tips)

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

def main(period="noon"):
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    
    if period == "noon":
        title = f"午间解盘 {now.strftime('%Y年%m月%d日')} {time_str}"
    else:
        title = f"收盘总结 {now.strftime('%Y年%m月%d日')} {time_str}"
    
    # 获取市场数据
    market_data = get_market_data()
    analysis = analyze_market(market_data)
    pick_tips = get_pick_tips()
    
    message = f"""{title}

【双系统分析】
{analysis}

【选股技巧】
{pick_tips}

祝您投资顺利！💰"""

    print(message)
    print("-" * 30)
    
    if send_message(message):
        print("✅ 发送成功")
    else:
        print("❌ 发送失败")

if __name__ == "__main__":
    import sys
    period = sys.argv[1] if len(sys.argv) > 1 else "noon"
    main(period)
