# 📊 Financial Health Dashboard — Power BI

An interactive Power BI dashboard for SMEs to monitor financial health, analyze trends, and forecast performance. Covers income statements, balance sheets, cash flows, and budget tracking.

---

## What This Dashboard Does

| Feature | Details |
|---|---|
| **Income Statement** | Revenue, COGS, gross profit, EBITDA, net income with margin analysis |
| **Balance Sheet** | Assets, liabilities, equity — liquidity and leverage ratios |
| **Cash Flow** | Operating, investing, financing flows — free cash flow tracking |
| **Budget vs Actual** | Variance analysis with 6-month forecasting |
| **KPI Trends** | 15+ financial ratios tracked over time |
| **Health Score** | Composite 0–100 score across profitability, liquidity, efficiency, growth |

---

## Report Pages

```
Page 1 — Executive Summary      (top-line KPIs + health score)
Page 2 — Income Statement       (P&L detail + margin trends)
Page 3 — Balance Sheet          (asset/liability structure + ratios)
Page 4 — Cash Flow              (CFO/CFI/CFF + free cash flow)
Page 5 — Budget vs Forecast     (variance analysis + projections)
Page 6 — KPI Trends             (all ratios over time)
```

---

## Repository Structure

```
financial-health-dashboard/
│
├── data/
│   ├── income_statement.csv       # P&L data (2023–2024, monthly, 2 divisions)
│   ├── balance_sheet.csv          # Balance sheet (quarterly snapshots)
│   ├── cash_flow.csv              # Cash flow statement (quarterly)
│   ├── budget_vs_actual.csv       # Budget vs actual + 6-month forecast
│   └── kpi_metrics.csv            # Pre-calculated KPI ratios (quarterly)
│
├── dax/
│   └── all_measures.dax           # All DAX measures (9 sections, 60+ measures)
│
├── docs/
│   └── powerbi_setup_guide.md     # Step-by-step Power BI setup instructions
│
├── .github/
│   └── workflows/
│       └── validate_data.yml      # GitHub Action: validates CSV structure on push
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## Quick Start

### Requirements
- Power BI Desktop (free) — [Download here](https://powerbi.microsoft.com/desktop/)
- Windows 10/11

### Setup (15–20 minutes)

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/financial-health-dashboard.git
cd financial-health-dashboard
```

**2. Open Power BI Desktop**

**3. Import data**  
Get Data → Text/CSV → import all 5 files from `/data` folder

**4. Create the Date Table**  
Modeling → New Table → paste the DAX from `docs/powerbi_setup_guide.md` (Step 2)

**5. Set up relationships**  
Model view → connect all Date columns to DateTable (see setup guide Step 3)

**6. Load measures**  
Modeling → New Measure → paste each section from `dax/all_measures.dax`

**7. Build report pages**  
Follow the visual layout in `docs/powerbi_setup_guide.md` (Step 5)

Full instructions: [`docs/powerbi_setup_guide.md`](docs/powerbi_setup_guide.md)

---

## Using Your Own Data

The sample data covers a fictional SME with two divisions (North, South) across 2023–2024.

To replace with real data:
1. Keep **exact column names** in the CSV files
2. Replace rows with your actual figures
3. In Power BI → Transform Data → Refresh Preview
4. All visuals update automatically

For live connections: replace CSV sources with SQL Server, SharePoint Excel, or your accounting software's Power BI connector (QuickBooks, Xero, SAP, Oracle).

---

## DAX Measures Included

| Category | Count | Examples |
|---|---|---|
| Income Statement | 10 | Gross Margin %, Net Margin %, EBITDA Margin % |
| YoY Growth | 6 | Revenue YoY Growth, Net Income YoY Growth |
| Rolling/YTD | 6 | Revenue YTD, Revenue 12M Rolling |
| Balance Sheet | 12 | Current Ratio, Quick Ratio, D/E Ratio, ROA, ROE |
| Cash Flow | 10 | Free Cash Flow, FCF Margin %, CapEx % of Revenue |
| Budget vs Actual | 8 | Budget Variance %, Budget Attainment %, Status label |
| Profitability Trends | 4 | 3M rolling margins, trend direction flags |
| KPI Cards | 8 | Formatted card measures, Financial Health Score |
| Forecasting | 4 | MA3 forecast, year-end projection, run-rate |

---

## Sample Data Specs

- **Period:** Jan 2023 – Dec 2024 (24 months monthly, 8 quarters)
- **Divisions:** North, South
- **Revenue range:** $450K – $820K/month (North), $320K – $642K/month (South)
- **Net margins:** 12–16% (realistic SME range)
- **Budget data:** 2024 actual + 6-month 2025 forecast

All figures are fictional but constructed to show realistic financial patterns including seasonality, margin expansion, and working capital dynamics.

---

## License

MIT License — free to use, modify, and distribute. See [LICENSE](LICENSE).

---

## Contributing

Pull requests welcome. For major changes, open an issue first.

If you adapt this for a real organization and add features, consider contributing back:
- New DAX measures
- Additional data categories (headcount, segment data)
- Power Query M scripts for live data sources
