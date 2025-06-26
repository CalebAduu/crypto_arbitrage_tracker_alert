<p align="center">
  <img src="assets/banner.png" alt="crypto_arbitrage_tracker_alert banner" width="100%" />
</p>

# 📌 CRYPTO ARBITRAGE TRACKER ALERT

**crypto_arbitrage_tracker_alert** is a terminal-based Python application that retrieves real-time cryptocurrency prices from **Binance**, **Coinbase**, and **Kraken**. It identifies **arbitrage opportunities** and highlights price discrepancies between exchanges.

---

## ⚙️ Features

- 📡 Live tracking of top 50 cryptocurrencies  
- 🧠 Detects arbitrage opportunities between exchanges (>1%)  
- ⚠️ Flags suspicious spreads (>50%) as potential data errors  
- 🎛️ Dynamic table updates in terminal  
- 🔄 Automatic refresh per 10-crypto batch  
- 🔐 Full exception handling and data validation

---

## 📁 File Overview

- `crypto_arbitrage_tracker_alert.py` – Main price tracking and arbitrage detection script  
- `crypto_arbitrage_tracker_alert.bat` – Windows launcher for quick use  
- `.vscode/`  
  - `settings.json` – Editor preferences  
  - `launch.json` – Debugging configuration  
  - `tasks.json` – Task runner integration  
  - `extensions.json` – Recommended VS Code extensions  
- `assets/`  
  - `banner.png` – Project banner  
- `README.md` – This documentation  
- `LICENSE` – Apache 2.0 License  
- `NOTICE` – Attribution and notices  
- `ETHICS.md` – Responsible use notice  
- `requirements.txt` – Python dependencies  
- `RELEASE_v1.0.0.md` – Initial release notes  
- `RELEASE_v2.0.0.md` – Latest release notes

---

## 🛠️ Dependencies

```
requests
```

Install with:

```bash
pip install -r requirements.txt
```

> Python 3.6+ is required.

---

## 🚀 Usage

### Option 1 – via Python:

```bash
python crypto_arbitrage_tracker_alert.py
```

### Option 2 – via `.bat` launcher (Windows):

```cmd
crypto_arbitrage_tracker_alert.bat
```

The program runs in the terminal, continuously updating price data and displaying `[ALERT]` or `[⚠️  POSSIBLE ERROR]` messages based on real-time spreads.

---

## 📂 Project Structure

```text
crypto_arbitrage_tracker_alert/
├── assets/
│   └── banner.png
├── .vscode/
│   ├── settings.json
│   ├── launch.json
│   ├── tasks.json
│   └── extensions.json
├── crypto_arbitrage_tracker_alert.py
├── crypto_arbitrage_tracker_alert.bat
├── LICENSE
├── NOTICE
├── ETHICS.md
├── README.md
├── requirements.txt
├── RELEASE_v1.0.0.md
└── RELEASE_v2.0.0.md
```

---

## ⚠️ DISCLAIMER

This software is intended **strictly for educational and research purposes**.

- All provided data is for informational use only and **not financial advice**  
- The creator **bears no responsibility** for losses or damages resulting from usage  
- Use it at **your own risk** and always verify independently

> **Use responsibly. Learn ethically. Contribute honestly.**

---

## ⚖️ Ethical Use

This tool is created strictly for **research and educational purposes**.  
See [ETHICS](./ETHICS.md) for the full statement.

---

## 📜 License

Licensed under the [Apache 2.0 License](./LICENSE)

---

## 📣 NOTICE

See [`NOTICE`](./NOTICE) for important information about attribution, DMCA protection, and reuse permissions.

---

## 🍱 Support

★ **Bitcoin (BTC)**  
`1MorphXyhHpgmYSfvwUpWojphfLTjrNXc7`

★ **Monero (XMR)**  
`86VAmEogaZF5WDwR3SKtEC6HSEUh6JPA1gVGcny68XmSJ1pYBbGLmdzEB1ZzGModLBXkG3WbRv12mSKv4KnD8i9w7VTg2uu`

★ **Dash (DASH)**  
`XtNuNfgaEXFKhtfxAKuDkdysxUqaZm7TDX`

**We also value early privacy coins such as:**  
★ **Bytecoin (BCN)**  
`bcnZNMyrDrweQgoKH6zpWaE2kW1VZRsX3aDEqnxBVEQfjNnPK6vvNMNRPA4S7YxfhsStzyJeP16woK6G7cRBydZm2TvLFB2eeR`

🙏 *Thank you for supporting independent research and ethical technology.*

---

## 👤 Author & Contact

🔗 GitHub: https://github.com/BitMorphX  
✉️ Email: BitMorphX@proton.me  
💬 Telegram: https://t.me/BitMorphX

> _“I morph bits, not to break, but to understand.”_  
> — **BitMorphX**

---

© BitMorphX – All rights reserved.
