# Power BI Setup Guide — Financial Health Dashboard

## Step 1: Import Data

Open Power BI Desktop → **Get Data → Text/CSV**

Import in this order:
1. `data/income_statement.csv`
2. `data/balance_sheet.csv`
3. `data/cash_flow.csv`
4. `data/budget_vs_actual.csv`
5. `data/kpi_metrics.csv`

**For each file:**
- Click "Transform Data" and verify column types
- Set `Date` columns → Data Type: **Date**
- Set all monetary columns → Data Type: **Decimal Number**
- Set `Year` → Data Type: **Whole Number**
- Click **Close & Apply**

---

## Step 2: Build the Date Table (Required for Time Intelligence)

In Power BI Desktop → **Modeling → New Table**, paste:

```dax
DateTable = 
ADDCOLUMNS(
    CALENDAR(DATE(2023,1,1), DATE(2025,12,31)),
    "Year",         YEAR([Date]),
    "Quarter",      "Q" & QUARTER([Date]),
    "Month Number", MONTH([Date]),
    "Month Name",   FORMAT([Date], "MMMM"),
    "Month Short",  FORMAT([Date], "MMM"),
    "Year-Month",   FORMAT([Date], "YYYY-MM"),
    "Year-Quarter", FORMAT([Date], "YYYY") & "-Q" & QUARTER([Date]),
    "Week Number",  WEEKNUM([Date]),
    "Day of Week",  FORMAT([Date], "DDDD"),
    "Is Weekend",   IF(WEEKDAY([Date], 2) >= 6, TRUE, FALSE)
)
```

Mark as **Date Table**: Right-click DateTable → **Mark as date table** → select `Date` column.

---

## Step 3: Create Relationships

Go to **Model view** and create these relationships:

| From Table | From Column | To Table | To Column | Cardinality |
|---|---|---|---|---|
| income_statement | Date | DateTable | Date | Many to One |
| balance_sheet | Date | DateTable | Date | Many to One |
| cash_flow | Date | DateTable | Date | Many to One |
| budget_vs_actual | Date | DateTable | Date | Many to One |

**Cross-filter direction:** Single (default)  
**Active:** Yes for all

---

## Step 4: Load DAX Measures

Go to **Modeling → New Measure** and paste each measure from `dax/all_measures.dax`.

Alternatively, create a **Measures table** (recommended):

1. **Modeling → New Table**: `Measures = ROW("x", 1)`
2. Add all measures to this table
3. Hide the `x` column

---

## Step 5: Build Report Pages

### Page 1 — Executive Summary
| Visual | Fields | Purpose |
|---|---|---|
| Card (4x) | KPI Revenue, KPI Net Income, KPI Gross Margin, KPI Free Cash Flow | Top-line KPIs |
| Card | Financial Health Score, Health Score Label | Composite health score |
| Line Chart | Date → Revenue, Gross Profit, Net Income | Trend over time |
| Clustered Bar | Quarter → Revenue by Division | Division breakdown |
| KPI Visual | Revenue vs Revenue PY | YoY comparison |

### Page 2 — Income Statement
| Visual | Fields | Purpose |
|---|---|---|
| Matrix | Year/Quarter → Revenue, COGS, Gross Profit, OpEx, EBITDA, Net Income | Full P&L |
| Line + Clustered Column | Date → Revenue (bar), Gross Margin % / Net Margin % (lines) | Margin trends |
| Waterfall Chart | Revenue → COGS → Gross Profit → OpEx → Net Income | Profit bridge |
| Scatter Chart | Revenue vs Net Margin % | Profitability scatter |

### Page 3 — Balance Sheet
| Visual | Fields | Purpose |
|---|---|---|
| Stacked Bar | Period → Current Assets, Fixed Assets | Asset composition |
| Stacked Bar | Period → Current Liabilities, LT Liabilities, Equity | Capital structure |
| Line Chart | Period → Current Ratio, Quick Ratio | Liquidity trends |
| Gauge | Debt to Equity Ratio | Leverage indicator (max=2) |
| Card (3x) | Working Capital, Return on Assets %, Return on Equity % | Efficiency KPIs |

### Page 4 — Cash Flow
| Visual | Fields | Purpose |
|---|---|---|
| Clustered Bar | Period → CFO, CFI, CFF | Cash flow components |
| Line Chart | Period → Ending Cash Balance, Free Cash Flow | Cash position |
| Card (3x) | FCF Margin %, CapEx as % of Revenue, Cash Flow Coverage | FCF KPIs |
| Waterfall | CFO → CFI → CFF → Net Change | Cash bridge |

### Page 5 — Budget vs Forecast
| Visual | Fields | Purpose |
|---|---|---|
| Line Chart | Date → Budget Amount, Actual Amount, Forecast Amount | All three lines |
| Bar Chart | Month → Budget Variance | Variance by month |
| Card | Budget Variance %, Budget Attainment %, Budget vs Actual Status | Attainment KPIs |
| Table | Category, Budget, Actual, Variance, Variance % | Detail drill-down |

### Page 6 — KPI Trends
| Visual | Fields | Purpose |
|---|---|---|
| Line Chart | Period → Gross Margin %, Net Margin %, EBITDA Margin % | Margin evolution |
| Line Chart | Period → Current Ratio, Quick Ratio | Liquidity evolution |
| Line Chart | Period → Revenue YoY Growth, Net Income YoY Growth | Growth rates |
| Matrix | Period → all KPI metrics | Full KPI table |

---

## Step 6: Slicers (Add to All Pages)

Add these slicers to every page using the **Sync Slicers** feature:

- **Year** (Dropdown) → DateTable[Year]
- **Quarter** (Dropdown) → DateTable[Quarter]  
- **Division** (List) → income_statement[Division]
- **Date Range** (Between) → DateTable[Date]

Enable **Sync Slicers**: View → Sync Slicers → check all pages for each slicer.

---

## Step 7: Conditional Formatting

Apply to key visuals:

**Gross Margin %:**
- Rules: < 30% = Red, 30–40% = Yellow, > 40% = Green

**Net Margin %:**
- Rules: < 5% = Red, 5–10% = Yellow, > 10% = Green

**Current Ratio:**
- Rules: < 1.0 = Red, 1.0–1.5 = Yellow, > 1.5 = Green

**Budget Variance %:**
- Rules: < -10% = Red, -10% to 0% = Yellow, > 0% = Green

**Revenue YoY Growth:**
- Rules: < 0% = Red, 0–10% = Yellow, > 10% = Green

---

## Step 8: Publish

1. **File → Publish → Publish to Power BI**
2. Select your workspace
3. In Power BI Service → **Schedule Refresh** (if using live data source)
4. Share dashboard link with stakeholders

---

## Replacing Sample Data with Real Data

The CSV files in `/data` are structured to match a real SME's chart of accounts. To replace:

1. Keep the **exact same column names**
2. Replace rows with your organization's actual figures
3. In Power BI Desktop → **Transform Data → Refresh Preview**
4. All visuals and measures update automatically

For live data, replace CSV sources with:
- SQL Server / Azure SQL connection
- Excel file on SharePoint
- Accounting software API connector (QuickBooks, Xero, SAP)
