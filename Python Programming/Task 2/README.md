# 📈 Stock Portfolio Tracker

A beginner Python project that calculates the total value of a stock portfolio using hardcoded prices and user input.

---

## What It Does

- Shows a list of available stocks with their prices
- Lets the user enter stock tickers and quantities
- Calculates the value of each holding and the grand total
- Optionally saves the result as a `.txt` or `.csv` file

---

## Concepts Practiced

| Concept | Where Used |
|---|---|
| Dictionary | `STOCK_PRICES` lookup table |
| User Input / Output | `input()`, formatted `print()` |
| Basic Arithmetic | `price × quantity`, running total |
| File Handling | `.txt` write, `csv.DictWriter` |
| Functions | Code split into small, focused functions |
| Error Handling | Invalid ticker, non-integer quantity |

---

## Project Structure

```
stock_portfolio_tracker/
├── stock_tracker.py   ← main script (run this)
└── README.md
```

Output files (if saved) are created in the same folder where you run the script:

```
portfolio_20240519_143022.txt
portfolio_20240519_143022.csv
```

---

## Requirements

- Python 3.7 or higher
- No external libraries needed (uses only the standard library)

---

## How to Run

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/stock-portfolio-tracker.git
cd stock-portfolio-tracker
```

**2. Run the script**

```bash
python stock_tracker.py
```

---

## Sample Session

```
╔══════════════════════════════════════╗
║     STOCK PORTFOLIO TRACKER v1.0     ║
╚══════════════════════════════════════╝

========================================
  Available Stocks
========================================
  Ticker   Company              Price (USD)
----------------------------------------
  AAPL     Apple                     $180
  TSLA     Tesla                     $250
  GOOGL    Alphabet                  $140
  MSFT     Microsoft                 $380
  ...
========================================

Enter your stocks one at a time.
Type 'done' when finished, or 'list' to see available stocks.

Stock ticker (e.g. AAPL): AAPL
  Quantity of AAPL: 10
  ✓  Added 10 × AAPL

Stock ticker (e.g. AAPL): TSLA
  Quantity of TSLA: 5
  ✓  Added 5 × TSLA

Stock ticker (e.g. AAPL): done

=======================================================
  PORTFOLIO SUMMARY
=======================================================
  Ticker      Qty       Price         Value
-------------------------------------------------------
  AAPL         10        $180         $1,800
  TSLA          5        $250         $1,250
-------------------------------------------------------
                   TOTAL              $3,050
=======================================================

Save results? Enter format or press Enter to skip.
  Options: txt / csv / both / skip : csv
  ✓  Saved to portfolio_20240519_143022.csv
```

---

## Available Stocks

| Ticker | Company | Price (USD) |
|---|---|---|
| AAPL | Apple | $180 |
| TSLA | Tesla | $250 |
| GOOGL | Alphabet | $140 |
| MSFT | Microsoft | $380 |
| AMZN | Amazon | $185 |
| META | Meta | $490 |
| NVDA | NVIDIA | $875 |
| NFLX | Netflix | $620 |
| AMD | AMD | $165 |
| INTC | Intel | $35 |

> Prices are hardcoded for learning purposes. They do not reflect live market data.

---

## How to Extend This Project

Ideas if you want to keep building:

- Pull live prices using the `yfinance` library
- Add a `--watchlist` flag to track specific tickers
- Build a simple CLI menu with `argparse`
- Store portfolio history in a SQLite database
- Add percentage allocation per stock

---

## License

MIT License. Use freely for learning and personal projects.
