# 🎓 English Learning Assistant - 快速入门

## 5 分钟上手

### 1️⃣ 安装依赖

```bash
cd /home/jason/.openclaw/workspace/skills/english-learning-assistant
pip install -r requirements.txt
```

### 2️⃣ 测试基础功能

```bash
# 测试语法纠错
python3 english_learning.py

# 测试文章搜索
python3 -c "
from english_learning import new_lesson
article = new_lesson()
print(f'找到文章: {article[\"title\"]}')
"
```

### 3️⃣ 配置飞书

在 `TOOLS.md` 中添加飞书配置。

---

## 💬 日常对话示例

### 检查语法
```
用户: 金宝，帮我检查 "I am agree with you"
金宝: 
❌ 原文: I am agree with you
✅ 纠正: I agree with you

📚 说明: agree 是动词，不需要 be 动词
```

### 获取文章
```
用户: 给我找一篇关于 AI 的英语文章
金宝: [搜索并发送到飞书]
```

### 听力练习
```
用户: 把这段话读给我听
金宝: [播放语音]
```

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `english_learning.py` | 核心模块 |
| `daily_lesson.py` | 每日课程脚本 |
| `grammar_checker.py` | 语法纠错 |
| `data/vocab_bank.json` | 词汇银行 |
| `data/progress.json` | 学习进度 |

---

## 🚀 每日使用

```bash
# 每天 8:00 自动运行 (通过 cron)
python3 daily_lesson.py
```

## 📚 下一步

1. 配置飞书 Bot
2. 测试 TTS 语音
3. 尝试语音输入 (STT)
4. 建立学习习惯
