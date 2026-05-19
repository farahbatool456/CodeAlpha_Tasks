"""
Stock Portfolio Tracker
=======================
Enter stock names and quantities to calculate your total investment value.
Prices are hardcoded for demonstration purposes.

Concepts used: dictionary, input/output, basic arithmetic, file handling
"""

import csv
import os
from datetime import datetime

# ── Hardcoded stock price dictionary (USD) ──────────────────────────────────
STOCK_PRICES = {
    "AAPL":  180,   # Apple
    "TSLA":  250,   # Tesla
    "GOOGL": 140,   # Alphabet (Google)
    "MSFT":  380,   # Microsoft
    "AMZN":  185,   # Amazon
    "META":  490,   # Meta
    "NVDA":  875,   # NVIDIA
    "NFLX":  620,   # Netflix
    "AMD":   165,   # AMD
    "INTC":   35,   # Intel
}


def show_available_stocks():
    """Print all stocks with their current prices."""
    print("\n" + "=" * 40)
    print("  Available Stocks")
    print("=" * 40)
    print(f"  {'Ticker':<8} {'Company':<20} {'Price (USD)':>10}")
    print("-" * 40)

    company_names = {
        "AAPL": "Apple", "TSLA": "Tesla", "GOOGL": "Alphabet",
        "MSFT": "Microsoft", "AMZN": "Amazon", "META": "Meta",
        "NVDA": "NVIDIA", "NFLX": "Netflix", "AMD": "AMD", "INTC": "Intel",
    }

    for ticker, price in STOCK_PRICES.items():
        name = company_names.get(ticker, "")
        print(f"  {ticker:<8} {name:<20} ${price:>9,}")
    print("=" * 40 + "\n")


def get_portfolio_from_user():
    """
    Prompt the user to enter stock tickers and quantities.
    Returns a dict like {"AAPL": 10, "TSLA": 5}.
    """
    portfolio = {}

    print("Enter your stocks one at a time.")
    print("Type 'done' when finished, or 'list' to see available stocks.\n")

    while True:
        ticker = input("Stock ticker (e.g. AAPL): ").strip().upper()

        if ticker == "DONE":
            break

        if ticker == "LIST":
            show_available_stocks()
            continue

        if ticker == "":
            print("  ⚠  Ticker cannot be empty. Try again.\n")
            continue

        if ticker not in STOCK_PRICES:
            print(f"  ⚠  '{ticker}' not found. Type 'list' to see available stocks.\n")
            continue

        # Get quantity
        qty_input = input(f"  Quantity of {ticker}: ").strip()
        try:
            qty = int(qty_input)
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("  ⚠  Please enter a positive whole number for quantity.\n")
            continue

        # Add to portfolio (accumulate if ticker entered twice)
        portfolio[ticker] = portfolio.get(ticker, 0) + qty
        print(f"  ✓  Added {qty} × {ticker}\n")

    return portfolio


def calculate_portfolio(portfolio):
    """
    Given a portfolio dict, calculate per-stock value and grand total.
    Returns a list of row dicts and the total.
    """
    rows = []
    total = 0

    for ticker, qty in portfolio.items():
        price = STOCK_PRICES[ticker]
        value = price * qty
        total += value
        rows.append({
            "ticker":    ticker,
            "quantity":  qty,
            "price_usd": price,
            "value_usd": value,
        })

    return rows, total


def display_results(rows, total):
    """Print a formatted portfolio summary to the terminal."""
    print("\n" + "=" * 55)
    print("  PORTFOLIO SUMMARY")
    print("=" * 55)
    print(f"  {'Ticker':<8} {'Qty':>6}  {'Price':>10}  {'Value':>12}")
    print("-" * 55)

    for row in rows:
        print(
            f"  {row['ticker']:<8}"
            f" {row['quantity']:>6}"
            f"  ${row['price_usd']:>9,}"
            f"  ${row['value_usd']:>11,}"
        )

    print("-" * 55)
    print(f"  {'TOTAL':>27}  ${total:>11,}")
    print("=" * 55 + "\n")


def save_as_txt(rows, total, filename):
    """Save portfolio summary to a .txt file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "w") as f:
        f.write("STOCK PORTFOLIO TRACKER\n")
        f.write(f"Generated: {timestamp}\n")
        f.write("=" * 55 + "\n")
        f.write(f"{'Ticker':<8} {'Qty':>6}  {'Price':>10}  {'Value':>12}\n")
        f.write("-" * 55 + "\n")

        for row in rows:
            f.write(
                f"{row['ticker']:<8}"
                f" {row['quantity']:>6}"
                f"  ${row['price_usd']:>9,}"
                f"  ${row['value_usd']:>11,}\n"
            )

        f.write("-" * 55 + "\n")
        f.write(f"{'TOTAL':>27}  ${total:>11,}\n")
        f.write("=" * 55 + "\n")

    print(f"  ✓  Saved to {filename}")


def save_as_csv(rows, total, filename):
    """Save portfolio data to a .csv file."""
    with open(filename, "w", newline="") as f:
        fieldnames = ["ticker", "quantity", "price_usd", "value_usd"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

        # Append total row
        writer.writerow({
            "ticker":    "TOTAL",
            "quantity":  "",
            "price_usd": "",
            "value_usd": total,
        })

    print(f"  ✓  Saved to {filename}")


def ask_to_save(rows, total):
    """Prompt user to optionally save results."""
    print("Save results? Enter format or press Enter to skip.")
    choice = input("  Options: txt / csv / both / skip : ").strip().lower()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"portfolio_{timestamp}"

    if choice in ("txt", "both"):
        save_as_txt(rows, total, f"{base}.txt")

    if choice in ("csv", "both"):
        save_as_csv(rows, total, f"{base}.csv")

    if choice not in ("txt", "csv", "both"):
        print("  Skipped saving.")

    print()


def main():
    print("\n╔══════════════════════════════════════╗")
    print("║     STOCK PORTFOLIO TRACKER v1.0     ║")
    print("╚══════════════════════════════════════╝\n")

    show_available_stocks()

    while True:
        portfolio = get_portfolio_from_user()

        if not portfolio:
            print("  ⚠  No stocks entered. Please add at least one stock.\n")
            continue

        rows, total = calculate_portfolio(portfolio)
        display_results(rows, total)
        ask_to_save(rows, total)

        again = input("Track another portfolio? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            break
        print()

    print("\nGoodbye!\n")


if __name__ == "__main__":
    main()
