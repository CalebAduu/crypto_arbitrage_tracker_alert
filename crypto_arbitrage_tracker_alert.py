import streamlit as st
import pandas as pd
import requests
from itertools import combinations
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 10 seconds
st_autorefresh(interval=10*1000, key="crypto_refresh")

# Exchanges to fetch
exchanges = ["binance", "kraken", "coinbase", "kucoin", "gateio", "bitmart"]

# Helper functions for fetching prices
def get_binance_price(symbol):
    try:
        data = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
        return float(data['price'])
    except:
        return None

def get_coinbase_price(symbol):
    try:
        data = requests.get(f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot").json()
        return float(data['data']['amount'])
    except:
        return None

def get_kraken_price(symbol):
    try:
        mapping = {"BTC":"XBT", "DOGE":"XDG", "USDT":"USDTZ"}
        sym = mapping.get(symbol, symbol)
        data = requests.get(f"https://api.kraken.com/0/public/Ticker?pair={sym}USD").json()
        pair = list(data['result'].keys())[0]
        return float(data['result'][pair]['c'][0])
    except:
        return None

def get_kucoin_price(symbol):
    try:
        data = requests.get(f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT").json()
        return float(data['data']['price'])
    except:
        return None

def get_gateio_price(symbol):
    try:
        data = requests.get(f"https://api.gateio.ws/api2/1/ticker/{symbol}_USDT").json()
        return float(data['last'])
    except:
        return None

def get_bitmart_price(symbol):
    try:
        data = requests.get(f"https://api-cloud.bitmart.com/spot/v1/ticker?symbol={symbol}_USDT").json()
        return float(data['data']['last_price'])
    except:
        return None

# Mapping exchange to fetch function
exchange_funcs = {
    "binance": get_binance_price,
    "coinbase": get_coinbase_price,
    "kraken": get_kraken_price,
    "kucoin": get_kucoin_price,
    "gateio": get_gateio_price,
    "bitmart": get_bitmart_price
}

# Fetch top 20 cryptos from CoinGecko
def get_top_cryptos(n=20):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency":"usd","order":"market_cap_desc","per_page":n,"page":1,"sparkline":"false"}
    data = requests.get(url, params=params).json()
    return [c['symbol'].upper() for c in data]

# Compute spread between two prices safely
def compute_spread(p1, p2):
    if p1 in (None,0) or p2 in (None,0):
        return None
    return round(abs(p1 - p2), 2)

# Build the table
all_rows = []
top_cryptos = get_top_cryptos(20)

for crypto in top_cryptos:
    row = {"Crypto": crypto}
    prices = {}
    for ex in exchanges:
        prices[ex] = exchange_funcs[ex](crypto)
        row[ex] = prices[ex]
    
    # Compute spreads for all exchange pairs
    for ex1, ex2 in combinations(exchanges, 2):
        row[f"{ex1} vs {ex2}"] = compute_spread(prices[ex1], prices[ex2])
    
    all_rows.append(row)

df = pd.DataFrame(all_rows)

st.title("Top 20 Crypto Exchange vs Exchange Spreads")
st.dataframe(df)
