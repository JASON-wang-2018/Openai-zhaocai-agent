#!/bin/bash
# 英语学习示例脚本

echo "📚 英语学习示例"
echo "================"

# 加载语言模型
source knowledge/english_learning/models/language_models.py

# 创建词汇表
vocabulary=$(Vocabulary [])
vocabulary.add_word "hello" "问候语，你好" "Hello, how are you?"
vocabulary.add_word "world" "世界" "Hello world!"
vocabulary.add_word "computer" "电脑" "I use a computer every day."
vocabulary.add_word "learning" "学习" "Learning English is fun."
vocabulary.add_word "practice" "练习" "Practice makes perfect."

echo "词汇表创建成功："
for word in "${!vocabulary.words[@]}"; do
    echo "  $word - ${vocabulary.words[$word]['definition']}"
done

echo ""
# 标记已知单词
vocabulary.mark_as_known "hello"
vocabulary.mark_as_known "world"

echo "已知单词："
for word in "${vocabulary.known_words[@]}"; do
    echo "  $word"
done

echo ""
# 获取学习计划
study_plan=$(vocabulary.get_study_plan 3)
echo "学习计划（前3个单词）："
for word in "${study_plan[@]}"; do
    echo "  $word"
done

echo ""
# 语法检查
sentence="This is a test sentence"
grammar_errors=$(check_grammar "$sentence")
echo "语法检查结果："
for error in "${grammar_errors[@]}"; do
    echo "  $error"
done

echo ""
# 发音指导
pronunciation=$(Pronunciation "hello" "/həˈloʊ/")
pronunciation_guide=$(pronunciation.get_pronunciation_guide)
echo "发音指导："
echo "  单词：${pronunciation_guide['word']}"
echo "  音标：${pronunciation_guide['phonetic']}"

echo ""
echo "📚 学习建议："
echo "  1. 每天学习新单词"
echo "  2. 练习语法规则"
echo "  3. 多听多说来提高发音"

echo ""
echo "💡 提示：这只是示例英语学习，实际学习请持之以恒！"