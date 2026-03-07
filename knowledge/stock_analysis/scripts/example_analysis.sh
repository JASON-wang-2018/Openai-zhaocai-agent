#!/bin/bash
# 股票分析示例脚本

echo "📈 股票分析示例"
echo "================"

# 模拟股票价格数据
prices=(100 102 101 103 105 104 106 108 107 109 110 112 111 113 115)

echo "股票价格数据：${prices[@]}"
echo ""

# 加载金融模型
source knowledge/stock_analysis/models/financial_models.py

# 分析股票趋势
trend=$(analyze_stock_trend prices)
echo "股票趋势分析：$trend"

# 计算移动平均线
ma20=$(calculate_moving_average prices 20)
echo "20日移动平均线：$ma20"

# 计算RSI
rsi=$(calculate_rsi prices 14)
echo "14日RSI：$rsi"

echo ""
echo "📊 分析建议："
if [ "$trend" == "上升趋势" ]; then
    echo "建议：考虑买入或持有"
elif [ "$trend" == "下降趋势" ]; then
    echo "建议：考虑卖出或观望"
else
    echo "建议：观望或等待明确信号"
fi

echo ""
echo "💡 提示：这只是示例分析，实际投资请谨慎决策！"