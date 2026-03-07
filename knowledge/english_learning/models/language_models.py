# 英语学习语言模型
# 包含语言学习相关模型和工具

class Vocabulary:
    def __init__(self, words):
        self.words = words
        self.known_words = set()
        self.learning_progress = {}
    
    def add_word(self, word, definition, example):
        """添加新单词"""
        self.words[word] = {
            'definition': definition,
            'example': example,
            'level': 'beginner'
        }
    
    def mark_as_known(self, word):
        """标记单词为已知"""
        if word in self.words:
            self.known_words.add(word)
            self.learning_progress[word] = 'known'
    
    def get_study_plan(self, target_words=20):
        """获取学习计划"""
        unknown_words = [word for word in self.words.keys() if word not in self.known_words]
        return unknown_words[:target_words]

class GrammarRule:
    def __init__(self, rule_name, explanation, examples):
        self.rule_name = rule_name
        self.explanation = explanation
        self.examples = examples
    
    def explain_rule(self):
        """解释语法规则"""
        return {
            'rule': self.rule_name,
            'explanation': self.explanation,
            'examples': self.examples
        }

class Pronunciation:
    def __init__(self, word, phonetic_spelling, audio_link=None):
        self.word = word
        self.phonetic_spelling = phonetic_spelling
        self.audio_link = audio_link
    
    def get_pronunciation_guide(self):
        """获取发音指导"""
        return {
            'word': self.word,
            'phonetic': self.phonetic_spelling,
            'audio': self.audio_link
        }

def analyze_sentence_structure(sentence):
    """分析句子结构"""
    words = sentence.split()
    word_count = len(words)
    avg_word_length = sum(len(word) for word in words) / word_count
    
    return {
        'word_count': word_count,
        'average_word_length': avg_word_length,
        'sentence_type': 'simple' if word_count < 10 else 'complex'
    }

def check_grammar(sentence):
    """检查语法"""
    # 简单的语法检查逻辑
    errors = []
    if sentence.endswith('.'):
        errors.append("句子以句号结尾 - 正确")
    else:
        errors.append("句子缺少句号")
    
    if sentence[0].isupper():
        errors.append("句子以大写字母开头 - 正确")
    else:
        errors.append("句子应以大写字母开头")
    
    return errors