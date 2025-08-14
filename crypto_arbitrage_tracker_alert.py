import streamlit as st
import requests
import pandas as pd

# List of top cryptocurrencies
cryptos = ["bitcoin", "ethereum", "solana"]

# List of exchanges you want to compare
exchanges = ["binance", "kraken", "coinbase-pro", "bitmart", "kucoin", "gateio"]

# Fetch prices from CoinGecko public API
def get_prices(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": crypto,
        "vs_currencies": "usd",
        "include_market_cap": "false",
        "include_24hr_vol": "false",
        "include_24hr_change": "true",
        "include_last_updated_at": "false"
    }
    response = requests.get(url, params=params).json()
    return response.get(crypto, {})

# For demonstration, we'll simulate exchange prices slightly differently
def simulate_exchange_prices(base_price):
    prices = {}
    for ex in exchanges:
        if base_price is not None:
            # add small random difference for demo
            prices[ex] = round(base_price * (1 + 0.01 * (hash(ex) % 5 - 2)), 2)
        else:
            prices[ex] = None
    return prices

# Compute spread between two exchanges safely
def compute_spread(price1, price2):
    if price1 in (None, 0) or price2 in (None, 0):
        return None
    return abs(price1 - price2)

# Build table
data = []
for crypto in cryptos:
    prices = get_prices(crypto)
    base_price = prices.get("usd")
    exchange_prices = simulate_exchange_prices(base_price)
    
    # Compute maximum spread between any two exchanges
    valid_prices = [p for p in exchange_prices.values() if p not in (None, 0)]
    max_spread = max(valid_prices) - min(valid_prices) if valid_prices else None
    
    row = {"Crypto": crypto.capitalize()}
    row.update(exchange_prices)
    row["Max Spread"] = max_spread
    data.append(row)

df = pd.DataFrame(data)

st.title("Crypto Prices & Exchange Spreads")
st.dataframe(df)
