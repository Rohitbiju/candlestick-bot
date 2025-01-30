import time
import pandas as pd
from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET

# Binance API Keys
API_KEY = 'NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv'
SECRET_KEY = '4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX'

# Connect to Binance
client = Client(API_KEY, SECRET_KEY)

# Set leverage
def set_leverage(symbol, leverage):
    try:
        response = client.futures_change_leverage(symbol=symbol, leverage=leverage)
        print(f"✅ Leverage set to {leverage}x for {symbol}")
        return response
    except Exception as e:
        print(f"❌ Error setting leverage: {e}")
        return None

# Fetch historical data
def fetch_klines(symbol, interval, lookback):
    try:
        klines = client.futures_klines(symbol=symbol, interval=interval, limit=lookback)
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                             'close_time', 'quote_asset_volume', 'trades',
                                             'taker_buy_base', 'taker_buy_quote', 'ignore'])
        data['close'] = data['close'].astype(float)
        return data
    except Exception as e:
        print(f"❌ Error fetching klines: {e}")
        return None

# Calculate moving averages
def calculate_moving_averages(data, short_window, long_window):
    data['SMA_Short'] = data['close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['close'].rolling(window=long_window).mean()
    return data

# Place market order
def place_order(symbol, side, quantity):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"✅ Order placed: {order}")
        return order  # Return the order to track entry price
    except Exception as e:
        print(f"❌ Error placing order: {e}")
        return None

# Check Stop-Loss and Take-Profit
def check_exit_conditions(symbol, entry_price, stop_loss, take_profit, side):
    try:
        # Fetch the current price
        ticker = client.futures_symbol_ticker(symbol=symbol)
        current_price = float(ticker['price'])

        # Check Stop-Loss or Take-Profit
        if side == SIDE_BUY:  # Long position
            if current_price <= stop_loss:
                print(f"🔴 Stop-Loss hit! Current Price: {current_price}. Closing position.")
                place_order(symbol, SIDE_SELL, quantity)
                return True
            elif current_price >= take_profit:
                print(f"🟢 Take-Profit hit! Current Price: {current_price}. Closing position.")
                place_order(symbol, SIDE_SELL, quantity)
                return True
        elif side == SIDE_SELL:  # Short position
            if current_price >= stop_loss:
                print(f"🔴 Stop-Loss hit! Current Price: {current_price}. Closing position.")
                place_order(symbol, SIDE_BUY, quantity)
                return True
            elif current_price <= take_profit:
                print(f"🟢 Take-Profit hit! Current Price: {current_price}. Closing position.")
                place_order(symbol, SIDE_BUY, quantity)
                return True
        return False
    except Exception as e:
        print(f"❌ Error checking exit conditions: {e}")
        return False

# Calculate the quantity based on USDT amount
def calculate_quantity(symbol, usdt_amount):
    try:
        ticker = client.futures_symbol_ticker(symbol=symbol)
        current_price = float(ticker['price'])
        quantity = usdt_amount / current_price
        return round(quantity, 3)  # Round to 3 decimal places for accuracy
    except Exception as e:
        print(f"❌ Error calculating quantity: {e}")
        return 0

# Strategy logic
def strategy(symbol, interval, usdt_amount, leverage, short_window=9, long_window=21, risk_reward_ratio=2):
    global entry_price, stop_loss, take_profit, in_position

    # Set leverage
    set_leverage(symbol, leverage)

    data = fetch_klines(symbol, interval, 50)
    if data is None:
        return

    # Calculate indicators
    data = calculate_moving_averages(data, short_window, long_window)

    # Get the last two rows to check crossover
    last_row = data.iloc[-1]
    prev_row = data.iloc[-2]

    # Calculate the quantity based on USDT amount
    quantity = calculate_quantity(symbol, usdt_amount)

    # Check if already in a position
    if in_position:
        exit_condition = check_exit_conditions(symbol, entry_price, stop_loss, take_profit, position_side)
        if exit_condition:
            in_position = False  # Reset position status
        return

    # Check buy signal (short SMA crosses above long SMA)
    if prev_row['SMA_Short'] < prev_row['SMA_Long'] and last_row['SMA_Short'] > last_row['SMA_Long']:
        print(f"📈 Buy Signal Detected! Placing BUY order for {symbol}.")
        order = place_order(symbol, SIDE_BUY, quantity)
        if order:
            entry_price = float(order['fills'][0]['price'])
            stop_loss = entry_price * (1 - 0.01)  # 1% stop-loss
            take_profit = entry_price * (1 + 0.02)  # 2% take-profit
            position_side = SIDE_BUY
            in_position = True

    # Check sell signal (short SMA crosses below long SMA)
    elif prev_row['SMA_Short'] > prev_row['SMA_Long'] and last_row['SMA_Short'] < last_row['SMA_Long']:
        print(f"📉 Sell Signal Detected! Placing SELL order for {symbol}.")
        order = place_order(symbol, SIDE_SELL, quantity)
        if order:
            entry_price = float(order['fills'][0]['price'])
            stop_loss = entry_price * (1 + 0.02)  # 2% stop-loss
            take_profit = entry_price * (1 - 0.04)  # 4% take-profit
            position_side = SIDE_SELL
            in_position = True

# Initialize variables
symbol = '1000BONKUSDT'    # Trading pair
interval = '1m'       # Candlestick interval (e.g., 1m, 5m, 1h)
usdt_amount = 10      # USDT amount to invest per trade
leverage = 20         # Leverage for the position
entry_price = 0       # Entry price for the current trade
stop_loss = 0         # Stop-loss price
take_profit = 0       # Take-profit price
position_side = None  # Current position side (BUY/SELL)
in_position = False   # Whether currently in a trade

# Run the bot
print("🚀 Starting trading bot with USDT-based quantity, Leverage, Stop-Loss, and Take-Profit...")
while True:
    strategy(symbol, interval, usdt_amount, leverage)
    time.sleep(60)  # Wait for the next candle
