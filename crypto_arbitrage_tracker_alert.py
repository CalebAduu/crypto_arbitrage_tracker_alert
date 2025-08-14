import streamlit as st
import requests
import time

st.set_page_config(page_title="Crypto Arbitrage Tracker", layout="wide")

# -----------------------------
# Helper functions
# -----------------------------

def get_top_50_cryptos():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.warning(f"Failed to fetch top cryptos: {e}")
        return []

def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url, timeout=5).json()
        return float(data['price']) if 'price' in data else None
    except:
        return None

def get_coinbase_price(symbol):
    try:
        url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
        data = requests.get(url, timeout=5).json()
        return float(data['data']['amount']) if 'data' in data else None
    except:
        return None

def get_kraken_price(symbol):
    try:
        special_cases = {"BTC": "XBT", "DOGE": "XDG", "USDT": "USDTZ"}
        kraken_symbol = special_cases.get(symbol, symbol)
        url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}USD"
        data = requests.get(url, timeout=5).json()
        if 'result' in data and len(data['result']) > 0:
            pair = list(data['result'].keys())[0]
            return float(data['result'][pair]['c'][0])
        return None
    except:
        return None

def calculate_spread(prices):
    valid_prices = [p for p in prices if p is not None]
    if not valid_prices:
        return 0.0
    return max(valid_prices) - min(valid_prices)

# -----------------------------
# Streamlit layout
# -----------------------------

st.title("📊 Crypto Prices & Exchange Spreads")

# Select cryptos to track
cryptos_data = get_top_50_cryptos()
crypto_names = [c['name'] for c in cryptos_data]
selected_cryptos = st.multiselect("Select Cryptos to Track", crypto_names, default=["Bitcoin", "Ethereum", "Solana"])

# Refresh interval (seconds)
refresh_interval = st.slider("Refresh Interval (seconds)", min_value=5, max_value=60, value=10)

placeholder = st.empty()

while True:
    display_data = []
    for crypto in cryptos_data:
        if crypto['name'] not in selected_cryptos:
            continue
        symbol = crypto['symbol'].upper()
        binance = get_binance_price(symbol)
        coinbase = get_coinbase_price(symbol)
        kraken = get_kraken_price(symbol)
        spread = calculate_spread([binance, coinbase, kraken])

        display_data.append({
            "Crypto": crypto['name'],
            "Binance": binance,
            "Coinbase": coinbase,
            "Kraken": kraken,
            "Spread": spread
        })

    placeholder.table(display_data)
    time.sleep(refresh_interval)
