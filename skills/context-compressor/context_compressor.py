#!/usr/bin/env python3
"""
上下文压缩工具 - 节省Token使用

功能：
1. 压缩长对话历史
2. 提取关键信息
3. 生成摘要
4. 压缩非必要内容

使用方法：
python3 context_compressor.py --input conversation.txt --output compressed.txt
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Tuple
import hashlib


class ContextCompressor:
    """上下文压缩器"""

    def __init__(self, max_tokens: int = 100000):
        """
        初始化压缩器
        
        Args:
            max_tokens: 最大token数（默认100k，对应约75k字符）
        """
        self.max_tokens = max_tokens
        self.compression_ratio = 0.5  # 目标压缩到50%

    def estimate_tokens(self, text: str) -> int:
        """估算token数量（粗略估算：1 token ≈ 4字符）"""
        return len(text) // 4

    def compress对话(self, messages: List[Dict], max_messages: int = 20) -> List[Dict]:
        """
        压缩对话历史
        
        Args:
            messages: 对话消息列表
            max_messages: 最大保留消息数
        
        Returns:
            压缩后的消息列表
        """
        if len(messages) <= max_messages:
            return messages
        
        # 保留最新的消息（通常更重要）
        recent = messages[-max_messages:]
        
        # 压缩旧消息
        compressed = []
        
        for i, msg in enumerate(recent):
            # 保留重要角色（用户、助手）的消息
            role = msg.get('role', '')
            content = msg.get('content', '')
            
            # 压缩长消息
            if len(content) > 500:
                content = self.summarize(content, max_length=200)
            
            # 跳过重复的确认消息
            if 'HEARTBEAT_OK' in content or content.strip() in ['', 'OK', '好的', '收到']:
                continue
            
            compressed.append({
                'role': role,
                'content': content,
                'compressed': True if len(msg.get('content', '')) > 500 else False
            })
        
        return compressed

    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        总结长文本
        
        Args:
            text: 原始文本
            max_length: 最大长度
        
        Returns:
            压缩后的文本
        """
        if len(text) <= max_length:
            return text
        
        # 提取关键句
        sentences = re.split(r'[。！？\n]', text)
        important = []
        
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            
            # 保留包含关键信息的句子
            keywords = ['需要', '要求', '任务', '计划', '目标', '重要', '必须', '关键']
            if any(kw in sent for kw in keywords):
                important.append(sent)
            
            # 保留第一句（通常包含主题）
            if len(important) == 0:
                important.append(sent)
        
        # 合并关键句
        summary = '。'.join(important[:5])  # 最多保留5句
        if len(summary) > max_length:
            summary = summary[:max_length] + '...'
        
        return summary if summary else text[:max_length] + '...'

    def extract_tasks(self, messages: List[Dict]) -> List[Dict]:
        """
        从对话中提取任务和待办事项
        
        Args:
            messages: 对话消息列表
        
        Returns:
            任务列表
        """
        tasks = []
        
        for msg in messages:
            content = msg.get('content', '')
            
            # 提取任务模式
            task_patterns = [
                r'创建(\w+)技能',
                r'添加(\w+)功能',
                r'执行(\w+)任务',
                r'完成(\w+)分析',
                r'(\w+)已创建',
                r'(\w+)已完成',
                r'需要(\w+)',
            ]
            
            for pattern in task_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    tasks.append({
                        'task': match,
                        'source': '对话提取',
                        'timestamp': datetime.now().isoformat()
                    })
        
        return tasks

    def generate_summary(self, messages: List[Dict]) -> str:
        """
        生成对话摘要
        
        Args:
            messages: 对话消息列表
        
        Returns:
            对话摘要
        """
        if not messages:
            return "无对话记录"
        
        # 统计信息
        user_msgs = [m for m in messages if m.get('role') == 'user']
        assistant_msgs = [m for m in messages if m.get('role') == 'assistant']
        
        # 提取主题
        topics = []
        for msg in messages:
            content = msg.get('content', '')[:100]  # 取前100字符
            if content:
                topics.append(content)
        
        summary = {
            'total_messages': len(messages),
            'user_messages': len(user_msgs),
            'assistant_messages': len(assistant_msgs),
            'topics': topics[:3] if len(topics) >= 3 else topics,
            'generated_at': datetime.now().isoformat()
        }
        
        return json.dumps(summary, ensure_ascii=False, indent=2)

    def compress_file(self, input_file: str, output_file: str, 
                     extract_tasks: bool = True,
                     generate_summary: bool = True) -> Dict:
        """
        压缩文件
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            extract_tasks: 是否提取任务
            generate_summary: 是否生成摘要
        
        Returns:
            压缩统计
        """
        # 读取文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        
        # 压缩对话
        compressed_messages = self.compress对话(messages)
        
        # 提取任务
        tasks = []
        if extract_tasks:
            tasks = self.extract_tasks(messages)
        
        # 生成摘要
        summary = ""
        if generate_summary:
            summary = self.generate_summary(messages)
        
        # 计算压缩比
        original_size = len(json.dumps(messages))
        compressed_size = len(json.dumps(compressed_messages))
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        # 保存结果
        result = {
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': f"{compression_ratio:.1f}%",
            'messages_count': len(messages),
            'compressed_count': len(compressed_messages),
            'tasks_extracted': len(tasks),
            'summary': summary,
            'compressed_messages': compressed_messages,
            'tasks': tasks,
            'compressed_at': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return result

    def quick_compress(self, text: str, max_tokens: int = 50000) -> str:
        """
        快速压缩文本（适用于紧急情况）
        
        Args:
            text: 原始文本
            max_tokens: 最大token数
        
        Returns:
            压缩后的文本
        """
        current_tokens = self.estimate_tokens(text)
        
        if current_tokens <= max_tokens:
            return text
        
        # 分段压缩
        lines = text.split('\n')
        compressed = []
        
        for line in lines:
            if not line.strip():
                continue
            
            # 跳过空白行和简单确认
            if line.strip() in ['', 'OK', '好的', '收到', 'HEARTBEAT_OK']:
                continue
            
            # 压缩长行
            if len(line) > 200:
                line = self.summarize(line, 100)
            
            compressed.append(line)
        
        result = '\n'.join(compressed)
        
        # 如果还是太大，继续压缩
        while self.estimate_tokens(result) > max_tokens:
            # 每隔一行删除一行
            compressed = compressed[::2]
            result = '\n'.join(compressed)
        
        return result


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='上下文压缩工具')
    parser.add_argument('--input', '-i', required=True, help='输入文件')
    parser.add_argument('--output', '-o', required=True, help='输出文件')
    parser.add_argument('--extract-tasks', '-t', action='store_true', help='提取任务')
    parser.add_argument('--summary', '-s', action='store_true', help='生成摘要')
    parser.add_argument('--quick', '-q', action='store_true', help='快速压缩模式')
    
    args = parser.parse_args()
    
    compressor = ContextCompressor()
    
    if args.quick:
        # 快速压缩模式
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
        
        compressed = compressor.quick_compress(text)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(compressed)
        
        print(f"✓ 快速压缩完成")
        print(f"  原始大小: {len(text)} 字符")
        print(f"  压缩后: {len(compressed)} 字符")
        print(f"  压缩比: {(1 - len(compressed)/len(text))*100:.1f}%")
    else:
        # 完整压缩模式
        result = compressor.compress_file(
            args.input, 
            args.output,
            extract_tasks=args.extract_tasks,
            generate_summary=args.summary
        )
        
        print(f"✓ 压缩完成")
        print(f"  原始大小: {result['original_size']} 字符")
        print(f"  压缩后: {result['compressed_size']} 字符")
        print(f"  压缩比: {result['compression_ratio']}")
        print(f"  消息数: {result['messages_count']} → {result['compressed_count']}")
        print(f"  提取任务: {result['tasks_extracted']} 个")


if __name__ == '__main__':
    main()
