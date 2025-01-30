import time
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET
import pandas as pd
from ta.momentum import RSIIndicator

# Step 1: Configure API keys
API_KEY = "NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv"
API_SECRET = "4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX"

# Step 2: Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Step 3: Define constants
SYMBOL = "1000PEPEUSDT"  # Replace with your trading pair
INTERVAL = "15m"  # Timeframe for fetching data
QUANTITY = 1350  # Adjust to your desired trade size
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

def fetch_data(symbol, interval):
    """Fetch historical candlestick data."""
    print("Fetching candlestick data... Hold tight!")
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=50)
    data = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"])
    data = data[["timestamp", "open", "high", "low", "close", "volume"]]
    data["close"] = pd.to_numeric(data["close"])
    return data

def calculate_rsi(data):
    """Calculate the RSI indicator."""
    print("Crunching numbers for RSI... Math is fun!")
    rsi = RSIIndicator(close=data["close"], window=RSI_PERIOD).rsi()
    return rsi

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

def main():
    print("Welcome to your friendly trading bot! Let's make some magic happen 🎩✨")
    while True:
        try:
            # Fetch and process data
            data = fetch_data(SYMBOL, INTERVAL)
            rsi = calculate_rsi(data)

            # Get the latest RSI value
            latest_rsi = rsi.iloc[-1]
            print(f"🤓 Latest RSI value: {latest_rsi}")

            # Trading logic
            if latest_rsi > RSI_OVERBOUGHT:
                print("📈 RSI is overbought! Time to hit that SELL button.")
                place_order(SYMBOL, SIDE_SELL, QUANTITY)
            elif latest_rsi < RSI_OVERSOLD:
                print("📉 RSI is oversold! Let's BUY and ride the wave up.")
                place_order(SYMBOL, SIDE_BUY, QUANTITY)
            else:
                print("😴 RSI is in a chill zone. No trades for now. Grab a coffee!")

            # Wait before fetching new data
            print("🕒 Waiting for the next signal... Patience is a virtue.")
            time.sleep(60)
        except Exception as e:
            print(f"🚨 Unexpected error: {e}. The bot will try again soon.")

if __name__ == "__main__":
    main()
