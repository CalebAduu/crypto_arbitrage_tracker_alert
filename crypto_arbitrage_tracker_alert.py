import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Crypto Arbitrage Tracker", layout="wide")

# List of top 20 cryptos (symbol: name)
TOP_20_CRYPTOS = {
    "BTC": "Bitcoin", "ETH": "Ethereum", "BNB": "Binance Coin", "XRP": "XRP",
    "ADA": "Cardano", "SOL": "Solana", "DOGE": "Dogecoin", "DOT": "Polkadot",
    "MATIC": "Polygon", "LTC": "Litecoin", "BCH": "Bitcoin Cash", "LINK": "Chainlink",
    "ATOM": "Cosmos", "XLM": "Stellar", "VET": "VeChain", "FIL": "Filecoin",
    "TRX": "TRON", "EOS": "EOS", "AAVE": "Aave", "SHIB": "Shiba Inu"
}

# List of exchanges
EXCHANGES = [
    "MEXC", "LBank", "Bybit", "Gateio", "CoinEx", "XT",
    "Bitget", "KuCoin", "Binance", "HTX", "BingX", "BitMart"
]

# ------------------- EXCHANGE PRICE FUNCTIONS -------------------
def get_binance_price(symbol):
    try:
        data = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()
        return float(data['price'])
    except:
        return None

def get_kucoin_price(symbol):
    try:
        data = requests.get(f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT").json()
        if data['code'] == "200000":
            return float(data['data']['price'])
    except:
        return None

def get_gateio_price(symbol):
    try:
        data = requests.get(f"https://api.gateio.ws/api2/1/ticker/{symbol}_USDT").json()
        if 'last' in data:
            return float(data['last'])
    except:
        return None

def get_bitmart_price(symbol):
    try:
        data = requests.get(f"https://api-cloud.bitmart.com/spot/v1/ticker?symbol={symbol}_USDT").json()
        if data['code'] == 1000:
            return float(data['data']['tick']['last_price'])
    except:
        return None

# Placeholders for exchanges without public endpoints
def get_mexc_price(symbol): return None
def get_lbank_price(symbol): return None
def get_bybit_price(symbol): return None
def get_coinex_price(symbol): return None
def get_xt_price(symbol): return None
def get_bitget_price(symbol): return None
def get_htx_price(symbol): return None
def get_bingx_price(symbol): return None

# Map exchange to its function
EXCHANGE_FUNCS = {
    "Binance": get_binance_price,
    "KuCoin": get_kucoin_price,
    "Gateio": get_gateio_price,
    "BitMart": get_bitmart_price,
    "MEXC": get_mexc_price,
    "LBank": get_lbank_price,
    "Bybit": get_bybit_price,
    "CoinEx": get_coinex_price,
    "XT": get_xt_price,
    "Bitget": get_bitget_price,
    "HTX": get_htx_price,
    "BingX": get_bingx_price
}

# ------------------- FETCH PRICES -------------------
prices_data = []

for symbol, name in TOP_20_CRYPTOS.items():
    row = {"Crypto": name}
    for ex in EXCHANGES:
        price = EXCHANGE_FUNCS[ex](symbol)
        row[ex] = price
    prices_data.append(row)

df_prices = pd.DataFrame(prices_data)
st.subheader("Crypto Prices Across Exchanges")
st.dataframe(df_prices)

# ------------------- CALCULATE SPREADS -------------------
spread_rows = []
for idx, row in df_prices.iterrows():
    crypto = row['Crypto']
    for i, ex1 in enumerate(EXCHANGES):
        for j, ex2 in enumerate(EXCHANGES):
            if i >= j:  # avoid duplicates
                continue
            p1, p2 = row[ex1], row[ex2]
            if p1 is not None and p2 is not None:
                spread = abs(p1 - p2)
                spread_pct = spread / min(p1, p2) * 100
                spread_rows.append({
                    "Crypto": crypto,
                    "Exchange 1": ex1,
                    "Exchange 2": ex2,
                    "Price 1": p1,
                    "Price 2": p2,
                    "Spread ($)": round(spread, 2),
                    "Spread (%)": round(spread_pct, 2)
                })

df_spreads = pd.DataFrame(spread_rows)
st.subheader("Exchange-to-Exchange Spreads")
st.dataframe(df_spreads)
