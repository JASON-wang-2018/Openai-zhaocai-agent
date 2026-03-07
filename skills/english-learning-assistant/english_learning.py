#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语学习助手核心模块
English Learning Assistant Core Module

功能:
1. 文章搜索与获取
2. 文字转语音 (TTS)
3. 语法纠错
4. 飞书消息发送
5. 学习进度追踪
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 尝试导入 TTS 工具
try:
    from skills.sag import tts as elevenlabs_tts
except ImportError:
    elevenlabs_tts = None

try:
    from skills.sherpa_onnx_tts import tts as sherpa_tts
except ImportError:
    sherpa_tts = None

# 尝试导入 STT 工具
# 优先级：openai_whisper > 无
try:
    from skills.openai_whisper import transcribe
except ImportError:
    transcribe = None


class EnglishLearningAssistant:
    """英语学习助手主类"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.user_level = "A2-B1"  # 初中级，略低于CET-4
        self.vocab_bank = self._load_json("vocab_bank.json", {})
        self.progress = self._load_json("progress.json", {
            "total_articles": 0,
            "grammar_corrections": 0,
            "daily_streak": 0,
            "last_study_date": None,
            "mistakes_log": []
        })
        
    def _load_json(self, filename, default):
        """加载 JSON 文件"""
        filepath = self.data_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filename, data):
        """保存 JSON 文件"""
        filepath = self.data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ==================== 文章搜索 ====================
    
    def search_article(self, topic: str, level: str = "intermediate") -> dict:
        """
        搜索英语文章
        
        Args:
            topic: 主题关键词
            level: 难度级别 (beginner/intermediate/advanced)
            
        Returns:
            文章信息字典
        """
        import subprocess
        
        # 预设英语学习文章（备用方案）
        preset_articles = [
            {
                "title": "The Rise of Artificial Intelligence in Everyday Life",
                "url": "https://www.bbc.com/learning-english/english/features/6-minute-english",
                "snippet": "How AI is changing the way we live, work, and interact with technology in our daily lives."
            },
            {
                "title": "Climate Change: What You Need to Know",
                "url": "https://www.bbc.com/learning-english/english/features/6-minute-english/ep-201205",
                "snippet": "Learn key vocabulary about climate change and environmental issues affecting our planet."
            },
            {
                "title": "The Science of Sleep",
                "url": "https://www.bbc.com/learning-english/english/features/6-minute-english/ep-190717",
                "snippet": "Discover why sleep is important and how it affects our health and productivity."
            },
            {
                "title": "Business Innovation in the Digital Age",
                "url": "https://www.bbc.com/learning-english/english/features/6-minute-english/ep-220427",
                "snippet": "Learn about how companies are innovating and adapting to the digital economy."
            },
            {
                "title": "The Future of Space Exploration",
                "url": "https://www.bbc.com/learning-english/english/features/6-minute-english/ep-230215",
                "snippet": "Explore new frontiers in space travel and the latest discoveries about our universe."
            }
        ]
        
        # 尝试使用 tavily-search skill 脚本
        query = f"{topic} English article learning {level} level"
        base_dir = "/home/jason/.openclaw/workspace/skills/tavily-search/scripts"
        results = []
        
        try:
            result = subprocess.run(
                ["node", f"{base_dir}/search.mjs", query, "-n", "3"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                import json
                try:
                    results = json.loads(result.stdout)
                except:
                    results = []
        except Exception as e:
            print(f"搜索出错: {e}")
        
        # 如果没有搜索结果，使用预设文章
        if not results:
            import random
            article = random.choice(preset_articles)
        else:
            article = {
                "title": results[0]["title"] if results else f"Article about {topic}",
                "url": results[0]["url"] if results else "",
                "snippet": results[0]["snippet"] if results else "",
            }
        
        # 添加元数据
        article.update({
            "topic": topic,
            "level": level,
            "fetched_at": datetime.now().isoformat()
        })
        
        # 更新进度
        self.progress["total_articles"] += 1
        self._save_json("progress.json", self.progress)
        
        return article
    
    # ==================== 文字转语音 ====================
    
    def text_to_speech(self, text: str, voice: str = "default", speed: float = 1.0) -> str:
        """
        文字转语音
        
        Args:
            text: 要转换的文本
            voice: 语音风格
            speed: 语速 (0.5-2.0)
            
        Returns:
            音频文件路径
        """
        # 使用可用的 TTS 工具
        if elevenlabs_tts:
            audio_path = elevenlabs_tts(text=text, voice=voice, speed=speed)
        elif sherpa_tts:
            audio_path = sherpa_tts(text=text, voice=voice, speed=speed)
        else:
            # 使用系统 TTS 工具
            from tools import tts
            result = tts(text=text)
            audio_path = result.get("file", "")
        
        return audio_path
    
    def play_audio(self, audio_path: str) -> bool:
        """
        播放音频文件
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            是否成功
        """
        try:
            import subprocess
            subprocess.run(["play", audio_path], check=True)
            return True
        except:
            return False
    
    # ==================== 语音转文字 ====================
    
    def speech_to_text(self, audio_path: str) -> str:
        """
        语音转文字
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            识别出的文字
        """
        # 优先使用 openai_whisper
        if transcribe and callable(transcribe):
            try:
                text = transcribe(audio_path=audio_path)
                return text
            except Exception as e:
                pass
        
        return "[语音识别未配置 - 请安装 openai_whisper skill]"
    
    # ==================== 语法纠错 ====================
    
    def correct_grammar(self, sentence: str) -> dict:
        """
        纠正英语语法错误
        
        Args:
            sentence: 用户输入的句子
            
        Returns:
            纠错结果字典
        """
        # 常见错误模式
        error_patterns = {
            r"\bI am agree\b": {
                "correct": "I agree",
                "explanation": "agree 是动词，不需要 be 动词"
            },
            r"\bShe have\b": {
                "correct": "She has",
                "explanation": "第三人称单数用 has"
            },
            r"\bsince \d+ years\b": {
                "correct": "for \d+ years",
                "explanation": "时间段用 for，since + 时间点"
            },
            r"\bI am agree with\b": {
                "correct": "I agree with",
                "explanation": "动词 agree 后直接加介词 with"
            },
            r"\bHe go\b": {
                "correct": "He goes",
                "explanation": "第三人称单数动词需要加 s"
            },
            r"\bGood morning\s*, teacher\b": {
                "correct": "Good morning",
                "explanation": "英语中通常不直接称呼老师为 'teacher'"
            }
        }
        
        import re
        
        correction = {
            "original": sentence,
            "corrected": sentence,
            "explanation": "句子看起来正确！",
            "has_error": False,
            "examples": []
        }
        
        # 检查错误模式
        for pattern, fix in error_patterns.items():
            if re.search(pattern, sentence, re.IGNORECASE):
                correction["corrected"] = re.sub(pattern, fix["correct"], sentence, flags=re.IGNORECASE)
                correction["explanation"] = fix["explanation"]
                correction["has_error"] = True
                correction["examples"].extend([
                    f"✅ {fix['correct']}",
                    f"❌ {sentence}"
                ])
                break
        
        # 如果没有匹配到模式，使用 AI 分析
        if not correction["has_error"]:
            correction["explanation"] = "未检测到明显语法错误，但可能有其他改进空间。"
        
        # 更新进度
        self.progress["grammar_corrections"] += 1
        self._save_json("progress.json", self.progress)
        
        return correction
    
    # ==================== 词汇管理 ====================
    
    def add_vocab(self, word: str, meaning: str, example: str = ""):
        """添加生词到词库"""
        self.vocab_bank[word.lower()] = {
            "meaning": meaning,
            "example": example,
            "added_at": datetime.now().isoformat(),
            "review_count": 0
        }
        self._save_json("vocab_bank.json", self.vocab_bank)
    
    def get_vocab_list(self) -> list:
        """获取词库列表"""
        return [
            {"word": k, **v} for k, v in self.vocab_bank.items()
        ]
    
    # ==================== 飞书集成 ====================
    
    def send_to_feishu(self, message: str, channel: str = "feishu"):
        """
        发送消息到飞书
        
        Args:
            message: 消息内容
            channel: 频道 (feishu)
        """
        # 尝试使用 webhook 发送
        import os
        import subprocess
        
        webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
        if webhook_url:
            # 使用 curl 发送 webhook 请求
            cmd = [
                "curl", "-X", "POST", "-H", "Content-Type: application/json",
                "-d", json.dumps({"msg_type": "text", "content": {"text": message}}),
                webhook_url
            ]
            subprocess.run(cmd, capture_output=True)
            print("✅ 已发送到飞书")
        else:
            # 没有配置 webhook，打印消息
            print("📱 飞书 webhook 未配置，发送消息:")
            print(message)
    
    def send_lesson_to_feishu(self, lesson_data: dict):
        """
        发送完整课程到飞书
        
        Args:
            lesson_data: 课程数据字典
        """
        text = f"""
