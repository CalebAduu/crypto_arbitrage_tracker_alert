# streamlit_arbitrage.py
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Arbitrage Tracker", layout="wide")

st.title("📈 Crypto Prices & Exchange Spreads")
st.markdown("Monitor top crypto prices across Binance, Coinbase, and Kraken in real-time!")

# ----------------------
# Functions to fetch data
# ----------------------
def get_top_50_cryptos():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50, "page": 1, "sparkline": "false"}
        response = requests.get(url, params=params).json()
        return response
    except:
        return []

def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url).json()
        return float(data['price'])
    except:
        return None

def get_coinbase_price(symbol):
    try:
        url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
        data = requests.get(url).json()
        return float(data['data']['amount'])
    except:
        return None

def get_kraken_price(symbol):
    try:
        special_cases = {"BTC": "XBT", "DOGE": "XDG", "USDT": "USDTZ"}
        kraken_symbol = special_cases.get(symbol, symbol)
        url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}USD"
        data = requests.get(url).json()
        if 'result' in data and len(data['result']) > 0:
            pair = list(data['result'].keys())[0]
            return float(data['result'][pair]['c'][0])
        return None
    except:
        return None

def calculate_spread(prices):
    valid_prices = [p for p in prices if p is not None]
    if not valid_prices:
        return None
    return max(valid_prices) - min(valid_prices)

# ----------------------
# Main App
# ----------------------
refresh = st.button("🔄 Refresh Prices")

cryptos = get_top_50_cryptos()
data = []

for crypto in cryptos[:20]:  # limit to top 20 for performance
    symbol = crypto['symbol'].upper()
    name = crypto['name']

    binance_price = get_binance_price(symbol)
    coinbase_price = get_coinbase_price(symbol)
    kraken_price = get_kraken_price(symbol)
    spread = calculate_spread([binance_price, coinbase_price, kraken_price])

    data.append({
        "Crypto": name,
        "Binance": binance_price,
        "Coinbase": coinbase_price,
        "Kraken": kraken_price,
        "Spread": spread
    })

df = pd.DataFrame(data)
st.table(df)

st.markdown("""
> Notes:  
> - Spread = Highest price - Lowest price across exchanges.  
> - Refresh manually to get latest prices.
""")
