import time
import pandas as pd
from binance.client import Client
from binance.enums import *

# Binance API Keys (keep these secure!)
API_KEY = "NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv"
API_SECRET = "4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX"
client = Client(API_KEY, API_SECRET)

# Parameters
SYMBOL = "BTCUSDT"
INTERVAL = "5m"
QUANTITY = 0.001
RISK_REWARD_RATIO = 2  # Take profit is 2x the risk
STOP_LOSS_BUFFER = 0.002  # 0.2% below/above the pattern

def fetch_data(symbol, interval, limit=10):
    """Fetch historical candlestick data."""
    print("📊 Fetching candlestick data...")
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    data = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    data = data[["timestamp", "open", "high", "low", "close", "volume"]]
    data[["open", "high", "low", "close"]] = data[["open", "high", "low", "close"]].astype(float)
    return data

def identify_engulfing_pattern(data):
    """Identify bullish or bearish engulfing patterns."""
    print("🔍 Analyzing for candlestick patterns...")
    latest = data.iloc[-2]
    current = data.iloc[-1]
    
    if latest["close"] < latest["open"] and current["close"] > current["open"] and current["close"] > latest["open"] and current["open"] < latest["close"]:
        return "BUY"
    elif latest["close"] > latest["open"] and current["close"] < current["open"] and current["close"] < latest["open"] and current["open"] > latest["close"]:
        return "SELL"
    
    return None

def place_order(symbol, side, quantity):
    """Place a market order with stop-loss and take-profit."""
    try:
        print(f"⚡ Placing a {'BUY' if side == SIDE_BUY else 'SELL'} order...")
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        entry_price = float(order['fills'][0]['price'])
        stop_price = round(entry_price * (1 - STOP_LOSS_BUFFER if side == SIDE_BUY else 1 + STOP_LOSS_BUFFER), 2)
        take_profit_price = round(entry_price * (1 + RISK_REWARD_RATIO * STOP_LOSS_BUFFER if side == SIDE_BUY else 1 - RISK_REWARD_RATIO * STOP_LOSS_BUFFER), 2)
        
        print(f"🎯 Order Details: Entry Price: {entry_price}, Stop Loss: {stop_price}, Take Profit: {take_profit_price}")
        return entry_price, stop_price, take_profit_price
    except Exception as e:
        print(f"😬 Error placing order: {e}")
        return None, None, None

def display_open_positions():
    """Display open positions with unrealized PnL."""
    try:
        print("📜 Checking open positions...")
        positions = client.futures_position_information()
        open_positions = [pos for pos in positions if float(pos['positionAmt']) != 0]
        
        if open_positions:
            print("💼 Current Open Positions:")
            for pos in open_positions:
                print(f"👉 {pos['symbol']}: Position: {pos['positionAmt']}, Unrealized PnL: {pos['unrealizedProfit']}")
        else:
            print("😴 No open positions. Market's quiet for now.")
    except Exception as e:
        print(f"😬 Error fetching open positions: {e}")

def main():
    print("🚀 Starting your fun and friendly candlestick bot! Let’s make trading exciting! 🤑")
    while True:
        try:
            # Check and display open positions
            display_open_positions()
            
            # Fetch and analyze data
            data = fetch_data(SYMBOL, INTERVAL)
            signal = identify_engulfing_pattern(data)
            
            if signal == "BUY":
                print("📈 Bullish Engulfing Pattern detected! Time to BUY! 🚀")
                place_order(SYMBOL, SIDE_BUY, QUANTITY)
            elif signal == "SELL":
                print("📉 Bearish Engulfing Pattern detected! Time to SELL! 😬")
                place_order(SYMBOL, SIDE_SELL, QUANTITY)
            else:
                print("🤔 No patterns detected. Waiting for the next candle...")
            
            # Wait for the next candlestick interval
            time.sleep(60)
        except Exception as e:
            print(f"😵 Error: {e}")

if __name__ == "__main__":
    main()