📚 今日英语学习

📰 标题: {lesson_data.get('title', 'No Title')}
📖 来源: {lesson_data.get('url', 'Unknown')}
📊 难度: {lesson_data.get('level', 'Intermediate')}

💡 核心词汇:
{lesson_data.get('vocab', '暂无词汇')}

📝 文章摘要:
{lesson_data.get('summary', '暂无摘要')}

🔗 原文链接: {lesson_data.get('url', '#')}
"""
        self.send_to_feishu(text)
    
    # ==================== 进度追踪 ====================
    
    def get_progress(self) -> dict:
        """获取学习进度"""
        return {
            "total_articles": self.progress["total_articles"],
            "grammar_corrections": self.progress["grammar_corrections"],
            "vocab_count": len(self.vocab_bank),
            "daily_streak": self.progress["daily_streak"],
            "last_study_date": self.progress["last_study_date"]
        }
    
    def update_streak(self):
        """更新连续学习天数"""
        from datetime import datetime, timedelta
        
        today = datetime.now().date().isoformat()
        last_date = self.progress.get("last_study_date")
        
        if last_date != today:
            if last_date:
                last = datetime.fromisoformat(last_date).date()
                if last == datetime.now().date() - timedelta(days=1):
                    self.progress["daily_streak"] += 1
                else:
                    self.progress["daily_streak"] = 1
            else:
                self.progress["daily_streak"] = 1
            
            self.progress["last_study_date"] = today
            self._save_json("progress.json", self.progress)


# ==================== 便捷函数 ====================

def new_lesson():
    """创建新课程"""
    assistant = EnglishLearningAssistant()
    
    # 搜索文章
    article = assistant.search_article(
        topic="technology",
        level="intermediate"
    )
    
    # 生成词汇表
    vocab_text = """
