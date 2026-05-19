# Data Dictionary

Complete field definitions for all CSV data sources in the HR Analytics Dashboard.

---

## employees.csv

Master employee roster. One row per employee (active and inactive).

| Field | Type | Nullable | Description | Example Values |
|-------|------|----------|-------------|----------------|
| EmployeeID | String | No | Unique anonymized identifier | EMP0001, EMP0042 |
| Department | String | No | Business unit / team | Engineering, Sales, HR |
| JobLevel | String | No | Seniority level code | IC1–IC5 (individual contributors), M1–M3 (managers), D1 (director) |
| HireDate | Date (YYYY-MM-DD) | No | Date employee joined the company | 2022-03-14 |
| TerminationDate | Date (YYYY-MM-DD) | Yes | Date employee left (blank if still active) | 2024-01-31 |
| Gender | String | No | Self-reported gender identity | Male, Female, Non-binary, Prefer not to say |
| AgeGroup | String | No | Age band (self-reported or derived) | 18-25, 26-35, 36-45, 46-55, 55+ |
| IsActive | Boolean | No | TRUE if currently employed | TRUE, FALSE |
| ManagerID | String | Yes | EmployeeID of direct manager (blank for top-level) | EMP0015 |
| Location | String | Yes | City or office location | New York, Remote, London |
| EmploymentType | String | No | Employment classification | Full-time, Part-time, Contract |
| Salary | Decimal | No | Annual gross salary in USD | 85000, 120000 |

---

## recruitment.csv

Job requisition and applicant tracking data. One row per candidate application.

| Field | Type | Nullable | Description | Example Values |
|-------|------|----------|-------------|----------------|
| ReqID | String | No | Unique requisition identifier | REQ0001, REQ0123 |
| Department | String | No | Hiring department | Engineering, Marketing |
| JobLevel | String | No | Target level for the role | IC3, M1 |
| RequisitionDate | Date (YYYY-MM-DD) | No | Date role was formally opened | 2023-06-01 |
| OfferAcceptedDate | Date (YYYY-MM-DD) | Yes | Date offer was accepted by candidate (blank if not hired) | 2023-07-15 |
| TimeToFill_Days | Integer | Yes | Calendar days from RequisitionDate to OfferAcceptedDate | 28, 45 |
| SourceChannel | String | No | How the candidate was sourced | LinkedIn, Employee Referral, Job Board, Recruiting Agency, Direct / Career Page, University Recruiting |
| CandidateStage | String | No | Final pipeline stage reached | Application, Phone Screen, Technical Interview, Final Interview, Offer, Hired, Rejected |
| HiringCost_USD | Decimal | No | Total recruiting cost for this candidate/hire | 5200.00 |
| OfferExtended | Boolean | No | Whether an offer was made | TRUE, FALSE |
| OfferAccepted | Boolean | No | Whether the offer was accepted | TRUE, FALSE |
| DiversityHire | Boolean | No | Whether candidate is from an under-represented group (self-identified) | TRUE, FALSE |

---

## performance_reviews.csv

Employee performance review records. One row per review cycle per employee.

| Field | Type | Nullable | Description | Example Values |
|-------|------|----------|-------------|----------------|
| EmployeeID | String | No | References Employees[EmployeeID] | EMP0001 |
| ReviewYear | Integer | No | Calendar year of the review | 2023, 2024 |
| ReviewCycle | String | No | Whether annual or mid-year review | Annual, Mid-Year |
| PerformanceRating | Integer | No | Manager-assigned rating (1–5 scale) | 1=Needs Improvement, 2=Below Expectations, 3=Meets Expectations, 4=Exceeds Expectations, 5=Outstanding |
| GoalAttainmentPct | Decimal | Yes | % of goals achieved (0–120, >100 = exceeded targets) | 85.0, 102.5 |
| ManagerRating | Integer | Yes | Direct manager's assessment (1–5) | 4 |
| PeerRating | Integer | Yes | Aggregated peer review score (1–5) | 3 |
| IsHighPerformer | Boolean | No | TRUE if PerformanceRating >= 4 | TRUE, FALSE |
| IsLowPerformer | Boolean | No | TRUE if PerformanceRating <= 2 | TRUE, FALSE |

---

## satisfaction_survey.csv

Employee pulse surveys and annual engagement survey data. Multiple rows per employee.

