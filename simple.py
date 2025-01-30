import os
from binance.client import Client
from binance.enums import *

# Set up Binance API credentials
API_KEY = "NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv"
API_SECRET = "4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX"

client = Client(API_KEY, API_SECRET, tld='com')

# Define trading pair
SYMBOL = "1000LUNCUSDT"
QUANTITY = 100  # Adjust based on your capital

def place_order(order_type):
    try:
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
            print("Invalid order type.")
            return
        print(f"Order placed: {order}")
    except Exception as e:
        print(f"Error placing order: {e}")

while True:
    action = input("Enter 'buy' or 'sell' to place an order, or 'exit' to quit: ").strip().lower()
    if action in ["buy", "sell"]:
        place_order(action)
    elif action == "exit":
        break
    else:
        print("Invalid input. Please enter 'buy', 'sell', or 'exit'.")
