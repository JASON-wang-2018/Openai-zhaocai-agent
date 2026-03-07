# 角色管理配置

## 一、角色列表

### 1. 股票分析师 (stock_analyst)
- **知识库路径**：roles/stock_analyst/knowledge/
- **模型库路径**：roles/stock_analyst/models/
- **脚本库路径**：roles/stock_analyst/scripts/
- **核心能力**：股票分析、技术分析、基本面分析、资金分析

### 2. 项目经理 (project_manager)
- **知识库路径**：roles/project_manager/knowledge/
- **模型库路径**：roles/project_manager/models/
- **脚本库路径**：roles/project_manager/scripts/
- **核心能力**：项目管理、进度控制、成本管理、质量管理

### 3. 产品设计师 (product_designer)
- **知识库路径**：roles/product_designer/knowledge/
- **模型库路径**：roles/product_designer/models/
- **脚本库路径**：roles/product_designer/scripts/
- **核心能力**：产品设计、用户体验、交互设计、视觉设计

### 4. 企业管理者 (business_manager)
- **知识库路径**：roles/business_manager/knowledge/
- **模型库路径**：roles/business_manager/models/
- **脚本库路径**：roles/business_manager/scripts/
- **核心能力**：战略管理、运营管理、组织管理、团队管理

### 5. 英语学习者 (english_learner)
- **知识库路径**：roles/english_learner/knowledge/
- **模型库路径**：roles/english_learner/models/
- **脚本库路径**：roles/english_learner/scripts/
- **核心能力**：英语学习、听说读写、词汇语法、语言应用

### 6. 文本处理专家 (text_processor)
- **知识库路径**：roles/text_processor/knowledge/
- **模型库路径**：roles/text_processor/models/
- **脚本库路径**：roles/text_processor/scripts/
- **核心能力**：文本处理、自然语言处理、数据分析、机器学习

## 二、角色切换机制

### 1. 角色切换流程
```markdown
# 角色切换流程
1. 角色选择：选择目标角色
2. 知识库加载：加载对应角色的知识库
3. 模型库加载：加载对应角色的模型库
4. 脚本库加载：加载对应角色的脚本库
5. 角色确认：确认角色切换成功
6. 角色应用：应用新角色的知识和能力
```

### 2. 角色切换脚本
```markdown
# 角色切换脚本
function switch_role(role_name) {
  // 1. 验证角色是否存在
  if (!role_exists(role_name)) {
    return "角色不存在";
  }
  
  // 2. 保存当前角色状态
  save_current_role_state();
  
  // 3. 加载新角色知识库
  load_knowledge_base(role_name);
  
  // 4. 加载新角色模型库
  load_model_library(role_name);
  
  // 5. 加载新角色脚本库
  load_script_library(role_name);
  
  // 6. 更新角色状态
  update_role_state(role_name);
  
  // 7. 确认角色切换
  return "角色切换成功: " + role_name;
}
```

### 3. 角色状态管理
```markdown
# 角色状态管理
- **当前角色**：business_manager (默认)
- **角色历史**：记录角色切换历史
- **角色配置**：存储角色配置信息
- **角色权限**：管理角色权限和访问控制
```

## 三、角色备份机制

### 1. 角色备份流程
```markdown
# 角色备份流程
1. 备份当前角色状态
2. 备份知识库
3. 备份模型库
4. 备份脚本库
5. 生成备份报告
6. 存储备份文件
```

### 2. 角色恢复流程
```markdown
# 角色恢复流程
1. 选择备份文件
2. 恢复角色状态
3. 恢复知识库
4. 恢复模型库
5. 恢复脚本库
6. 确认恢复成功
```

## 四、角色配置管理

### 1. 角色配置文件
```markdown
# 角色配置文件
{
  "current_role": "business_manager",
  "roles": {
    "stock_analyst": {
      "knowledge_path": "roles/stock_analyst/knowledge/",
      "model_path": "roles/stock_analyst/models/",
      "script_path": "roles/stock_analyst/scripts/"
    },
    "project_manager": {
      "knowledge_path": "roles/project_manager/knowledge/",
      "model_path": "roles/project_manager/models/",
      "script_path": "roles/project_manager/scripts/"
    },
    "product_designer": {
      "knowledge_path": "roles/product_designer/knowledge/",
      "model_path": "roles/product_designer/models/",
      "script_path": "roles/product_designer/scripts/"
    },
    "business_manager": {
      "knowledge_path": "roles/business_manager/knowledge/",
      "model_path": "roles/business_manager/models/",
      "script_path": "roles/business_manager/scripts/"
    },
    "english_learner": {
      "knowledge_path": "roles/english_learner/knowledge/",
      "model_path": "roles/english_learner/models/",
      "script_path": "roles/english_learner/scripts/"
    },
    "text_processor": {
      "knowledge_path": "roles/text_processor/knowledge/",
      "model_path": "roles/text_processor/models/",
      "script_path": "roles/text_processor/scripts/"
    }
  }
}
```

### 2. 角色配置管理脚本
```markdown
# 角色配置管理脚本
function manage_role_configuration() {
  // 1. 查看当前角色配置
  view_current_configuration();
  
  // 2. 修改角色配置
  modify_role_configuration();
  
  // 3. 添加新角色
  add_new_role();
  
  // 4. 删除角色
  delete_role();
  
  // 5. 备份角色配置
  backup_role_configuration();
  
  // 6. 恢复角色配置
  restore_role_configuration();
}
```

## 五、角色应用示例

### 1. 股票分析师角色应用
```markdown
# 股票分析师角色应用
- **股票分析**：使用股票分析知识库和模型
- **技术分析**：使用技术分析工具和脚本
- **基本面分析**：使用基本面分析方法和模型
- **资金分析**：使用资金分析工具和脚本
```

### 2. 项目经理角色应用
```markdown
# 项目经理角色应用
- **项目管理**：使用项目管理知识库和模型
- **进度控制**：使用进度控制工具和脚本
- **成本管理**：使用成本管理方法和模型
- **质量管理**：使用质量管理工具和脚本
```

### 3. 产品设计师角色应用
```markdown
# 产品设计师角色应用
- **产品设计**：使用产品设计知识库和模型
- **用户体验**：使用用户体验工具和脚本
- **交互设计**：使用交互设计方法和模型
- **视觉设计**：使用视觉设计工具和脚本
```

### 4. 企业管理者角色应用
```markdown
# 企业管理者角色应用
- **战略管理**：使用战略管理知识库和模型
- **运营管理**：使用运营管理工具和脚本
- **组织管理**：使用组织管理方法和模型
- **团队管理**：使用团队管理工具和脚本
```

### 5. 英语学习者角色应用
```markdown
# 英语学习者角色应用
- **英语学习**：使用英语学习知识库和模型
- **听说读写**：使用听说读写工具和脚本
- **词汇语法**：使用词汇语法方法和模型
- **语言应用**：使用语言应用工具和脚本
```

### 6. 文本处理专家角色应用
```markdown
# 文本处理专家角色应用
- **文本处理**：使用文本处理知识库和模型
- **自然语言处理**：使用NLP工具和脚本
- **数据分析**：使用数据分析方法和模型
- **机器学习**：使用机器学习工具和脚本
```

---

*本角色管理配置将持续更新，包含最新的角色配置和管理方法。*