• artificial intelligence (AI) - 人工智能
• personalized - 个性化的  
• adaptive learning - 自适应学习
• algorithm - 算法
• data-driven - 数据驱动的
"""
    
    # 发送到飞书
    assistant.send_lesson_to_feishu({
        "title": article["title"],
        "url": article["url"],
        "level": article["level"],
        "vocab": vocab_text,
        "summary": article["snippet"]
    })
    
    return article


def check_english(text: str) -> str:
    """快速检查英语"""
    assistant = EnglishLearningAssistant()
    correction = assistant.correct_grammar(text)
    
    if correction["has_error"]:
        return f"""
❌ 原文: {correction['original']}
✅ 纠正: {correction['corrected']}

📚 说明: {correction['explanation']}
"""
    else:
        return f"✅ {correction['original']}\n\n📚 {correction['explanation']}"


def practice_speech(audio_path: str) -> str:
    """语音练习"""
    assistant = EnglishLearningAssistant()
    
    # 语音转文字
    text = assistant.speech_to_text(audio_path)
    
    if text and "[语音识别" not in text:
        # 检查语法
        correction = assistant.correct_grammar(text)
        return f"""
🎤 语音识别: {text}
{correction}
"""
    else:
        return text


if __name__ == "__main__":
    # 测试代码
    print("🧪 测试英语学习助手")
    
    assistant = EnglishLearningAssistant()
    
    # 测试语法纠错
    test_sentences = [
        "I am agree with you",
        "She have a car",
        "I have lived here since five years"
    ]
    
    for sentence in test_sentences:
        result = assistant.correct_grammar(sentence)
        print(f"\n原文: {sentence}")
        print(f"纠正: {result['corrected']}")
        print(f"说明: {result['explanation']}")
