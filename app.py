from fastapi import FastAPI
from binance.client import Client
import pandas as pd

app = FastAPI()

# Binance API keys (Users will input their own)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
client = Client(API_KEY, API_SECRET, tld='com')

@app.get("/")
def home():
    return {"message": "Welcome to the Candlestick Trading API"}

@app.get("/trade")
def trade(symbol: str, quantity: float, order_type: str):
    try:
        if order_type.lower() == "buy":
            order = client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
        elif order_type.lower() == "sell":
            order = client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity)
        else:
            return {"error": "Invalid order type"}
        
        return {"status": "success", "order": order}
    except Exception as e:
        return {"error": str(e)}
