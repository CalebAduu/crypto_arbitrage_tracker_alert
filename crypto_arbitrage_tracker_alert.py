import streamlit as st
import requests
import pandas as pd
from itertools import combinations

# Exchanges to compare
exchanges = ["binance", "kraken", "coinbase-pro", "bitmart", "kucoin", "gateio"]

# Get top N cryptocurrencies by market cap
def get_top_cryptos(n=20):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1,
        "sparkline": "false"
    }
    response = requests.get(url, params=params).json()
    return [c["id"] for c in response]

# Fetch base prices from CoinGecko
def get_prices(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params).json()
    return response.get(crypto, {})

# Simulate exchange prices for demo (replace with real API calls)
def simulate_exchange_prices(base_price):
    prices = {}
    for ex in exchanges:
        if base_price is not None:
            # small variation per exchange
            prices[ex] = round(base_price * (1 + 0.01 * (hash(ex) % 5 - 2)), 2)
        else:
            prices[ex] = None
    return prices

# Compute spread safely
def compute_spread(price1, price2):
    if price1 in (None, 0) or price2 in (None, 0):
        return None
    return round(abs(price1 - price2), 2)

# Build table
all_rows = []
top_cryptos = get_top_cryptos(20)

for crypto in top_cryptos:
    prices = get_prices(crypto)
    base_price = prices.get("usd")
    exchange_prices = simulate_exchange_prices(base_price)
    
    row = {"Crypto": crypto.capitalize()}
    
    # Compute spread for every exchange pair
    for ex1, ex2 in combinations(exchanges, 2):
        row[f"{ex1} vs {ex2}"] = compute_spread(exchange_prices[ex1], exchange_prices[ex2])
    
    all_rows.append(row)

df = pd.DataFrame(all_rows)

st.title("Top 20 Cryptos Exchange Spread Matrix")
st.dataframe(df)

