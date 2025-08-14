import requests
import streamlit as st
import pandas as pd
import time

# Telegram settings
TELEGRAM_BOT_TOKEN = "8211027473:AAEwuL0nkumeqqyE8yaH167MtSsbUK6JJfM"
TELEGRAM_CHAT_ID = "1888691302"

# Exchanges to track
EXCHANGES = [
    "MEXC", "LBank", "Bybit", "Gateio", "CoinEx", "XT",
    "Bitget", "KuCoin", "Binance", "HTX", "BingX", "BitMart"
]

# Minimum and maximum spread percentage
MIN_SPREAD = 2
MAX_SPREAD = 10

# Function to send telegram alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram alert failed: {e}")

# Placeholder: Replace with real futures API calls for each exchange
def get_futures_price(exchange, symbol):
    # Example: here we just return dummy random data for testing
    # Replace with real exchange API calls
    try:
        url_map = {
            "Binance": f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}USDT",
            # Add real endpoints for other exchanges
        }
        url = url_map.get(exchange)
        if url:
            data = requests.get(url).json()
            return float(data['price'])
    except:
        return None
    # For unimplemented exchanges, return None
    return None

# Top 20 crypto symbols (common futures symbols)
TOP_20 = [
    "BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE", "DOT", "MATIC", "LTC",
    "AVAX", "UNI", "SHIB", "LINK", "ATOM", "ALGO", "VET", "FIL", "TRX", "ICP"
]

st.title("Futures Crypto Arbitrage Tracker")
st.write(f"Tracking top 20 crypto futures across {len(EXCHANGES)} exchanges")

# Streamlit loop
while True:
    data = []
    alerts = []
    for symbol in TOP_20:
        prices = {}
        for ex in EXCHANGES:
            price = get_futures_price(ex, symbol)
            if price:
                prices[ex] = price
        if not prices:
            continue

        max_price = max(prices.values())
        min_price = min(prices.values())
        spread_percent = (max_price - min_price) / min_price * 100

        row = {"Crypto": symbol}
        row.update({ex: prices.get(ex, None) for ex in EXCHANGES})
        row["Spread %"] = round(spread_percent, 2)
        data.append(row)

        # Telegram alert if spread is between min and max threshold
        if MIN_SPREAD <= spread_percent <= MAX_SPREAD:
            msg = f"Arbitrage Opportunity: {symbol}\nSpread: {spread_percent:.2f}%\nPrices: {prices}"
            send_telegram_alert(msg)
            alerts.append(symbol)

    df = pd.DataFrame(data)
    st.dataframe(df)

    if alerts:
        st.success(f"Alerts sent for: {', '.join(alerts)}")

    time.sleep(60)  # update every 60 seconds


