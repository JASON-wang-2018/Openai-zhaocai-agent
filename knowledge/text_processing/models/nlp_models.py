# 文本处理NLP模型
# 包含自然语言处理相关模型和工具

import re
from collections import Counter

class TextAnalyzer:
    def __init__(self, text):
        self.text = text
        self.words = self._tokenize(text)
        self.sentences = self._split_sentences(text)
    
    def _tokenize(self, text):
        """分词"""
        return re.findall(r'\b\w+\b', text.lower())
    
    def _split_sentences(self, text):
        """分句"""
        return re.split(r'[.!?]+', text)
    
    def word_count(self):
        """单词计数"""
        return len(self.words)
    
    def sentence_count(self):
        """句子计数"""
        return len(self.sentences)
    
    def most_common_words(self, n=10):
        """最常见的单词"""
        word_counts = Counter(self.words)
        return word_counts.most_common(n)
    
    def average_sentence_length(self):
        """平均句子长度"""
        if not self.sentences:
            return 0
        total_words = sum(len(sentence.split()) for sentence in self.sentences)
        return total_words / len(self.sentences)

class TextSummarizer:
    def __init__(self, text, summary_length=3):
        self.text = text
        self.summary_length = summary_length
    
    def generate_summary(self):
        """生成摘要"""
        sentences = self.text.split('.')
        # 简单的摘要生成逻辑：选择前几个句子
        return '.'.join(sentences[:self.summary_length]) + '.'

class SentimentAnalyzer:
    def __init__(self, text):
        self.text = text.lower()
        self.positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
        self.negative_words = ['bad', 'terrible', 'awful', 'horrible', 'poor']
    
    def analyze_sentiment(self):
        """分析情感"""
        words = self.text.split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

def format_text(text, style='standard'):
    """格式化文本"""
    if style == 'standard':
        return text.strip()
    elif style == 'markdown':
        return f"**{text}**"
    elif style == 'html':
        return f"<p>{text}</p>"
    else:
        return text

def translate_text(text, target_language='english'):
    """翻译文本（简单实现）"""
    translations = {
        'hello': '你好' if target_language == 'chinese' else 'hello',
        'world': '世界' if target_language == 'chinese' else 'world'
    }
    
    words = text.lower().split()
    translated_words = []
    for word in words:
        translated_words.append(translations.get(word, word))
    
    return ' '.join(translated_words)