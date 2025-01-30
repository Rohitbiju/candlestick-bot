import time
import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
from ta.momentum import RSIIndicator

# Initialize Binance client
API_KEY = "NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv"
API_SECRET = "4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX"
client = Client(API_KEY, API_SECRET)

# Parameters
SYMBOL = "1000LUNCUSDT"
INTERVAL = "15m"  # Timeframe for fetching candlestick data
QUANTITY = 250  # Adjust based on your account size
SHORT_EMA = 9
LONG_EMA = 26

def fetch_data(symbol, interval, limit=100):
    """Fetch historical candlestick data."""
    print("Fetching candlestick data... Hold tight!")
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=limit)
    data = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    data = data[["timestamp", "open", "high", "low", "close", "volume"]]
    data["close"] = pd.to_numeric(data["close"])
    return data

def calculate_ema(data, short_window=SHORT_EMA, long_window=LONG_EMA):
    """Calculate fast and slow EMAs."""
    print("Calculating EMAs... Trend is your friend!")
    data['EMA_Short'] = data['close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_Long'] = data['close'].ewm(span=long_window, adjust=False).mean()
    return data

def generate_signals(data):
    """Generate buy/sell signals based on EMA crossover."""
    print("Generating trade signals...")
    data['Signal'] = 0
    data['Signal'] = np.where(data['EMA_Short'] > data['EMA_Long'], 1, -1)
    data['Position'] = data['Signal'].diff()  # Detect changes in signals
    return data

def place_order(symbol, side, quantity):
    """Place a market order."""
    try:
        print(f"Attempting to place a {'BUY' if side == SIDE_BUY else 'SELL'} order for {quantity} {symbol}... Fingers crossed!")
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"🎉 Success! Order placed: {order}")
    except Exception as e:
        print(f"😢 Oops! Something went wrong: {e}")

def place_trade_based_on_ema(data, symbol, quantity):
    """Place trades based on EMA signals."""
    latest_position = data.iloc[-1]['Position']
    if latest_position == 1:  # Golden Cross (Buy Signal)
        print("📈 EMA crossover detected: BUY signal!")
        place_order(symbol, SIDE_BUY, quantity)
    elif latest_position == -1:  # Death Cross (Sell Signal)
        print("📉 EMA crossover detected: SELL signal!")
        place_order(symbol, SIDE_SELL, quantity)
    else:
        print("😴 No actionable EMA signal at the moment.")

def main():
    print("Welcome to your EMA trading bot! 🛠️📊")
    while True:
        try:
            # Fetch and process data
            data = fetch_data(SYMBOL, INTERVAL)
            data = calculate_ema(data, short_window=SHORT_EMA, long_window=LONG_EMA)
            data = generate_signals(data)

            # Execute trades based on signals
            place_trade_based_on_ema(data, SYMBOL, QUANTITY)

            # Wait before fetching new data
            print("🕒 Waiting for the next signal... Patience is a virtue.")
            time.sleep(60)
        except Exception as e:
            print(f"🚨 Unexpected error: {e}. The bot will try again soon.")

if __name__ == "__main__":
    main()