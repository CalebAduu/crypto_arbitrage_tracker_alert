import requests
import time
import os
from datetime import datetime

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    yellow = "\033[93m"
    red = "\033[91m"
    turquoise = "\033[96m"
    reset = "\033[0m"
    date = datetime.utcnow().strftime("%Y-%m-%d")
    time_utc = datetime.utcnow().strftime("%H:%M UTC")
    print(yellow + "=" * 95)
    print("ARBITRAGE PRICE TRACKER | Monitor crypto exchange prices and spot opportunities in real-time!")
    print("=" * 95)
    print(red + "DISCLAIMER: This software is for informational purposes only. Use at your own risk.\n"
          "Crypto prices may differ between exchanges. Always verify before trading." + yellow)
    print("=" * 95)
    print(turquoise + f"DATE: {date} | TIME: {time_utc}" + yellow)
    print("=" * 95)
    print(f"{'Cryptocurrency':<18} | {'Exchange':<12} | {'Price (USD)':<15}")
    print("=" * 95 + reset)

def get_top_50_cryptos():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, params=params)
        return response.json()
    except:
        return []

def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url).json()
        return float(data['price']) if 'price' in data else None
    except:
        return None

def get_coinbase_price(symbol):
    try:
        url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
        data = requests.get(url).json()
        return float(data['data']['amount']) if 'data' in data else None
    except:
        return None

def get_kraken_price(symbol):
    try:
        special_cases = {"BTC": "XBT", "DOGE": "XDG", "USDT": "USDTZ"}
        kraken_symbol = special_cases.get(symbol, symbol)
        url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}USD"
        data = requests.get(url).json()
        if 'result' in data and len(data['result']) > 0:
            pair = list(data['result'].keys())[0]
            return float(data['result'][pair]['c'][0])
        return None
    except:
        return None

def detect_arbitrage(prices, name):
    values = [v for v in prices.values() if v is not None and 0.01 < v < 100000]
    if len(values) < 2:
        return
    min_price = min(values)
    max_price = max(values)
    diff = (max_price - min_price) / min_price

    if diff >= 0.5:
        print(f"\033[93m[⚠️  POSSIBLE ERROR] Check data for {name} | "
              f"Buy @ ${min_price:.2f}, Sell @ ${max_price:.2f} | Spread: {diff*100:.2f}%\033[0m")
    elif diff >= 0.01:
        print(f"\033[92m[ALERT] Arbitrage Opportunity: {name} | "
              f"Buy @ ${min_price:.2f}, Sell @ ${max_price:.2f} | Spread: {diff*100:.2f}%\033[0m")

def display_crypto(crypto):
    name = crypto['name']
    symbol = crypto['symbol'].upper()

    binance_price = get_binance_price(symbol)
    coinbase_price = get_coinbase_price(symbol)
    kraken_price = get_kraken_price(symbol)

    if not any([binance_price, coinbase_price, kraken_price]):
        return

    print(f"{name:<18}")
    if binance_price:
        print(f"{'':<18} | Binance     | {binance_price:<15.4f} USD")
    if coinbase_price:
        print(f"{'':<18} | Coinbase    | {coinbase_price:<15.4f} USD")
    if kraken_price:
        print(f"{'':<18} | Kraken      | {kraken_price:<15.4f} USD")

    detect_arbitrage({
        "Binance": binance_price,
        "Coinbase": coinbase_price,
        "Kraken": kraken_price
    }, name)
    print("-" * 95)
    time.sleep(0.66)

def main():
    cryptos = get_top_50_cryptos()
    total = len(cryptos)
    batch_size = 10

    while True:
        for i in range(0, total, batch_size):
            clear_terminal()
            display_header()
            for crypto in cryptos[i:i+batch_size]:
                display_crypto(crypto)
            time.sleep(2)

if __name__ == "__main__":
    main()
