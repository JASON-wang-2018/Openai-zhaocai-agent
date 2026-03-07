# 股票分析金融模型
# 包含常用的股票分析算法和指标

def calculate_moving_average(prices, period=20):
    """计算移动平均线"""
    return sum(prices[-period:]) / period

def calculate_rsi(prices, period=14):
    """计算相对强弱指数"""
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - (100./(1.+rs))
    
    for i in range(period, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
            
        up = (up*(period-1) + upval)/period
        down = (down*(period-1) + downval)/period
        rs = up/down
        rsi[i] = 100. - (100./(1.+rs))
        
    return rsi

def analyze_stock_trend(prices):
    """分析股票趋势"""
    if len(prices) < 20:
        return "数据不足"
    
    ma20 = calculate_moving_average(prices, 20)
    ma50 = calculate_moving_average(prices, 50)
    
    if prices[-1] > ma20 and ma20 > ma50:
        return "上升趋势"
    elif prices[-1] < ma20 and ma20 < ma50:
        return "下降趋势"
    else:
        return "震荡趋势"