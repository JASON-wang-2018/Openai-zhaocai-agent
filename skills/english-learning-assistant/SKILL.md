# 🎓 English Learning Assistant Skill

> **最后更新**: 2026-02-18  
> **版本**: v1.0  
> **目的**: 英语听说读写全方位学习助手

---

## 📋 技能概述

这是一个专为英语学习设计的助手技能，帮助用户：
- 📖 **每日阅读**: 自动搜索并推送英语文章
- 🗣️ **听力训练**: 将文章转换为英语语音
- ✍️ **写作提升**: 语法纠错、表达优化
- 🗨️ **口语练习**: 语音识别转文字（评估中）
- 📊 **学习追踪**: 记录学习进度和错误

---

## 🛠️ 核心工具

### 1. 文字转语音 (TTS)
```python
from skills.english_learning_assistant import tts_play, tts_send_to_feishu

# 播放语音（本地）
tts_play("Hello, welcome to English learning!")

# 发送到飞书
tts_send_to_feishu("This is a sample text", channel="feishu")
```

### 2. 文章搜索
```python
from skills.english_learning_assistant import search_article

# 搜索英语文章
article = search_article(topic="technology", level="intermediate")
# 返回: {title, content, url, difficulty}
```

### 3. 语法纠错
```python
from skills.english_learning_assistant import correct_grammar

# 纠正英语错误
feedback = correct_grammar("I goes to school yesterday")
# 返回: {corrected: "I went to school yesterday", explanation: "..."}
```

### 4. 飞书消息
```python
from skills.english_learning_assistant import send_to_feishu

# 发送文本消息
send_to_feishu("Today's lesson: Present Perfect Tense")

# 发送语音消息
send_to_feishu(voice_file="/path/to/audio.mp3")
```

---

## 📚 功能模块

### 模块 1: 每日文章推送

**工作流**:
1. 根据用户兴趣搜索英语文章
2. 提供原文、音频、词汇解释
3. 发送到飞书
4. 生成学习笔记

**使用方式**:
```
金宝，今天给我找一篇关于 AI 的英语文章
```

**输出示例**:
```
📰 今日英语文章

标题: The Future of AI in Education
来源: BBC Learning English
难度: Intermediate (B1)

📝 核心词汇:
- artificial intelligence (AI) - 人工智能
- personalized - 个性化的
- adaptive learning - 自适应学习

📖 文章摘要:
[AI 正在改变教育方式...]

🔗 原文链接: https://...
🎵 语音版本: [音频文件]
```

---

### 模块 2: 语音听力训练

**功能**:
- 将文章转换为英语语音
- 支持多种语音风格（新闻、对话、演讲）
- 可调节语速

**使用方式**:
```
金宝，把这篇文章读给我听
金宝，用慢速读这段话
```

**TTS 命令** (已集成):
```bash
# 基础用法
tts text="Hello, world!"

# 带参数
tts text="The quick brown fox" voice="Joanna" speed=1.2
```

---

### 模块 3: 语法纠错助手

**功能**:
- 纠正语法错误
- 解释错误原因
- 提供正确表达
- 给出类似例句

**使用方式**:
```
金宝，帮我检查这句话: "She have been working here since five years"
```

**输出示例**:
```
✅ 语法纠错

原文: She have been working here since five years
纠正: She has been working here for five years

📚 错误分析:
1. "have" → "has" (主语是 she，第三人称单数)
2. "since five years" → "for five years" (时间段用 for，since + 时间点)

💡 拓展练习:
- I have lived here for 10 years.
- She has studied English since 2020.
```

---

### 模块 4: 口语练习 (待开发)

**评估状态**: 
- 🔍 调研中: 飞书语音消息识别能力
- 🔄 备选方案: 使用浏览器语音识别 API

**计划功能**:
- 语音输入转文字
- 发音评分
- 跟读对比

---

## 🔧 集成指南

### 飞书配置

在 `TOOLS.md` 中添加飞书配置:
```markdown
### 飞书 (Feishu)

- **Channel ID**: YOUR_CHANNEL_ID
- **Bot Token**: YOUR_BOT_TOKEN
- **App ID**: YOUR_APP_ID
- **语音支持**: ✅ 文本转语音 ✅ 语法纠错
- **语音输入**: 🔍 评估中
```

### 每日学习定时任务

```bash
# 每日 8:00 自动推送英语文章
0 8 * * * cd /home/jason/.openclaw/workspace && \
  python3 skills/english_learning_assistant/daily_lesson.py
```

---

## 📁 文件结构

```
skills/english-learning-assistant/
├── SKILL.md                    # 本文件
├── README.md                   # 快速入门
├── english_learning.py         # 核心模块
├── daily_lesson.py             # 每日课程脚本
├── grammar_checker.py          # 语法纠错模块
├── article_fetcher.py          # 文章获取模块
├── tts_wrapper.py              # TTS 封装
├── feishu_sender.py            # 飞书发送模块
├── examples/                   # 使用示例
│   ├── basic_usage.py
│   ├── daily_routine.py
│   └── conversation_practice.py
└── data/
    ├── vocab_bank.json         # 词汇银行
    └── progress.json          # 学习进度
```

---

## 🚀 快速开始

### 第一步: 基础对话

```python
# 检查语法
user_input: "I am agree with you"
response: """
❌ 错误: "I am agree with you"
✅ 正确: "I agree with you"

解释: agree 是动词，不需要 be 动词。
     正确用法: I agree with you.
"""

# 语音播放
tts_play("I agree with you. Let me explain why.")
```

### 第二步: 获取文章

```python
article = fetch_english_article(
    topic="technology",
    level="intermediate",
    length="medium"
)
print(f"标题: {article['title']}")
print(f"内容: {article['content'][:200]}...")
```

### 第三步: 发送到飞书

```python
send_lesson_to_feishu(
    text=article['content'],
    audio_path=article['audio_file'],
    title=article['title']
)
```

---

## 💡 每日学习流程

```
┌─────────────────────────────────────┐
│  🌅 早晨 (8:00)                      │
│  - 自动推送每日英语文章              │
│  - 发送语音版本到飞书               │
│  - 附带词汇表和学习提示             │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  📖 白天 (随时)                      │
│  - 用户阅读文章                     │
│  - 提问语法问题                      │
│  - 练习造句                         │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  🌙 晚间 (20:00)                     │
│  - 总结今日学习                     │
│  - 发送学习报告                     │
│  - 推送明日预告                     │
└─────────────────────────────────────┘
```

---

## 🔍 待评估功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 语音输入转文字 | 🔍 评估中 | 需要测试飞书语音消息 API |
| 实时语音对话 | 🔄 规划中 | 依赖 STT + TTS |
| 发音评分 | 🔄 规划中 | 需要语音分析库 |
| 生词本同步 | ✅ 已实现 | 使用 JSON 存储 |

---

## 📝 更新日志

### v1.0 (2026-02-18)
- ✅ 创建技能框架
- ✅ 集成 TTS 能力
- ✅ 集成文章搜索
- ✅ 语法纠错模块
- 🔍 评估语音输入能力
