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
    print("\n🔍 Fetching account details...")
    account_info = client.get_account()

    print("\n📊 Account Overview:")
    print(f"- Account Type: {account_info['accountType']}")
    print(f"- Balances:")
    for balance in account_info['balances']:
        if float(balance['free']) > 0 or float(balance['locked']) > 0:
            print(f"  • {balance['asset']}: Free = {balance['free']}, Locked = {balance['locked']}")
    print("\n✅ Account details retrieved successfully!")
except Exception as e:
    print(f"❌ Error fetching account details: {e}")