#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活助理 - 每日早晨问候
功能：获取天气、穿衣建议、生活提示
"""

import requests
import json
import re
import random
from datetime import datetime

# 钉钉Webhook
DINGTALK_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/dea464ec-019a-49f5-8c6f-3938759ed06e"

def get_weather():
    """获取苏州天气"""
    try:
        url = "https://wttr.in/Suzhou?format=%l:+%c+%t+体感%f+湿度%h+%w&lang=zh"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text.strip()
    except:
        pass
    
    # 备用方案
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=31.3&longitude=120.6&current_weather=true&lang=zh"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            temp = data['current_weather']['temperature']
            wind = data['current_weather']['windspeed']
            return f"苏州: {temp}°C, 风速{wind}km/h"
    except:
        pass
    
    return "苏州: 天气获取失败"

def get_clothing_advice(weather_str):
    """根据天气给出穿衣建议"""
    temp_match = re.search(r'(\d+)°C', weather_str)
    if temp_match:
        temp = int(temp_match.group(1))
        
        if temp >= 30:
            return "🥵 炎热夏季，建议穿短袖短裤，注意防暑防晒"
        elif temp >= 25:
            return "👕 温暖天气，建议穿短袖、长裤，适合轻薄装扮"
        elif temp >= 20:
            return "👔 舒适宜人，建议穿长袖+薄外套，早晚注意保暖"
        elif temp >= 15:
            return "🧥 凉爽天气，建议穿外套+长裤，注意早晚温差"
        elif temp >= 10:
            return "🧥 较冷天气，建议穿厚外套、秋裤，注意保暖"
        elif temp >= 5:
            return "❄️ 寒冷天气，建议穿羽绒服、棉服，裹严实"
        else:
            return "🥶 严寒天气，建议减少外出，室内取暖"
    
    return "👔 建议根据体感适时增减衣物"

def get_life_tips():
    """获取生活小贴士"""
    tips = [
        "💧 多喝水，保持身体水分",
        "🚶 适度运动，保持健康",
        "😊 保持好心情一天更顺利",
        "📱 适当休息眼睛，远离电子屏幕",
        "🥗 注意饮食均衡",
        "🧘 适当放松，缓解压力",
        "🔋 手机电量充足了吗？",
        "🌞 记得适当开窗通风"
    ]
    
    return random.choice(tips)

def send_dingtalk(message):
    """发送到钉钉/飞书"""
    headers = {"Content-Type": "application/json"}
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    
    try:
        r = requests.post(DINGTALK_WEBHOOK, headers=headers, data=json.dumps(data), timeout=10)
        if r.status_code == 200:
            result = r.json()
            if result.get('code') == 0:
                return True
    except Exception as e:
        print(f"发送失败: {e}")
    
    return False

def main():
    """主函数"""
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M")
    
    # 获取天气
    weather = get_weather()
    clothing = get_clothing_advice(weather)
    tip = get_life_tips()
    
    # 组合消息
    message = f"""🌤️ 早上好！{date_str} {time_str}

【今日天气】
{weather}

【穿衣建议】
{clothing}

【生活小贴士】
{tip}

祝您今天心情愉快！😊"""

    print(message)
    print("-" * 30)
    
    if send_dingtalk(message):
        print("✅ 发送成功")
    else:
        print("❌ 发送失败")

if __name__ == "__main__":
    main()
