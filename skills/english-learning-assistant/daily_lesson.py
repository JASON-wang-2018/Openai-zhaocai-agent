#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日英语课程脚本
Daily English Lesson Script

功能:
1. 搜索英语文章
2. 生成语音版本
3. 发送到飞书
4. 记录学习进度
"""

from english_learning import EnglishLearningAssistant
from datetime import datetime
import json


def generate_daily_lesson():
    """生成每日英语课程"""
    
    print("📚 生成每日英语课程...")
    
    assistant = EnglishLearningAssistant()
    
    # 1. 搜索文章
    print("🔍 搜索英语文章...")
    topics = [
        "artificial intelligence",
        "climate change", 
        "space exploration",
        "healthy lifestyle",
        "business innovation"
    ]
    
    import random
    topic = random.choice(topics)
    article = assistant.search_article(topic=topic, level="intermediate")
    
    print(f"✅ 找到文章: {article['title']}")
    
    # 2. 生成词汇表 (模拟)
    vocab_list = f"""
• {topic.replace(' ', ', ')} - 核心词汇
• artificial intelligence - 人工智能
• sustainable development - 可持续发展
• innovative solutions - 创新解决方案
• global challenges - 全球性挑战
"""
    
    # 3. 发送到飞书
    print("📱 发送到飞书...")
    lesson_data = {
        "title": article['title'],
        "url": article['url'],
        "level": article['level'],
        "vocab": vocab_list,
        "summary": article['snippet'],
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    
    assistant.send_lesson_to_feishu(lesson_data)
    
    # 4. 更新学习记录
    assistant.update_streak()
    progress = assistant.get_progress()
    
    print("✅ 课程发送完成!")
    print(f"📊 学习进度: {progress['total_articles']} 篇文章, {progress['daily_streak']} 天连续学习")
    
    return lesson_data


if __name__ == "__main__":
    generate_daily_lesson()
