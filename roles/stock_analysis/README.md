# 股票分析 - 已有资源汇总

## 一、已有模型 (models/)

### 1. financial_models.py（已有）
```python
- calculate_moving_average()  # 移动平均线
- calculate_rsi()            # RSI指标
- analyze_stock_trend()     # 趋势分析
```

### 2. technical_analysis.py（新建）
```python
- calculate_ma()             # 均线计算
- analyze_ma_trend()        # 均线趋势
- calculate_rsi()           # RSI（含改进版）
- analyze_rsi()            # RSI分析
- calculate_macd()          # MACD计算
- analyze_macd()           # MACD分析
- analyze_candle()          # K线形态识别
- analyze_volume_price()    # 量价关系
- comprehensive_analysis()  # 综合评分模型
```

---

## 二、已有脚本 (scripts/)

### 1. example_analysis.sh（已有）
```bash
# 示例：基础价格数据分析
# 调用 financial_models.py 中的函数
```

### 2. stock_data.py（新建）
```python
# 数据获取接口
- get_stock_eastmoney()     # 东方财富实时行情
- get_stock_sina()         # 新浪财经实时
- get_realtime_quotes()    # 批量获取
- get_money_flow()         # 资金流向
- get_sector_money()       # 板块资金
- get_lhb_data()          # 龙虎榜
- validate_data()          # 数据校验
```

---

## 三、知识库 (knowledge/)

### 1. stock_knowledge.md（新建）
- K线基础、成交量
- 技术指标（RSI、MACD、均线）
- 市场认知（趋势、波段、主力坐庄）
- 游资手法（炒股养家、徐翔、赵老哥等）
- 交易心理

---

## 四、使用方式

```bash
# 1. 获取实时数据
python3 roles/stock_analysis/scripts/stock_data.py

# 2. 技术分析
python3 roles/stock_analysis/models/technical_analysis.py

# 3. 综合分析（需传入数据）
from models.technical_analysis import comprehensive_analysis
score, level, advice = comprehensive_analysis(quote_data, history_data)
```

---

## 五、数据获取（已可用）

| 源 | 状态 | 用途 |
|----|------|------|
| **AKShare** | ✅ 已安装 | 历史K线数据 |
| **Baostock** | ✅ 已安装 | A股历史数据 |
| **Tushare** | ✅ 已安装（需Token） | 财报/行情数据 |
| **东方财富** | ✅ 已集成 | 实时行情 |
| **新浪财经** | ✅ 已集成 | 备用实时数据 |

**测试结果**：
- 实时数据：8.22元, +8.25%
- 历史数据：282条（2025-01至今）

---

## 六、使用示例

```python
from scripts.stock_data_v2 import get_stock_data, get_history_data

# 实时数据
data, status = get_stock_data("002642")

# 历史数据（2025-01-01至今）
df, source = get_history_data("002642")
```

---

## 七、待完成

1. ✅ 基础模型 - 完成
2. ✅ 技术分析 - 完成
3. ✅ 数据获取 - 完成（2025-01至今）
4. ⏳ 选股策略模型
5. ⏳ 游资案例库
