#!/bin/bash
# 文本处理示例脚本

echo "📝 文本处理示例"
echo "================"

# 加载NLP模型
source knowledge/text_processing/models/nlp_models.py

# 示例文本
text="Hello world! This is a sample text for processing. We will analyze this text and generate some insights."

echo "处理文本："
echo "$text"
echo ""

# 文本分析
analyzer=$(TextAnalyzer "$text")
word_count=$(analyzer.word_count)
sentence_count=$(analyzer.sentence_length)
common_words=$(analyzer.most_common_words 5)

echo "文本分析结果："
echo "  单词数量：$word_count"
echo "  句子数量：$sentence_count"
echo "  最常见单词："
for word, count in "${common_words[@]}"; do
    echo "    $word: $count次"
done

echo ""
# 生成摘要
summarizer=$(TextSummarizer "$text" 2)
summary=$(summarizer.generate_summary)
echo "文本摘要："
echo "$summary"

echo ""
# 情感分析
sentiment_analyzer=$(SentimentAnalyzer "$text")
sentiment=$(sentiment_analyzer.analyze_sentiment)
echo "情感分析：$sentiment"

echo ""
# 文本格式化
formatted_text=$(format_text "$text" "markdown")
echo "Markdown格式化："
echo "$formatted_text"

echo ""
echo "📝 处理建议："
echo "  1. 根据分析结果优化文本内容"
echo "  2. 使用摘要功能提取关键信息"
echo "  3. 检查情感倾向"

echo ""
echo "💡 提示：这只是示例文本处理，实际处理请根据需求调整！"