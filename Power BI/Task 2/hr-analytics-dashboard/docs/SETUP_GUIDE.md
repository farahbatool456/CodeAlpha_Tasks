# Setup Guide

Step-by-step instructions to get the HR Analytics Dashboard running in Power BI Desktop.

---

## Prerequisites

| Requirement | Version | Download |
|-------------|---------|----------|
| Power BI Desktop | 2.120 or later | [Download](https://powerbi.microsoft.com/desktop/) |
| Python (optional) | 3.9+ | [Download](https://python.org) |
| Git | Any | [Download](https://git-scm.com) |

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/hr-analytics-dashboard.git
cd hr-analytics-dashboard
```

---

## Step 2 — Generate Sample Data (optional)

If you want fresh synthetic data, run:

```bash
# Install dependencies
pip install pandas numpy faker prophet

# Generate all data files
python src/generate_sample_data.py --employees 400 --years 3
```

This creates 6 CSV files in the `/data` folder. Skip this step if you plan to connect real data directly.

---

## Step 3 — Open in Power BI Desktop

1. Open **Power BI Desktop**
2. Go to **File → Open Report**
3. Select `HR_Analytics_Dashboard.pbix`
4. If prompted about data source credentials: click **Edit Credentials**

---

## Step 4 — Connect Data Sources

### Option A: Use sample CSV files (default)

1. In Power BI Desktop, click **Home → Transform Data**
2. In Power Query Editor, select any query (e.g., `Employees`)
3. Click **Home → Data Source Settings**
4. For each source, click **Change Source** and point to the absolute path of your `/data` folder
5. Click **Close & Apply**
6. Click **Refresh** on the Home ribbon

### Option B: Connect to your HRIS / ATS

Supported data sources that map to the same schema:

| System | Connection Type | Notes |
|--------|----------------|-------|
| Workday | REST API / CSV Export | Export Active Workers report |
| BambooHR | API Connector | Use Employee Directory endpoint |
| ADP | CSV Export | Map field names to match schema |
| SAP SuccessFactors | OData Feed | Configure in Power BI connector |
| Greenhouse (ATS) | CSV Export | Export "All Applications" report |
| Lever (ATS) | CSV Export | Export from Analytics tab |
| Excel / SharePoint | Excel connector | Enable SharePoint connector |

To switch the data source:
1. **Transform Data → Advanced Editor** (for any query)
2. Replace the `Source` line with your connector
3. Map column names to match the Data Dictionary

---

## Step 5 — Configure Relationships

Verify these relationships exist in **Model View** (drag-and-drop if missing):

| From | Column | To | Column | Type |
|------|--------|----|--------|------|
| Employees | HireDate | Date | Date | Many-to-One ✱→1 |
| Exits | TerminationDate | Date | Date | Many-to-One ✱→1 |
| Recruitment | RequisitionDate | Date | Date | Many-to-One ✱→1 |
| Survey | SurveyDate | Date | Date | Many-to-One ✱→1 |
| Performance | EmployeeID | Employees | EmployeeID | Many-to-One ✱→1 |
| Survey | EmployeeID | Employees | EmployeeID | Many-to-One ✱→1 |
| Exits | EmployeeID | Employees | EmployeeID | Many-to-One ✱→1 |

> **Important:** Set `Date[Date]` as the date table:  
> Right-click `Date` table → **Mark as date table** → select the `Date` column.

---

## Step 6 — Import DAX Measures

All measures are pre-built in the `.pbix` file. If rebuilding from scratch:

1. Open **Modeling → New Measure**
2. Paste measures from [`docs/DAX_MEASURES.md`](DAX_MEASURES.md)
3. Assign each measure to the appropriate table in the **Properties** pane

---

## Step 7 — Validate Data

Run the validation script before each data refresh:

```bash
python src/data_validation.py
```

Expected output:
```
── employees.csv
  ✓  Loaded 400 rows × 12 columns
  ✓  All required columns present
  ✓  'EmployeeID' is unique
  ✓  'HireDate' dates parse correctly
  ...
✅  Validation PASSED — data is ready for Power BI.
```

---

## Step 8 — Publish to Power BI Service (optional)

1. Click **Home → Publish**
2. Select your target workspace
3. Once published, go to [app.powerbi.com](https://app.powerbi.com)
4. Navigate to your workspace → find the dataset
5. Click **…  → Settings → Scheduled Refresh**
6. Configure refresh frequency (daily recommended)

### Setting Up Row-Level Security (RLS)

To restrict managers to viewing only their own department's data:

1. **Modeling → Manage Roles → New Role** → name it `DepartmentManager`
2. Add filter to `Employees` table:
   ```dax
   [Department] = LOOKUPVALUE(Employees[Department], Employees[EmployeeID], USERPRINCIPALNAME())
   ```
3. In Power BI Service: **Dataset → Security** → assign users to roles

---

## Step 9 — Configure What-If Parameters

The Forecast page uses Power BI What-If parameters:

1. Go to **Modeling → New Parameter**
2. Create these parameters:

| Parameter | Min | Max | Default | Increment |
|-----------|-----|-----|---------|-----------|
| Attrition Assumption % | 5 | 35 | 14 | 1 |
| Growth Target % | 0 | 30 | 8 | 1 |
| Forecast Periods | 3 | 24 | 12 | 3 |

3. Reference these parameters in the forecast measures:
```dax
Required Hires (What-If) =
VAR AttritionRate = 'Attrition Assumption %'[Attrition Assumption % Value] / 100
VAR GrowthRate = 'Growth Target %'[Growth Target % Value] / 100
...
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Cannot find file" error | Update data source paths in Transform Data → Data Source Settings |
| Blank visuals after refresh | Check that `Date` table is marked as a date table |
| Relationship errors | Verify all relationships in Model View match the table in Step 5 |
| Python visuals not loading | Enable Python visuals: File → Options → Security → enable Python visuals |
| Slow refresh | Reduce date table range; disable auto date/time in Options |
| RLS not working | Check user email matches USERPRINCIPALNAME() format in Power BI Service |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01 | Initial release |
| 1.1.0 | 2025-03 | Added predictive forecast page |
| 1.2.0 | 2025-05 | Added RLS, diversity metrics, 9-box grid |
