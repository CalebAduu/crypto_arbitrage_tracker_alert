import streamlit as st
import requests
import pandas as pd

# List of exchanges to check
EXCHANGES = ["Binance", "Kraken", "Coinbase"]  # you can add more later

# Function to get price from Binance
def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url).json()
        return float(data['price'])
    except:
        return None

# Function to get price from Coinbase
def get_coinbase_price(symbol):
    try:
        url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
        data = requests.get(url).json()
        return float(data['data']['amount'])
    except:
        return None

# Function to get price from Kraken
def get_kraken_price(symbol):
    try:
        special_cases = {"BTC": "XBT"}
        kraken_symbol = special_cases.get(symbol, symbol)
        url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}USD"
        data = requests.get(url).json()
        pair = list(data['result'].keys())[0]
        return float(data['result'][pair]['c'][0])
    except:
        return None

# Map exchange names to functions
EXCHANGE_FUNCS = {
    "Binance": get_binance_price,
    "Kraken": get_kraken_price,
    "Coinbase": get_coinbase_price
}

# Get top N cryptocurrencies
def get_top_cryptos(n=20):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1,
        "sparkline": "false"
    }
    data = requests.get(url, params=params).json()
    return [(c['symbol'].upper(), c['name']) for c in data]

# Build dataframe with prices and spreads
def build_price_df(cryptos):
    rows = []
    for symbol, name in cryptos:
        prices = {}
        for ex in EXCHANGES:
            prices[ex] = EXCHANGE_FUNCS[ex](symbol)
        # Compute max spread between exchanges
        valid_prices = [p for p in prices.values() if p is not None]
        spread = max(valid_prices) - min(valid_prices) if len(valid_prices) > 1 else 0
        row = {"Crypto": name, **prices, "Spread (USD)": spread}
        rows.append(row)
    return pd.DataFrame(rows)

# Streamlit app
st.title("Crypto Exchange Price Spreads")
cryptos = get_top_cryptos()
df = build_price_df(cryptos)
st.dataframe(df)
