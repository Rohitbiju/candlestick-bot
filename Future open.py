import time
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL

# Binance API Keys
API_KEY = "NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv"
API_SECRET = "4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX"

# Connect to Binance
client = Client(API_KEY, API_SECRET)

# Set your risk threshold for suggestions
profit_threshold = 0.02  # 2% profit to suggest closing
loss_threshold = -0.02   # -2% loss to suggest closing

# Function to get the open positions from Binance Futures account
def get_open_positions():
    try:
        positions = client.futures_position_information()
        print(f"Open positions response: {positions}")  # Debugging: print the full response
        open_positions = [pos for pos in positions if float(pos['positionAmt']) != 0]
        return open_positions
    except Exception as e:
        print(f"❌ Error fetching open positions: {e}")
        return []

# Function to check the current profit/loss and suggest an action
def check_positions():
    open_positions = get_open_positions()
    
    if not open_positions:
        print("✅ No open positions currently.")
        return
    
    for position in open_positions:
        symbol = position['symbol']
        position_amt = float(position['positionAmt'])
        entry_price = float(position['entryPrice'])
        mark_price = float(position['markPrice'])
        unrealized_profit = float(position.get('unrealizedProfit', 0))  # Handle missing key with default value
        
        # Calculate the percentage profit/loss
        pnl_percentage = (unrealized_profit / (entry_price * position_amt)) * 100

        # Display position information
        print(f"\nPosition Info for {symbol}:")
        print(f"Entry Price: {entry_price} | Current Price: {mark_price}")
        print(f"Unrealized PnL: {unrealized_profit} | PnL Percentage: {pnl_percentage:.2f}%")

        # Suggest action based on thresholds
        if pnl_percentage >= profit_threshold * 100:
            print(f"🟢 Suggestion: Close Position for {symbol} as profit is {pnl_percentage:.2f}%!")
        elif pnl_percentage <= loss_threshold * 100:
            print(f"🔴 Suggestion: Close Position for {symbol} as loss is {pnl_percentage:.2f}%!")
        else:
            print(f"🟡 Suggestion: Hold position for {symbol}.")
    
# Run the bot to check positions and suggest actions
print("🚀 Starting position monitor bot...")

while True:
    check_positions()
    time.sleep(60)  # Check every minute