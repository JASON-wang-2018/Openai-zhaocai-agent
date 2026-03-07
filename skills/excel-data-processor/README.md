# Excel 数据处理技能

> 快速读取、分析、处理 Excel 数据，生成项目管理报告和办公文档

## 📦 安装说明

### 依赖库
```bash
# 已安装的库
pip3 install pandas openpyxl xlrd

# 可选库（用于高级功能）
pip3 install xlsxwriter  # Excel 写入增强
pip3 install openpyxl    # Excel 格式化
```

### 环境检查
```bash
python3 --version  # Python 3.12.3
pip3 list | grep pandas    # pandas 3.0.0
pip3 list | grep openpyxl  # openpyxl 3.1.5
```

## 🚀 快速开始

### 1. 基础使用

#### 读取 Excel
```python
import pandas as pd

# 简单读取
df = pd.read_excel('data.xlsx')

# 指定工作表
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 跳过前2行，只读取A-C列
df = pd.read_excel('data.xlsx', skiprows=2, usecols='A:C')
```

#### 数据分析
```python
# 查看数据
df.head()              # 前5行
df.info()              # 数据类型和空值
df.describe()          # 统计摘要

# 筛选数据
df[df['列名'] > 100]                      # 条件筛选
df[(df['列1'] > 100) & (df['列2'] == 'A')] # 多条件

# 分组统计
df.groupby('类别')['数值'].sum()           # 求和
df.groupby('类别')['数值'].mean()          # 平均
```

#### 写入 Excel
```python
# 写入 Excel
df.to_excel('output.xlsx', index=False)

# 格式化（使用 excel_processor）
from excel_processor import ExcelProcessor
processor = ExcelProcessor()
processor.format_excel('output.xlsx')
```

### 2. 使用核心类

```python
from excel_processor import ExcelProcessor, ProjectManager

# 创建处理器
processor = ExcelProcessor()

# 读取 Excel
df = processor.read_excel('data.xlsx', sheet_name='Sheet1')

# 写入 Excel（自动格式化）
processor.write_excel(df, 'output.xlsx')
processor.format_excel('output.xlsx')

# 合并多个文件
processor.merge_excels(['file1.xlsx', 'file2.xlsx'], 'merged.xlsx')

# 创建透视表
pivot = processor.create_pivot_table(df, index='类别', columns='时间', values='销售额', aggfunc='sum')
```

### 3. 项目管理

```python
from excel_processor import ProjectManager

pm = ProjectManager()

# 创建项目管理模板
pm.create_progress_tracker('项目进度表.xlsx')
pm.create_resource_allocation('资源表.xlsx')
pm.create_risk_register('风险表.xlsx')

# 生成项目状态报告
report = pm.generate_status_report('项目进度表.xlsx', '报告.md')
print(report)

# 生成周报
weekly_report = pm.generate_weekly_report('项目进度表.xlsx', '2024-01-01', '2024-01-07')
print(weekly_report)
```

## 📚 文件结构

```
excel-data-processor/
├── SKILL.md                    # 技能说明文档
├── excel_processor.py          # 核心处理类
├── README.md                   # 本文件
└── examples/
    ├── quick_start.py          # 快速入门示例
    └── output/                  # 示例输出目录（自动创建）
        ├── 进度表.xlsx
        ├── 资源表.xlsx
        ├── 风险表.xlsx
        ├── 项目状态报告.md
        └── 本周项目周报.md
```

## 🎯 典型场景

### 场景1: 读取和分析销售数据
```python
from excel_processor import ExcelProcessor

processor = ExcelProcessor()

# 读取销售数据
df = processor.read_excel('销售数据.xlsx')

# 分析
print("\n各区域销售:")
region_sales = df.groupby('区域')['销售额'].sum()
print(region_sales)

print("\nTOP 5 产品:")
top_products = df.nlargest(5, '销售额')[['产品', '销售额']]
print(top_products)

# 保存分析结果
region_sales.to_excel('区域销售分析.xlsx')
```

### 场景2: 数据清洗
```python
from excel_processor import ExcelProcessor

processor = ExcelProcessor()

# 读取原始数据
df = processor.read_excel('原始数据.xlsx')

# 清洗
df_clean = processor.clean_data(
    df,
    dropna_cols=['姓名'],           # 删除姓名为空的行
    fillna_dict={'年龄': 30},       # 填充年龄空值
    strip_cols=['姓名', '城市']     # 去除字符串空格
)

# 保存清洗后的数据
processor.write_excel(df_clean, '清洗后数据.xlsx')
```

### 场景3: 生成项目报告
```python
from excel_processor import ProjectManager

pm = ProjectManager()

# 生成当前项目状态
report = pm.generate_status_report(
    '项目进度表.xlsx',
    '项目状态报告.md'
)

# 也可以直接查看
print(report)
```

### 场景4: 合并多个 Excel 文件
```python
from excel_processor import ExcelProcessor

processor = ExcelProcessor()

# 合并多个分公司数据
file_list = [
    '北京分公司.xlsx',
    '上海分公司.xlsx',
    '广州分公司.xlsx'
]

merged = processor.merge_excels(
    file_list,
    '全国汇总.xlsx',
    add_source=True  # 添加来源文件列
)
```

### 场景5: 创建透视表
```python
from excel_processor import ExcelProcessor

processor = ExcelProcessor()
df = processor.read_excel('销售数据.xlsx')

# 创建透视表：产品 × 季度
pivot = processor.create_pivot_table(
    df,
    index='产品',
    columns='季度',
    values='销售额',
    aggfunc='sum'
)

# 保存透视表
pivot.to_excel('销售透视表.xlsx')
```

