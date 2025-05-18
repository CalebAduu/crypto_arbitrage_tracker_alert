# 📌 Crypto Arbitrage Tracker Alert

## Project Description

**`arbitrage_tracker_alert.py`** is a terminal-based Python application that retrieves real-time cryptocurrency prices from **Binance**, **Coinbase**, and **Kraken**. It identifies **arbitrage opportunities** and highlights price discrepancies between exchanges.

**Technologies:** Python, REST API, JSON parsing, CLI formatting

---

## Features

- 📡 Live tracking of top 50 cryptocurrencies
- 🧠 Detects arbitrage opportunities between exchanges (>1%)
- ⚠️ Flags suspicious spreads (>50%) as potential data errors
- 🎛️ Dynamic table updates in terminal
- 🔄 Automatic refresh per 10-crypto batch
- 🔐 Full exception handling and data validation

---

## Requirements

- 🐍 **Python 3.6+**

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python crypto_arbitrage_tracker_alert.py
```

The program runs in the terminal, continuously updating price data and displaying `[ALERT]` or `[⚠️  POSSIBLE ERROR]` messages based on real-time spreads.

---

## 📄 License

MIT License — see [LICENSE](LICENSE).

You are permitted to:

1. Use the software for any purpose, including commercial;
2. Modify, copy, and distribute the source code freely;
3. Integrate it into your own products or systems, provided that original authorship and disclaimer remain intact;
4. **It is strictly prohibited to use this software for unethical, malicious, or illegal purposes**, including but not limited to market manipulation, unauthorized access, or exploitative behavior.

---

## ⚠️ Disclaimer

This software is intended **strictly for educational and research purposes**.

- All provided data is for informational use only and **not financial advice**;
- The creator **bears no responsibility** for losses or damages resulting from usage;
- Use it at **your own risk** and always verify independently.

---

## 🎁 Support

If you'd like to support future development and research:

★ **Bitcoin (BTC)**  
`1MorphXyhHpgmYSfvwUpWojphfLTjrNXc7`

★ **Monero (XMR)**  
`86VAmEogaZF5WDwR3SKtEC6HSEUh6JPA1gVGcny68XmSJ1pYBbGLmdzEB1ZzGModLBXkG3WbRv12mSKv4KnD8i9w7VTg2uu`

★ **Dash (DASH)**  
`XtNuNfgaEXFKhtfxAKuDkdysxUqaZm7TDX`

---

We also value early privacy coins such as **Bytecoin (BCN)**:

`bcnZNMyrDrweQgoKH6zpWaE2kW1VZRsX3aDEqnxBVEQfjNnPK6vvNMNRPA4S7YxfhsStzyJeP16woK6G7cRBydZm2TvLFB2eeR`

🙏 *Thank you for supporting independent research and ethical technology.*

---

Crafted with dedication to education, blockchain exploration, and ethical software engineering.  
*“I morph bits, not to break, but to understand.” — BitMorphX*
