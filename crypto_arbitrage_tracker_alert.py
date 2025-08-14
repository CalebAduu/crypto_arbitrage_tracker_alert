import streamlit as st
import requests
import pandas as pd
import numpy as np
import itertools
import time

st.set_page_config(page_title="Crypto Exchange Spread Tracker", layout="wide")

EXCHANGES = ["Binance", "KuCoin", "Gateio", "BitMart"]  # add more
TOP_N = 20  # top 20 cryptos

# Mapping of symbols for exchanges if needed
SYMBOL_OVERRIDES = {"BTC": "BTC", "ETH": "ETH", "SOL": "SOL"}

# Functions to get prices from each exchange
def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url).json()
        return float(data['price'])
    except:
        return None

def get_kucoin_price(symbol):
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT"
        data = requests.get(url).json()
        return float(data['data']['price'])
    except:
        return None

def get_gateio_price(symbol):
    try:
        url = f"https://api.gateio.ws/api2/1/ticker/{symbol}_USDT"
        data = requests.get(url).json()
        return float(data['last'])
    except:
        return None

def get_bitmart_price(symbol):
    try:
        url = f"https://api-cloud.bitmart.com/spot/v1/ticker?symbol={symbol}_USDT"
        data = requests.get(url).json()
        return float(data['data'][0]['last_price'])
    except:
        return None

EXCHANGE_FUNCS = {
    "Binance": get_binance_price,
    "KuCoin": get_kucoin_price,
    "Gateio": get_gateio_price,
    "BitMart": get_bitmart_price
}

# Get top cryptos from CoinGecko
def get_top_cryptos(n=TOP_N):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": n, "page": 1, "sparkline": "false"}
    data = requests.get(url, params=params).json()
    return [coin['symbol'].upper() for coin in data]

def fetch_prices():
    cryptos = get_top_cryptos()
    rows = []

    for symbol in cryptos:
        row = {"Crypto": symbol}
        prices = {}
        for exchange in EXCHANGES:
            func = EXCHANGE_FUNCS.get(exchange)
            if func:
                price = func(symbol)
                row[exchange] = price if price is not None else np.nan
                prices[exchange] = price
        # Compute all exchange-to-exchange spreads
        spread_list = []
        for ex1, ex2 in itertools.combinations(EXCHANGES, 2):
            p1 = prices.get(ex1)
            p2 = prices.get(ex2)
            if p1 and p2:
                spread = abs(p1 - p2)
                spread_list.append(f"{ex1}-{ex2}: {spread:.2f}")
        row["Spreads"] = ", ".join(spread_list)
        rows.append(row)

    df = pd.DataFrame(rows)
    # Ensure all numeric columns are floats
    for ex in EXCHANGES:
        df[ex] = df[ex].fillna(0.0).astype(float)
    return df

st.title("Crypto Exchange Spread Tracker")

# Auto-refresh every 30 seconds
REFRESH_INTERVAL = 30
placeholder = st.empty()

while True:
    df = fetch_prices()
    with placeholder.container():
        st.dataframe(df)
        st.write(f"Last update: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    time.sleep(REFRESH_INTERVAL)