## 📖 运行示例

### 运行所有示例
```bash
cd /home/jason/.openclaw/workspace/skills/excel-data-processor
python3 examples/quick_start.py
```

### 示例输出
运行后会在 `examples/output/` 目录下生成以下文件：
- `进度表.xlsx` - 项目进度跟踪表
- `资源表.xlsx` - 资源分配表
- `风险表.xlsx` - 风险登记册
- `项目状态报告.md` - 项目状态报告
- `本周项目周报.md` - 本周项目周报
- `财务报表.xlsx` - 财务报表（格式化后）
- `合并后的数据.xlsx` - 合并后的数据

## 💡 常用技巧

### 1. 处理日期
```python
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month
```

### 2. 字符串处理
```python
df['列名'] = df['列名'].str.strip()           # 去空格
df['列名'] = df['列名'].str.upper()           # 大写
df['列名'] = df['列名'].str.replace('旧', '新')  # 替换
```

### 3. 多条件筛选
```python
# 和关系 (&)
df[(df['列1'] > 100) & (df['列2'] == 'A')]

# 或关系 (|)
df[(df['列1'] > 100) | (df['列2'] == 'A')]

# 包含筛选
df[df['列名'].isin(['值1', '值2'])]
```

### 4. 排序
```python
# 单列排序
df.sort_values('列名', ascending=False)

# 多列排序
df.sort_values(['列1', '列2'], ascending=[True, False])
```

### 5. 数据类型转换
```python
df['数值列'] = pd.to_numeric(df['数值列'], errors='coerce')
df['文本列'] = df['文本列'].astype(str)
df['日期列'] = pd.to_datetime(df['日期列'])
```

## 🔧 核心类说明

### ExcelProcessor
Excel 数据处理核心类

**主要方法:**
- `read_excel(filepath, sheet_name)` - 读取 Excel
- `write_excel(df, filepath)` - 写入 Excel
- `format_excel(filepath)` - 格式化 Excel（标题、边框、列宽）
- `merge_excels(file_list, output_file)` - 合并多个文件
- `create_pivot_table(df, index, columns, values, aggfunc)` - 创建透视表
- `export_multiple_sheets(data_dict, output_file)` - 导出多 sheet
- `clean_data(df, dropna_cols, fillna_dict, strip_cols)` - 数据清洗
- `analyze_data(df)` - 数据分析

### ProjectManager
项目管理工具类

**主要方法:**
- `create_progress_tracker(output_file)` - 创建进度跟踪表
- `create_resource_allocation(output_file)` - 创建资源分配表
- `create_risk_register(output_file)` - 创建风险登记册
- `generate_status_report(progress_file, output_file)` - 生成状态报告
- `generate_weekly_report(progress_file, start_date, end_date)` - 生成周报

## 📝 模板说明

### 进度跟踪表模板
包含以下字段:
- 任务ID
- 任务名称
- 负责人
- 开始日期
- 计划完成
- 实际完成
- 状态（已完成/进行中/待开始）
- 进度(%)
- 优先级
- 备注

### 资源分配表模板
包含以下字段:
- 资源ID
- 资源名称
- 技能
- 可用性(%)
- 当前项目
- 成本/小时
- 联系方式

### 风险登记册模板
包含以下字段:
- 风险ID
- 风险描述
- 风险类别
- 可能性(1-5)
- 影响程度(1-5)
- 风险等级
- 应对策略
- 责任人
- 状态
- 更新日期

## 🎓 学习路径

1. **基础**: 阅读 SKILL.md，了解 Excel 处理基本概念
2. **实践**: 运行 `examples/quick_start.py`，查看输出
3. **应用**: 使用 `ProjectManager` 创建项目管理模板
4. **进阶**: 根据实际需求修改和扩展功能

## ❓ 常见问题

### Q: 如何处理大文件？
A: 使用 `chunksize` 参数分块读取:
```python
for chunk in pd.read_excel('large_file.xlsx', chunksize=1000):
    process(chunk)
```

### Q: 如何处理公式？
A: 使用 `openpyxl` 直接读取:
```python
from openpyxl import load_workbook
wb = load_workbook('file.xlsx', data_only=False)
```

### Q: 如何保护 Excel 文件？
A: 使用 `openpyxl` 设置密码:
```python
from openpyxl import Workbook
from openpyxl.security import WorkbookProtection

wb = Workbook()
wb.security = WorkbookProtection(workbookPassword='password')
wb.save('protected.xlsx')
```

### Q: 如何批量处理多个文件？
A: 使用 glob 和循环:
```python
import glob

for file in glob.glob('data/*.xlsx'):
    df = pd.read_excel(file)
    # 处理数据
    df.to_excel(f'processed/{file}')
```

## 🔗 相关资源

- [Pandas 官方文档](https://pandas.pydata.org/docs/)
- [OpenPyXL 文档](https://openpyxl.readthedocs.io/)
- [Excel 数据处理最佳实践](https://pandas.pydata.org/docs/user_guide/io.html#excel-files)

## 📞 支持

如有问题，请查看:
1. SKILL.md - 详细技能说明
2. examples/quick_start.py - 代码示例
3. excel_processor.py - 源代码（包含详细注释）

---

**版本**: 1.0
**更新日期**: 2026-02-17
