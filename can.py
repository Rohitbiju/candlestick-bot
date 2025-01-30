import os
from binance.client import Client
from binance.enums import *
import pandas as pd
import time
import random

# Set up Binance API credentials
API_KEY = "NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv"
API_SECRET = "4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX"

client = Client(API_KEY, API_SECRET, tld='com')

# Define trading pair
SYMBOL = "1000LUNCUSDT"
QUANTITY = 150  # Adjust based on your capital

funny_responses = [
    "Deploying financial wizardry... 🧙‍♂️✨",
    "HODL or YOLO? Oh wait, I decide! 😆",
    "Engulfing detected! It's go time! 🚀",
    "Placing order faster than your ex moved on! 💔💸",
    "Risking it all like a game of rock-paper-scissors! ✊✋✌️"
]

def get_candlestick_data():
    try:
        klines = client.futures_klines(symbol=SYMBOL, interval=Client.KLINE_INTERVAL_3MINUTE, limit=5)
        df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"])
        df["open"] = df["open"].astype(float)
        df["close"] = df["close"].astype(float)
        return df
    except Exception as e:
        print(f"Error fetching candlestick data: {e}")
        return None

def detect_engulfing_pattern():
    df = get_candlestick_data()
    if df is None:
        return None
    last_candle = df.iloc[-1]
    prev_candle = df.iloc[-2]
    
    if last_candle["close"] > last_candle["open"] and prev_candle["close"] < prev_candle["open"] and last_candle["close"] > prev_candle["open"] and last_candle["open"] < prev_candle["close"]:
        return "bullish"
    elif last_candle["close"] < last_candle["open"] and prev_candle["close"] > prev_candle["open"] and last_candle["close"] < prev_candle["open"] and last_candle["open"] > prev_candle["close"]:
        return "bearish"
    return None

def place_order(order_type):
    try:
        print(random.choice(funny_responses))
        if order_type == "buy":
            order = client.futures_create_order(
                symbol=SYMBOL,
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quantity=QUANTITY
            )
        elif order_type == "sell":
            order = client.futures_create_order(
                symbol=SYMBOL,
                side=SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=QUANTITY
            )
        else:
            print("Invalid order type. Try again, rookie! 😜")
            return
        print(f"Order placed successfully: {order}")
    except Exception as e:
        print(f"Oops! Something broke: {e}")

while True:
    pattern = detect_engulfing_pattern()
    if pattern == "bullish":
        print("🔥 Bullish Engulfing detected! Moon mission commencing... 🚀")
        place_order("buy")
    elif pattern == "bearish":
        print("💀 Bearish Engulfing detected! Jumping ship! 🏴‍☠️")
        place_order("sell")
    else:
        print("😴 No pattern detected. Bot is taking a nap... Zzz")
    time.sleep(10)
