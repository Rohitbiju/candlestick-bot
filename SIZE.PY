import time
from binance.client import Client

# Initialize Binance Client (replace with your API credentials)
api_key = 'NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv'
api_secret = '4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX'
client = Client(api_key, api_secret)

# Get the allowed precision for the asset
def get_precision(symbol):
    # Fetch exchange info to get precision details for the symbol
    info = client.futures_exchange_info()
    for s in info['symbols']:
        if s['symbol'] == symbol:
            # Fetch precision for quantity
            quantity_precision = s['quantityPrecision']
            return quantity_precision
    return 0  # Default precision if symbol not found

# Place an order with the correct quantity
def place_order(symbol, usdt_amount, leverage, position_side):
    try:
        # Get the current market price for the symbol
        market_price = float(client.futures_symbol_ticker(symbol=symbol)['price'])
        
        # Calculate the quantity of asset to trade based on USDT amount
        quantity = usdt_amount / market_price
        
        # Get the precision for the symbol
        quantity_precision = get_precision(symbol)
        
        # Round the quantity to the allowed precision
        quantity = round(quantity, quantity_precision)
        
        # Print the rounded quantity for debugging
        print(f"Rounded quantity: {quantity} (Precision: {quantity_precision})")
        
        # Set leverage
        client.futures_change_leverage(symbol=symbol, leverage=leverage)
        
        # Check if we are already in a position (prevent multiple trades simultaneously)
        if position_side is not None:
            print(f"❌ Already in a {position_side} position. Waiting to exit the current position.")
            return None, position_side
        
        # Place the order (Buy or Sell based on strategy)
        if position_side is None:  # No position, so we can open a new one
            # Open a long position (BUY)
            order = client.futures_market_buy(symbol=symbol, quantity=quantity)
            position_side = "BUY"  # Update position to BUY
            print(f"✅ Buy order placed: {order}")
        
        return order, position_side
    
    except Exception as e:
        print(f"❌ Error placing order: {e}")
        return None, position_side

# Function to close the position (buy or sell based on the current position)
def close_position(symbol, position_side, quantity):
    try:
        if position_side == "BUY":
            # Close the long position by selling
            order = client.futures_market_sell(symbol=symbol, quantity=quantity)
            print(f"✅ Sell order placed to close long position: {order}")
            position_side = None  # Reset position to None
        elif position_side == "SELL":
            # Close the short position by buying
            order = client.futures_market_buy(symbol=symbol, quantity=quantity)
            print(f"✅ Buy order placed to close short position: {order}")
            position_side = None  # Reset position to None
        return position_side
    except Exception as e:
        print(f"❌ Error closing position: {e}")
        return position_side

# Main loop for trading
symbol = '1000BONKUSDT'  # Example trading pair
usdt_amount = 6           # USDT amount to invest per trade
leverage = 20             # Leverage for the position
position_side = None      # Current position side (BUY/SELL)

while True:
    if position_side is None:
        # Place an order with USDT amount and leverage
        order, position_side = place_order(symbol, usdt_amount, leverage, position_side)
        if order:
            # Wait for the order to be placed
            print("Waiting for the next action...")
            time.sleep(60)
    
    # You can implement your exit strategy here (e.g., take profit, stop loss, etc.)
    # For now, we're just running the loop to place orders.
    
    # Example of closing the position (this could be triggered based on your strategy)
    if position_side == "BUY" and some_condition_to_close_position():  # Define your condition
        position_side = close_position(symbol, position_side, quantity)
    
    # Repeat the loop (or adjust as necessary)
    time.sleep(60)