| Field | Type | Nullable | Description | Example Values |
|-------|------|----------|-------------|----------------|
| EmployeeID | String | No | References Employees[EmployeeID] | EMP0042 |
| SurveyDate | Date (YYYY-MM-DD) | No | Date survey was completed | 2023-11-01 |
| eNPS_Score | Integer | No | Employee Net Promoter Score (0–10): "How likely are you to recommend this company as a place to work?" | 8 |
| eNPS_Category | String | No | Derived from eNPS_Score: 9-10 = Promoter, 7-8 = Passive, 0-6 = Detractor | Promoter, Passive, Detractor |
| EngagementScore | Decimal | Yes | Overall engagement rating (1.0–5.0) | 4.2 |
| ManagerSatisfaction | Decimal | Yes | Satisfaction with direct manager (1.0–5.0) | 4.5 |
| WorkLifeBalance | Decimal | Yes | Work-life balance rating (1.0–5.0) | 3.8 |
| CompensationSatisfaction | Decimal | Yes | Satisfaction with compensation & benefits (1.0–5.0) | 3.3 |
| AbsenceDays | Integer | Yes | Number of unplanned absence days in the period | 2, 5 |
| SurveyType | String | No | Type of survey | Annual Engagement, Pulse, Onboarding, Exit |

---

## exits.csv

Exit interview and offboarding records for terminated employees. One row per leaver.

| Field | Type | Nullable | Description | Example Values |
|-------|------|----------|-------------|----------------|
| EmployeeID | String | No | References Employees[EmployeeID] | EMP0015 |
| Department | String | No | Department at time of exit | Engineering |
| JobLevel | String | No | Level at time of exit | IC4 |
| HireDate | Date (YYYY-MM-DD) | No | Original hire date | 2021-09-01 |
| TerminationDate | Date (YYYY-MM-DD) | No | Last day of employment | 2024-02-28 |
| ExitType | String | No | Whether departure was voluntary or involuntary | Voluntary, Involuntary |
| ExitReason | String | No | Primary reason for leaving (from exit interview) | Better compensation elsewhere, Career growth opportunity, Work-life balance, Relocation, Manager relationship, Company culture, Role change, Personal reasons, Performance-based, Layoff / Restructuring |
| LastPerformanceRating | Integer | Yes | Most recent performance rating (1–5) | 4 |
| IsRegrettable | Boolean | No | TRUE if voluntary exit and LastPerformanceRating >= 4 | TRUE, FALSE |
| TenureDays | Integer | Yes | Days between HireDate and TerminationDate | 912 |
| ConductedExitInterview | Boolean | No | Whether a formal exit interview was completed | TRUE, FALSE |

---

## date_table.csv

Standard date dimension table for time intelligence in Power BI. One row per calendar date.

| Field | Type | Nullable | Description | Example Values |
|-------|------|----------|-------------|----------------|
| Date | Date (YYYY-MM-DD) | No | Calendar date (primary key) | 2024-01-15 |
| Year | Integer | No | Calendar year | 2024 |
| Quarter | Integer | No | Quarter number (1–4) | 1 |
| QuarterLabel | String | No | Display label | Q1 2024 |
| Month | Integer | No | Month number (1–12) | 1 |
| MonthName | String | No | Full month name | January |
| MonthShort | String | No | Abbreviated month | Jan |
| WeekNumber | Integer | No | ISO week number (1–53) | 3 |
| DayOfWeek | String | No | Full day name | Monday |
| IsWeekend | Boolean | No | TRUE for Saturday and Sunday | FALSE |
| FiscalYear | Integer | No | Fiscal year (July–June cycle) | 2024 |
| FiscalQuarter | Integer | No | Fiscal quarter (1–4, starting July) | 3 |

---

## forecast_output.csv *(generated by forecast_model.py)*

Monthly hiring demand forecast output. Generated programmatically.

| Field | Type | Nullable | Description | Example Values |
|-------|------|----------|-------------|----------------|
| ForecastMonth | String | No | Year-month label | 2025-01 |
| ForecastMonthDate | Date (YYYY-MM-DD) | No | First day of forecast month | 2025-01-01 |
| Scenario | String | Yes | Scenario name (present when scenarios mode enabled) | Base Case, High Growth |
| StartHeadcount | Integer | No | Headcount at start of month | 312 |
| TargetHeadcount | Integer | No | Planned end-of-month headcount | 316 |
| ExpectedAttrition | Integer | No | Projected leavers for the month | 4 |
| GrossHiresNeeded | Integer | No | Total new hires required before internal fills | 8 |
| InternalFills | Integer | No | Vacancies covered by internal moves | 1 |
| PipelineHires | Integer | No | Candidates already in pipeline expected to close | 1 |
| NetHiresRequired | Integer | No | New hires still needed from external recruiting | 6 |
| AttritionRateAnnual | Decimal | No | Assumed annual attrition rate (%) | 14.0 |
| GrowthTargetAnnual | Decimal | No | Assumed annual growth target (%) | 8.0 |

---

## Notes on Data Privacy

- All `EmployeeID` values are synthetic and non-reversible
- No personally identifiable information (PII) is stored in any column
- Salary values are randomly generated and do not reflect real compensation
- Gender and demographic fields use broad categories only
- If connecting to real HRIS data, ensure compliance with GDPR / local privacy regulations before loading into Power BI Service
