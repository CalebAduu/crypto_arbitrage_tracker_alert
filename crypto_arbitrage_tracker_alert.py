import streamlit as st
import requests
import pandas as pd
from itertools import combinations

# ----------------- CONFIG -----------------
TOP_N_CRYPTOS = 20
SPREAD_THRESHOLD = 1.0  # percent

EXCHANGES = [
    "MEXC", "LBank", "Bybit", "Gateio", "CoinEx",
    "XT", "Bitget", "KuCoin", "Binance", "HTX",
    "BingX", "BitMart"
]

# Placeholder URLs for public futures endpoints (replace with real ones)
EXCHANGE_PUBLIC_URLS = {
    "MEXC": "https://www.mexc.com/api/v3/futures/ticker/24hr?symbol={symbol}USDT",
    "LBank": "https://api.lbkex.com/v2/futures/tickers/{symbol}USDT",
    "Bybit": "https://api.bybit.com/v2/public/tickers?symbol={symbol}USDT",
    "Gateio": "https://api.gateio.ws/api/v4/futures/usdt/tickers?contract={symbol}_USDT",
    "CoinEx": "https://api.coinex.com/v1/futures/ticker?symbol={symbol}USDT",
    "XT": "https://api.xt.com/futures/public/ticker?symbol={symbol}USDT",
    "Bitget": "https://api.bitget.com/api/mix/v1/market/ticker?symbol={symbol}USDT",
    "KuCoin": "https://api.kucoin.com/api/v1/contracts/active?symbol={symbol}-USDT",
    "Binance": "https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}USDT",
    "HTX": "https://api.huobi.pro/market/detail/merged?symbol={symbol}USDT",
    "BingX": "https://api.bingx.com/api/v1/futures/ticker?symbol={symbol}USDT",
    "BitMart": "https://api.bitmart.com/contract/v1/ticker?symbol={symbol}USDT",
}

# ----------------- HELPER FUNCTIONS -----------------
def fetch_price(exchange, symbol):
    try:
        url = EXCHANGE_PUBLIC_URLS[exchange].format(symbol=symbol)
        r = requests.get(url, timeout=5)
        data = r.json()
        # Default fallback
        price = None

        if exchange == "Binance":
            price = float(data['price']) if 'price' in data else None
        elif exchange == "Bybit":
            price = float(data['last_price']) if 'last_price' in data else None
        elif exchange == "Bitget":
            price = float(data['last']) if 'last' in data else None
        elif exchange in ["MEXC", "CoinEx", "XT", "BitMart", "LBank", "HTX", "BingX"]:
            price = float(data.get('last', 0))
        elif exchange == "KuCoin":
            price = float(data['data']['last'] if 'data' in data else 0)
        elif exchange == "Gateio":
            price = float(data[0]['last'] if isinstance(data, list) and len(data) > 0 else 0)

        if price == 0:
            price = None
        return price
    except:
        return None

# ----------------- MAIN APP -----------------
st.set_page_config(page_title="Crypto Futures Spread Tracker", layout="wide")
st.title("Crypto Futures Spread Tracker")

# Top 20 cryptos
TOP_CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL", "BNB", "ADA", "XRP", "DOGE", "DOT",
                      "AVAX", "MATIC", "SHIB", "LTC", "TRX", "ATOM", "LINK",
                      "ETC", "XMR", "ALGO", "FIL", "VET"][:TOP_N_CRYPTOS]

all_data = []

for symbol in TOP_CRYPTO_SYMBOLS:
    row = {"Crypto": symbol}
    prices = {}
    for ex in EXCHANGES:
        price = fetch_price(ex, symbol)
        row[ex] = price
        prices[ex] = price

    # Calculate spreads for all exchange pairs
    for ex1, ex2 in combinations(EXCHANGES, 2):
        p1 = prices.get(ex1)
        p2 = prices.get(ex2)
        if p1 is not None and p2 is not None:
            spread = abs(p1 - p2) / min(p1, p2) * 100
            row[f"{ex1}-{ex2} Spread %"] = round(spread, 2)
        else:
            row[f"{ex1}-{ex2} Spread %"] = None

    all_data.append(row)

# Show DataFrame in Streamlit
df = pd.DataFrame(all_data)
st.data
