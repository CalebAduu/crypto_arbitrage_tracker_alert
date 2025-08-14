import streamlit as st
import requests
from telegram import Bot
import time

# ------------------------
# Telegram Configuration
# ------------------------
TELEGRAM_BOT_TOKEN = "8211027473:AAEwuL0nkumeqqyE8yaH167MtSsbUK6JJfM"
TELEGRAM_CHAT_ID = "1888691302"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        st.error(f"Error sending Telegram message: {e}")

# ------------------------
# Exchange API URLs
# ------------------------
EXCHANGE_API_URLS = {
    "Binance": "https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT",
    "KuCoin": "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT",
    "Bybit": "https://api.bybit.com/v2/public/tickers?symbol={symbol}USDT",
    "Gate.io": "https://api.gateio.ws/api2/1/ticker/{symbol}_USDT",
    "CoinEx": "https://api.coinex.com/v1/market/ticker?market={symbol}_USDT",
    "XT": "https://api.xt.com/data/v1/ticker?symbol={symbol}_USDT",
    "Bitget": "https://api.bitget.com/api/spot/v1/market/ticker?symbol={symbol}_USDT",
    "HTX": "https://api.htx.com/api/v1/market/detail?symbol={symbol}_USDT",
    "BingX": "https://api.bingx.com/api/v1/market/ticker?symbol={symbol}_USDT",
    "BitMart": "https://api-cloud.bitmart.com/spot/v1/ticker?symbol={symbol}_USDT"
}

# ------------------------
# Top 20 Cryptos
# ------------------------
TOP_20_CRYPTOS = ["BTC","ETH","BNB","XRP","ADA","DOGE","USDT","DOT","UNI","LTC",
                  "BCH","LINK","XLM","VET","TRX","EOS","FIL","AAVE","ATOM","SOL"]

# ------------------------
# Fetch Price Function
# ------------------------
def fetch_price(exchange, symbol):
    try:
        url = EXCHANGE_API_URLS.get(exchange)
        if not url:
            return None
        response = requests.get(url.format(symbol=symbol), timeout=5)
        if response.status_code != 200:
            return None
        data = response.json()
        # Parsing price depending on exchange
        if exchange == "Binance":
            return float(data['price'])
        elif exchange == "KuCoin":
            return float(data['data']['price'])
        elif exchange == "Bybit":
            return float(data['result'][0]['last_price'])
        elif exchange == "Gate.io":
            return float(data['last'])
        elif exchange == "CoinEx":
            return float(data['data']['ticker']['last'])
        elif exchange == "XT":
            return float(data['ticker']['last'])
        elif exchange == "Bitget":
            return float(data['data']['last'])
        elif exchange == "HTX":
            return float(data['data']['close'])
        elif exchange == "BingX":
            return float(data['data']['last'])
        elif exchange == "BitMart":
            return float(data['data']['tickers'][0]['last_price'])
        else:
            return None
    except:
        return None

# ------------------------
# Streamlit App
# ------------------------
st.set_page_config(page_title="Crypto Arbitrage Monitor", layout="wide")
st.title("Crypto Arbitrage Monitor")
st.write("Monitoring top 20 cryptocurrencies across multiple exchanges.")

# Display refresh interval
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 10, 300, 60)

# Main loop
if 'last_run' not in st.session_state:
    st.session_state.last_run = 0

if time.time() - st.session_state.last_run > refresh_interval:
    st.session_state.last_run = time.time()
    table_data = []

    for crypto in TOP_20_CRYPTOS:
        row = {"Crypto": crypto}
        prices = {}
        for exchange in EXCHANGE_API_URLS.keys():
            price = fetch_price(exchange, crypto)
            if price:
                prices[exchange] = price
                row[exchange] = price
            else:
                row[exchange] = None
        if prices:
            min_price = min(prices.values())
            max_price = max(prices.values())
            spread = (max_price - min_price) / min_price * 100
            row["Spread %"] = round(spread, 2)

            if spread >= 1:
                msg = f"🚨 Arbitrage Opportunity: {crypto}\nBuy: ${min_price:.2f}\nSell: ${max_price:.2f}\nSpread: {spread:.2f}%"
                send_telegram_message(msg)
        else:
            row["Spread %"] = None

        table_data.append(row)

    st.table(table_data)

