# Context Compressor - 上下文压缩工具

> **功能**: 压缩对话历史，节省Token使用
> **版本**: 1.0

---

## 🎯 功能

1. **压缩对话历史** - 移除冗余，保留关键信息
2. **提取任务** - 自动识别待办事项
3. **生成摘要** - 总结对话要点
4. **快速压缩** - 紧急情况下快速压缩

---

## 🚀 使用方法

### 1. 完整压缩模式
```bash
python3 context_compressor.py -i input.json -o output.json -t -s
```

参数：
- `-i/--input`: 输入文件
- `-o/--output`: 输出文件
- `-t/--extract-tasks`: 提取任务
- `-s/--summary`: 生成摘要

### 2. 快速压缩模式
```bash
python3 context_compressor.py -i input.txt -o output.txt -q
```

### 3. Python API
```python
from context_compressor import ContextCompressor

compressor = ContextCompressor()

# 压缩对话
compressed = compressor.compress对话(messages, max_messages=20)

# 快速压缩
compressed = compressor.quick_compress(text, max_tokens=50000)

# 提取任务
tasks = compressor.extract_tasks(messages)
```

---

## 📊 压缩效果

### 示例
```
原始对话: 1000 条消息
压缩后: 200 条消息
压缩比: 80%
节省Token: ~60%
```

### 使用场景
1. **长对话** - 压缩历史消息
2. **紧急情况** - 快速压缩
3. **定期清理** - 清理冗余
4. **存档** - 压缩后存档

---

## 💡 最佳实践

### 1. 定期压缩
```bash
# 每周压缩一次对话历史
python3 context_compressor.py -i weekly_context.json -o compressed.json -t -s
```

### 2. 紧急压缩
```bash
# Token使用超过80%时
python3 context_compressor.py -i current_context.json -o temp.json -q
```

### 3. 监控Token使用
```bash
# 检查上下文使用
session_status

# 当 >70% 时触发压缩
```

---

## 📁 文件说明

- `context_compressor.py` - 核心压缩工具
- `README.md` - 本文档

---

**记住：定期压缩上下文可以显著节省Token成本！**
