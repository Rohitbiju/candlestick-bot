from binance.client import Client

API_KEY = 'NPUodhVWsD30tpiqwS6jdKMVLj880MXBr1t5IGsJEAH6Q6mVWXdKxDI5yuVtAJQv'
SECRET_KEY = '4xi1JmzETuBygsYDSZly0eDWVUTDmmxpnvMaJPua9u4i5o2ca1kymwmqWMxUMxoX'

try:
    client = Client(API_KEY, SECRET_KEY)
    print("✅ Successfully connected to Binance!")
except Exception as e:
    print(f"❌ Failed to connect to Binance: {e}")
    exit()

# Get and display account information
try:
    print("\n🔍 Fetching Spot account details...")
    account_info = client.get_account()

    print("\n📊 Spot Account Overview:")
    print(f"- Account Type: {account_info['accountType']}")
    print(f"- Balances:")
    for balance in account_info['balances']:
        if float(balance['free']) > 0 or float(balance['locked']) > 0:
            print(f"  • {balance['asset']}: Free = {balance['free']}, Locked = {balance['locked']}")
    print("\n✅ Spot account details retrieved successfully!")
except Exception as e:
    print(f"❌ Error fetching Spot account details: {e}")

# Get and display Futures wallet information
try:
    print("\n🔍 Fetching Futures wallet details...")
    futures_account = client.futures_account()

    print("\n📊 Futures Account Overview:")
    print(f"- Total Wallet Balance: {futures_account['totalWalletBalance']} USDT")
    print(f"- Total Unrealized Profit: {futures_account['totalUnrealizedProfit']} USDT")
    print("- Open Positions:")
    for position in futures_account['positions']:
        if float(position['positionAmt']) != 0:
            print(f"  • Symbol: {position['symbol']}")
            print(f"    - Position Amount: {position['positionAmt']}")
            print(f"    - Entry Price: {position['entryPrice']}")
            print(f"    - Unrealized PnL: {position['unrealizedProfit']} USDT")
            print(f"    - Margin Type: {position['marginType']}")
    print("\n✅ Futures wallet details retrieved successfully!")
except Exception as e:
    print(f"❌ Error fetching Futures wallet details: {e}")