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

# 飞书Webhook
WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/dea464ec-019a-49f5-8c6f-3938759ed06e"

def get_lunar_date():
    """获取农历日期"""
    # 2026年农历新年是2月17日
    lunar_new_year = datetime(2026, 2, 17)
    today = datetime.now()
    
    # 计算今天是农历第几天
    days_since = (today - lunar_new_year).days
    
    # 简单农历计算（近似）
    lunar_months = [29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30]  # 大月小月交替
    lunar_days = ['初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
                  '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
                  '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十']
    lunar_months_cn = ['', '正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','冬月','腊月']
    
    # 计算农历月份和日期
    month = 1
    remaining_days = days_since
    
    for i, days_in_month in enumerate(lunar_months):
        if remaining_days < days_in_month:
            break
        remaining_days -= days_in_month
        month += 1
    
    day = remaining_days + 1
    
    # 判断是否闰月（简单处理，2026年不是闰年）
    return f"{lunar_months_cn[month]} {lunar_days[day-1]}"

def get_date_info():
    """获取日期详细信息"""
    now = datetime.now()
    
    # 阳历
    yangli = now.strftime("%Y年%m月%d日 %A")
    
    # 农历
    nongli = get_lunar_date()
    
    # 节气（简单判断）
    jieqi = ""
    # 简单节气表
    jieqi_list = [
        (1, 20, "大寒"), (2, 4, "立春"), (3, 5, "惊蛰"), (4, 5, "清明"),
        (5, 5, "立夏"), (6, 6, "芒种"), (7, 7, "小暑"), (8, 7, "立秋"),
        (9, 8, "白露"), (10, 8, "寒露"), (11, 7, "立冬"), (12, 7, "大雪")
    ]
    month = now.month
    day = now.day
    for m, d, name in jieqi_list:
        if m == month and day >= d:
            jieqi = name
    
    return yangli, nongli, jieqi

def get_weather():
    """获取苏州天气（详细信息）"""
    def kmh_to_level(kmh):
        """风速(km/h)转风力等级"""
        kmh = abs(kmh)
        if kmh < 1:
            return 0, "无风"
        elif kmh < 6:
            return 1, "1级"
        elif kmh < 12:
            return 2, "2级"
        elif kmh < 20:
            return 3, "3级"
        elif kmh < 29:
            return 4, "4级"
        elif kmh < 39:
            return 5, "5级"
        elif kmh < 50:
            return 6, "6级"
        elif kmh < 62:
            return 7, "7级"
        else:
            return 8, "8级以上"
    
    def get_wind_direction(deg):
        """风向角度转中文"""
        directions = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
        idx = round(deg / 45) % 8
        return directions[idx]
    
    def get_weather_icon(code):
        """天气代码转图标和中文"""
        mapping = {
            0: ("☀️", "晴"),
            1: ("🌤️", "晴间多云"),
            2: ("⛅", "多云"),
            3: ("☁️", "阴"),
            45: ("🌫️", "雾"),
            48: ("🌫️", "雾"),
            51: ("🌧️", "小毛毛雨"),
            53: ("🌧️", "中雨"),
            55: ("🌧️", "大雨"),
            61: ("🌧️", "小雨"),
            63: ("🌧️", "中雨"),
            65: ("🌧️", "大雨"),
            71: ("🌨️", "小雪"),
            73: ("🌨️", "中雪"),
            75: ("🌨️", "大雪"),
            77: ("🌨️", "雪粒"),
            80: ("🌧️", "阵雨"),
            81: ("🌧️", "阵雨"),
            82: ("🌧️", "大阵雨"),
            95: ("⚡", "雷暴"),
            96: ("⚡", "雷暴"),
            99: ("⚡", "雷暴"),
        }
        return mapping.get(code, ("🌤️", "多云"))
    
    def get_uv_level(uv):
        """紫外线指数转等级和提示"""
        if uv < 3:
            return "低", "无需防护"
        elif uv < 6:
            return "中等", "戴帽子"
        elif uv < 8:
            return "较高", "SPF30+防晒"
        elif uv < 11:
            return "高", "避免强光"
        else:
            return "极高", "减少外出"
    
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=31.3&longitude=120.6&current_weather=true&hourly=relative_humidity_2m&daily=temperature_2m_max,temperature_2m_min,weathercode,uv_index_max&timezone=Asia/Shanghai&lang=zh"
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            current = data['current_weather']
            daily = data.get('daily', {})
            hourly = data.get('hourly', {})
            
            temp = current['temperature']
            wind_kmh = current['windspeed']
            wind_dir = current.get('winddirection', 0)
            wind_level, wind_desc = kmh_to_level(wind_kmh)
            wind_info = f"{get_wind_direction(wind_dir)}风{wind_desc}"
            
            # 湿度
            humidity = '--'
            if hourly and 'relative_humidity_2m' in hourly:
                humidity = hourly['relative_humidity_2m'][-1]
            
            # 天气状态
            weather_code = daily.get('weathercode', [0])[0]
            icon, weather_status = get_weather_icon(weather_code)
            
            # 最高最低气温
            if daily and 'temperature_2m_max' in daily:
                today_max = daily['temperature_2m_max'][0]
                today_min = daily['temperature_2m_min'][0]
                
                # 紫外线
                uv_max = daily.get('uv_index_max', [0])[0]
                uv_level, uv_tip = get_uv_level(uv_max)
                
                return {
                    'temp': temp,
                    'humidity': humidity,
                    'high': today_max,
                    'low': today_min,
                    'wind': wind_info,
                    'icon': icon,
                    'status': weather_status,
                    'uv': uv_max,
                    'uv_level': uv_level,
                    'uv_tip': uv_tip
                }
    except Exception as e:
        print(f"天气获取异常: {e}")
    
    return {'temp': '--', 'humidity': '--', 'high': '--', 'low': '--', 'wind': '--', 'icon': '🌤️', 'status': '未知', 'uv': '--', 'uv_level': '--', 'uv_tip': ''}

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
        r = requests.post(WEBHOOK, headers=headers, data=json.dumps(data), timeout=10)
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
    time_str = now.strftime("%H:%M")
    
    # 获取日期信息
    yangli, nongli, jieqi = get_date_info()
    
    # 获取天气
    w = get_weather()
    weather_info = f"{w['icon']} {w['status']}"
    clothing = get_clothing_advice(f"{w['temp']}°C")
    tip = get_life_tips()
    
    # 组合消息
    message = f"""🌤️ 早上好！{yangli}

【农历】{nongli}{f' | {jieqi}' if jieqi else ''}

【今日天气】
苏州地区:   
天气状态：{weather_info}
目前温度：{w['temp']}°C   目前湿度：{w['humidity']}%
最高气温：{w['high']}°C 
最低气温：{w['low']}°C
风向风级：{w['wind']}
紫外线指数：{w.get('uv','--')} ({w.get('uv_level','--')}) {w.get('uv_tip','')}

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
