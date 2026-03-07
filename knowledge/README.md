# 知识库管理系统

## 结构说明

```
knowledge/
├── stock_analysis/      # 股票分析
│   ├── models/         # 模型库
│   └── scripts/        # 运行脚本
├── project_management/  # 项目管理
│   ├── models/         # 模型库
│   └── scripts/        # 运行脚本
├── product_design/      # 产品设计
│   ├── models/         # 模型库
│   └── scripts/        # 运行脚本
├── english_learning/    # 英语学习
│   ├── models/         # 模型库
│   └── scripts/        # 运行脚本
└── text_processing/     # 文本处理
    ├── models/         # 模型库
    └── scripts/        # 运行脚本
```

## 使用方法

当你需要切换角色时，可以这样操作：

```bash
# 切换到股票分析师角色
source knowledge/stock_analysis/scripts/activate.sh

# 切换到项目经理角色
source knowledge/project_management/scripts/activate.sh

# 切换到产品设计师角色
source knowledge/product_design/scripts/activate.sh

# 切换到英语学习助手角色
source knowledge/english_learning/scripts/activate.sh

# 切换到文本处理专家角色
source knowledge/text_processing/scripts/activate.sh
```

## 角色切换示例

```
招财，现在你作为一名股票分析师，来给我解决股票分析工作。
```

系统会自动加载相应的知识库、模型和脚本，让你快速进入对应的工作状态。
```