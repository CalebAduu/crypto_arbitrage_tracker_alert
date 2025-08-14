import streamlit as st
import requests
import pandas as pd
import time
from itertools import combinations

st.set_page_config(page_title="Crypto Arbitrage Tracker", layout="wide")

# List of exchanges and their public endpoints (futures)
EXCHANGES = {
    "Binance": lambda symbol: f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}USDT",
    "KuCoin": lambda symbol: f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT",
    "Gateio": lambda symbol: f"https://api.gateio.ws/api2/1/tickers/{symbol}_USDT",
    "Bybit": lambda symbol: f"https://api.bybit.com/v2/public/tickers?symbol={symbol}USDT",
    "BitMart": lambda symbol: f"https://api-cloud.bitmart.com/spot/v1/ticker?symbol={symbol}_USDT",
    # Add more exchanges here if they have public endpoints
}

# Top 20 cryptos symbols for futures (example)
TOP_20_SYMBOLS = ["BTC", "ETH", "SOL", "BNB", "ADA", "XRP", "DOGE", "DOT", "AVAX", "MATIC",
                  "LTC", "TRX", "LINK", "ATOM", "ETC", "NEAR", "ALGO", "FTM", "VET", "FIL"]

def fetch_price(exchange, symbol):
    try:
        url = EXCHANGES[exchange](symbol)
        response = requests.get(url, timeout=5).json()
        # Parse response per exchange
        if exchange == "Binance":
            return float(response.get('price', 0))
        elif exchange == "KuCoin":
            return float(response.get('data', {}).get('price', 0))
        elif exchange == "Gateio":
            return float(response.get('last', 0)) if isinstance(response, dict) else float(response[0]['last'])
        elif exchange == "Bybit":
            return float(response.get('result', [{}])[0].get('last_price', 0))
        elif exchange == "BitMart":
            return float(response.get('data', {}).get('tickers', [{}])[0].get('last_price', 0))
        return 0
    except:
        return 0

def get_spreads(prices_dict):
    """Compute spreads between every pair of exchanges"""
    spreads = []
    for ex1, ex2 in combinations(prices_dict.keys(), 2):
        p1 = prices_dict[ex1]
        p2 = prices_dict[ex2]
        if p1 > 0 and p2 > 0:
            spread = abs(p1 - p2) / min(p1, p2) * 100
            spreads.append((ex1, ex2, round(spread, 2)))
    return spreads

st.title("Crypto Futures Arbitrage Tracker (Top 20)")

refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)

while True:
    table_data = []
    for symbol in TOP_20_SYMBOLS:
        prices = {ex: fetch_price(ex, symbol) for ex in EXCHANGES}
        spreads = get_spreads(prices)
        max_spread = max([s[2] for s in spreads], default=0)
        table_data.append({
            "Crypto": symbol,
            **prices,
            "Max Spread (%)": max_spread,
            "Spreads": spreads
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

    time.sleep(refresh_interval)
    st.experimental_rerun()
