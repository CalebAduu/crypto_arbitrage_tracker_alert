import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Crypto Arbitrage Tracker", layout="wide")

# List of exchanges
EXCHANGES = [
    "Binance", "HTX", "BingX", "Bybit", "CoinEx", "Bitget", 
    "MEXC", "LBank", "XT", "BitMart", "KuCoin", "Gate.io", "Kraken"
]

# Functions to fetch prices from public APIs
def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        return float(requests.get(url).json()['price'])
    except:
        return None

def get_htx_price(symbol):
    try:
        url = f"https://api.huobi.pro/market/trade?symbol={symbol.lower()}usdt"
        data = requests.get(url).json()
        return float(data['tick']['data'][0]['price'])
    except:
        return None

def get_bingx_price(symbol):
    try:
        url = f"https://api.bingx.com/api/v1/market/ticker?symbol={symbol}USDT"
        data = requests.get(url).json()
        return float(data['data']['lastPrice'])
    except:
        return None

# Add other exchange functions here in similar format...
# Bybit, CoinEx, Bitget, MEXC, LBank, XT, BitMart

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

def get_kraken_price(symbol):
    try:
        special_cases = {"BTC": "XBT", "ETH": "ETH", "SOL": "SOL"}
        kraken_symbol = special_cases.get(symbol, symbol)
        url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}USD"
        data = requests.get(url).json()
        pair = list(data['result'].keys())[0]
        return float(data['result'][pair]['c'][0])
    except:
        return None

# Map exchanges to their functions
EXCHANGE_FUNCS = {
    "Binance": get_binance_price,
    "HTX": get_htx_price,
    "BingX": get_bingx_price,
    "KuCoin": get_kucoin_price,
    "Gate.io": get_gateio_price,
    "Kraken": get_kraken_price,
    # Add other exchanges here...
}

# Top 20 cryptos (Coingecko)
def get_top_20_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 20, "page": 1}
    data = requests.get(url, params=params).json()
    return [coin['symbol'].upper() for coin in data]

# Fetch prices for all exchanges and cryptos
def fetch_all_prices():
    cryptos = get_top_20_cryptos()
    all_prices = {}
    for symbol in cryptos:
        all_prices[symbol] = {}
        for ex in EXCHANGES:
            func = EXCHANGE_FUNCS.get(ex)
            if func:
                all_prices[symbol][ex] = func(symbol)
            else:
                all_prices[symbol][ex] = None
    return all_prices

# Calculate spreads between all exchange pairs
def calculate_spreads(prices):
    spread_data = []
    for symbol, ex_prices in prices.items():
        for ex1 in EXCHANGES:
            for ex2 in EXCHANGES:
                if ex1 != ex2:
                    p1 = ex_prices.get(ex1)
                    p2 = ex_prices.get(ex2)
                    if p1 and p2:
                        spread = abs(p1 - p2) / min(p1, p2) * 100
                        spread_data.append({
                            "Crypto": symbol,
                            "Exchange 1": ex1,
                            "Exchange 2": ex2,
                            "Price 1": p1,
                            "Price 2": p2,
                            "Spread (%)": round(spread, 4)
                        })
    return pd.DataFrame(spread_data)

# Streamlit UI
st.title("Crypto Arbitrage Exchange-to-Exchange Spreads (Top 20 Cryptos)")
while True:
    prices = fetch_all_prices()
    df_spreads = calculate_spreads(prices)
    st.dataframe(df_spreads)
    time.sleep(30)  # refresh every 30 seconds
