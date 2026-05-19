# 🧑‍💼 HR Analytics Dashboard

> An interactive Power BI report for analyzing and optimizing HR processes and workforce management — covering recruitment metrics, employee turnover, satisfaction analytics, performance tracking, and predictive hiring forecasts.

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Excel](https://img.shields.io/badge/Microsoft%20Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Dashboard Pages](#-dashboard-pages)
- [Key Metrics & KPIs](#-key-metrics--kpis)
- [Data Sources](#-data-sources)
- [Folder Structure](#-folder-structure)
- [Getting Started](#-getting-started)
- [DAX Measures Reference](#-dax-measures-reference)
- [Data Dictionary](#-data-dictionary)
- [Predictive Analytics](#-predictive-analytics)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

This Power BI project provides HR teams and executives with a **360° view of workforce health**. It transforms raw HR data into actionable intelligence across four key pillars:

| Pillar | Focus |
|--------|-------|
| 🎯 **Recruitment** | Time-to-hire, cost-per-hire, offer acceptance rates, sourcing channel ROI |
| 🔄 **Retention & Turnover** | Voluntary vs. involuntary attrition, flight-risk scoring, department-level churn |
| 😊 **Satisfaction & Engagement** | eNPS trends, survey sentiment, absenteeism patterns |
| 📈 **Performance & Forecasting** | Goal attainment, rating distributions, predictive headcount modeling |

---

## 📊 Dashboard Pages

### Page 1 — Executive Summary
High-level KPI cards, YoY comparisons, headcount waterfall, and attrition trend line.

### Page 2 — Recruitment Analytics
- **Funnel visualization**: Applications → Screened → Interviewed → Offered → Hired
- Time-to-fill by department and role level
- Sourcing channel effectiveness (cost per hire, quality of hire score)
- Diversity hiring metrics (gender, age band, ethnicity breakdown)
- Monthly hiring velocity vs. headcount target

### Page 3 — Turnover & Retention
- Rolling 12-month attrition rate (voluntary vs. involuntary)
- Tenure cohort survival analysis
- Department/manager-level turnover heatmap
- Exit reason categorization (Pareto chart)
- Regrettable vs. non-regrettable attrition split

### Page 4 — Employee Satisfaction & Engagement
- eNPS over time (Promoters / Passives / Detractors)
- Survey participation rate and pulse check scores
- Absenteeism rate by team and month
- Sentiment word cloud from open-text survey responses
- Correlation: satisfaction score vs. performance rating

### Page 5 — Performance Management
- Rating distribution bell curve
- Goal attainment % by department
- High-performer / low-performer segmentation matrix (9-box grid)
- Year-over-year performance trend per employee band

### Page 6 — Predictive Hiring Forecast *(AI-powered)*
- 6-month and 12-month headcount forecasting model
- Attrition-adjusted hiring requirement calculator
- Seasonal demand pattern overlay
- What-if scenario slicers (growth %, attrition assumption)

---

## 📐 Key Metrics & KPIs

| Metric | Definition |
|--------|-----------|
| **Headcount** | Total active employees at end of period |
| **Attrition Rate** | `Leavers / Avg Headcount × 100` |
| **Time to Fill** | Days from job requisition open to offer accepted |
| **Time to Hire** | Days from candidate application to offer accepted |
| **Cost per Hire** | `(Internal + External Recruiting Costs) / Total Hires` |
| **Offer Acceptance Rate** | `Offers Accepted / Offers Extended × 100` |
| **eNPS** | `% Promoters − % Detractors` (range: −100 to +100) |
| **Absenteeism Rate** | `Absent Days / Available Working Days × 100` |
| **Regrettable Attrition** | Turnover of high-performing employees rated 4+ |
| **Quality of Hire** | Average performance rating of new hires at 12-month mark |

---

## 🗃️ Data Sources

| File | Description | Refresh Frequency |
|------|-------------|-------------------|
| `data/employees.csv` | Master employee roster (anonymized) | Daily |
| `data/recruitment.csv` | Job requisitions and applicant tracking | Weekly |
| `data/performance_reviews.csv` | Annual/mid-year review scores | Quarterly |
| `data/satisfaction_survey.csv` | Pulse survey and annual eNPS results | Monthly |
| `data/exits.csv` | Exit interview data and termination reasons | As-needed |
| `data/date_table.csv` | Standard date dimension table | Static |

> ⚠️ **Note:** All sample data files in `/data` are synthetically generated for demonstration. Replace with your real HRIS export before publishing internally.

---

## 📁 Folder Structure

```
hr-analytics-dashboard/
│
├── 📊 HR_Analytics_Dashboard.pbix          # Main Power BI file
│
├── 📁 data/
│   ├── employees.csv                        # Employee master data
│   ├── recruitment.csv                      # Recruitment pipeline data
│   ├── performance_reviews.csv              # Performance ratings
│   ├── satisfaction_survey.csv              # Survey & eNPS data
│   ├── exits.csv                            # Exit interview records
│   └── date_table.csv                       # Date dimension
│
├── 📁 src/
│   ├── generate_sample_data.py              # Python script to regenerate sample data
│   ├── forecast_model.py                    # Predictive hiring forecast logic (Prophet)
│   └── data_validation.py                   # Pre-load data quality checks
│
├── 📁 docs/
│   ├── DATA_DICTIONARY.md                   # Full field definitions
│   ├── DAX_MEASURES.md                      # All DAX formulas documented
│   ├── SETUP_GUIDE.md                       # Step-by-step Power BI setup
│   └── SCREENSHOTS/                         # Dashboard preview images
│
├── 📁 assets/
│   └── icons/                               # Custom SVG icons used in report
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- [Power BI Desktop](https://powerbi.microsoft.com/desktop/) (version 2.120+ recommended)
- Python 3.9+ (optional — for data generation and forecasting scripts)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/hr-analytics-dashboard.git
cd hr-analytics-dashboard

# 2. (Optional) Install Python dependencies for data scripts
pip install -r requirements.txt

# 3. (Optional) Regenerate sample data
python src/generate_sample_data.py

# 4. Open the Power BI report
# Double-click HR_Analytics_Dashboard.pbix
# OR open Power BI Desktop → File → Open → select the .pbix file
```

### Connecting to Your Real Data

1. Open the `.pbix` file in Power BI Desktop
2. Go to **Home → Transform Data → Data Source Settings**
3. Replace CSV file paths with your HRIS/ATS export paths (or connect to SQL/SharePoint/API)
4. Click **Refresh** — all visuals will update automatically
5. Publish to Power BI Service: **Home → Publish → Select Workspace**

---

## 📐 DAX Measures Reference

See [`docs/DAX_MEASURES.md`](docs/DAX_MEASURES.md) for the full library. Key measures:

```dax
-- Attrition Rate (Rolling 12-Month)
Attrition Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(Exits), DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -12, MONTH)),
    CALCULATE(AVERAGE(Headcount[HeadcountValue]), DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -12, MONTH)),
    0
) * 100

-- Time to Fill (Average)
Avg Time to Fill = 
AVERAGEX(
    FILTER(Recruitment, Recruitment[Status] = "Hired"),
    DATEDIFF(Recruitment[RequisitionDate], Recruitment[OfferAcceptedDate], DAY)
)

-- eNPS Score
eNPS = 
VAR Promoters = CALCULATE(COUNTROWS(Survey), Survey[Score] >= 9) / COUNTROWS(Survey) * 100
VAR Detractors = CALCULATE(COUNTROWS(Survey), Survey[Score] <= 6) / COUNTROWS(Survey) * 100
RETURN Promoters - Detractors

-- Regrettable Attrition Rate
Regrettable Attrition Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(Exits), Exits[IsRegrettable] = TRUE()),
    COUNTROWS(Exits),
    0
) * 100
```

---

## 📖 Data Dictionary

See [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) for full field definitions. Summary:

### `employees.csv`
| Field | Type | Description |
|-------|------|-------------|
| EmployeeID | String | Unique identifier (anonymized) |
| Department | String | Business unit / department name |
| JobLevel | String | IC1–IC5, M1–M4, D1–D2 |
| HireDate | Date | Date of joining |
| Gender | String | Gender identity (Self-reported) |
| AgeGroup | String | 18-25, 26-35, 36-45, 46-55, 55+ |
| IsActive | Boolean | Currently employed flag |
| ManagerID | String | Direct manager's EmployeeID |

### `recruitment.csv`
| Field | Type | Description |
|-------|------|-------------|
| ReqID | String | Requisition identifier |
| Department | String | Hiring department |
| RequisitionDate | Date | Date role was opened |
| OfferAcceptedDate | Date | Date offer was accepted |
| SourceChannel | String | LinkedIn / Referral / Job Board / Agency / Direct |
| HiringCost | Decimal | Total cost for this hire (USD) |
| CandidateStage | String | Application / Screen / Interview / Offer / Hired / Rejected |

---

## 🔮 Predictive Analytics

The **Forecast Page** uses a hybrid model:

1. **Historical trend decomposition** — Power BI's built-in forecasting (exponential smoothing) for headcount projections
2. **Python / Facebook Prophet integration** — `src/forecast_model.py` outputs a 12-month hiring demand CSV that feeds the what-if scenario page
3. **Attrition-adjusted headcount formula:**

```
Required Hires (next period) = 
  Target Headcount 
  + Expected Attrition (historical rate × current headcount)
  - Internal Transfers IN
  + Internal Transfers OUT
```

### Running the Forecast Script

```bash
python src/forecast_model.py \
  --input data/employees.csv \
  --attrition-rate 0.14 \
  --growth-target 0.08 \
  --periods 12 \
  --output data/forecast_output.csv
```

---

## 📸 Screenshots

| Page | Preview |
|------|---------|
| Executive Summary | *(Add screenshot after publishing)* |
| Recruitment Funnel | *(Add screenshot after publishing)* |
| Turnover Heatmap | *(Add screenshot after publishing)* |
| Predictive Forecast | *(Add screenshot after publishing)* |

> Add screenshots to `docs/SCREENSHOTS/` and update the table above.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/add-diversity-metrics`
3. Commit your changes: `git commit -m "feat: add diversity hiring funnel breakdown"`
4. Push and open a Pull Request

Please follow the [Conventional Commits](https://www.conventionalcommits.org/) standard.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- Sample data generated using [Faker](https://faker.readthedocs.io/) (Python)
- Forecasting powered by [Facebook Prophet](https://facebook.github.io/prophet/)
- Icons from [Feather Icons](https://feathericons.com/)
- Dashboard design inspired by best practices from the Power BI community

---

*Built for HR professionals who believe decisions should be driven by data, not gut instinct.*
