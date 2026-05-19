# DAX Measures Reference

Complete library of all DAX measures used in the HR Analytics Dashboard.  
Copy-paste directly into Power BI Desktop → **Modeling → New Measure**.

---

## Table of Contents

1. [Headcount Measures](#1-headcount-measures)
2. [Attrition & Retention Measures](#2-attrition--retention-measures)
3. [Recruitment Measures](#3-recruitment-measures)
4. [Satisfaction & Engagement Measures](#4-satisfaction--engagement-measures)
5. [Performance Measures](#5-performance-measures)
6. [Forecast Measures](#6-forecast-measures)
7. [Time Intelligence Measures](#7-time-intelligence-measures)
8. [Utility / Formatting Measures](#8-utility--formatting-measures)

---

## 1. Headcount Measures

```dax
-- Total Active Headcount
Headcount =
CALCULATE(
    COUNTROWS(Employees),
    Employees[IsActive] = TRUE()
)

-- Headcount at End of Period
Headcount EOP =
CALCULATE(
    COUNTROWS(Employees),
    Employees[IsActive] = TRUE(),
    LASTDATE('Date'[Date])
)

-- Average Headcount (for attrition denominator)
Avg Headcount =
AVERAGEX(
    SUMMARIZE(
        'Date',
        'Date'[Year],
        'Date'[Month],
        "MthHeadcount",
        CALCULATE(COUNTROWS(Employees), Employees[IsActive] = TRUE())
    ),
    [MthHeadcount]
)

-- New Hires (Period)
New Hires =
CALCULATE(
    COUNTROWS(Employees),
    DATESBETWEEN(
        Employees[HireDate],
        STARTOFMONTH(LASTDATE('Date'[Date])),
        ENDOFMONTH(LASTDATE('Date'[Date]))
    )
)

-- Headcount by Department
Headcount by Dept =
CALCULATE(
    [Headcount],
    ALLEXCEPT(Employees, Employees[Department])
)

-- Headcount YoY Change
Headcount YoY Change =
[Headcount] - CALCULATE([Headcount], SAMEPERIODLASTYEAR('Date'[Date]))

-- Headcount YoY Change %
Headcount YoY % =
DIVIDE(
    [Headcount YoY Change],
    CALCULATE([Headcount], SAMEPERIODLASTYEAR('Date'[Date])),
    0
)
```

---

## 2. Attrition & Retention Measures

```dax
-- Total Leavers
Total Leavers =
CALCULATE(
    COUNTROWS(Exits),
    NOT(ISBLANK(Exits[TerminationDate]))
)

-- Voluntary Leavers
Voluntary Leavers =
CALCULATE(
    COUNTROWS(Exits),
    Exits[ExitType] = "Voluntary"
)

-- Involuntary Leavers
Involuntary Leavers =
CALCULATE(
    COUNTROWS(Exits),
    Exits[ExitType] = "Involuntary"
)

-- Attrition Rate (Annual)
Attrition Rate =
DIVIDE(
    [Total Leavers],
    [Avg Headcount],
    0
) * 100

-- Voluntary Attrition Rate
Voluntary Attrition Rate =
DIVIDE(
    [Voluntary Leavers],
    [Avg Headcount],
    0
) * 100

-- Regrettable Attrition
Regrettable Leavers =
CALCULATE(
    COUNTROWS(Exits),
    Exits[IsRegrettable] = TRUE()
)

-- Regrettable Attrition Rate
Regrettable Attrition Rate =
DIVIDE(
    [Regrettable Leavers],
    [Total Leavers],
    0
) * 100

-- Rolling 12-Month Attrition
Attrition Rate Rolling 12M =
DIVIDE(
    CALCULATE(
        [Total Leavers],
        DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -12, MONTH)
    ),
    CALCULATE(
        [Avg Headcount],
        DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -12, MONTH)
    ),
    0
) * 100

-- Average Tenure (Days) of Leavers
Avg Tenure Leavers (Days) =
AVERAGEX(
    FILTER(Exits, NOT(ISBLANK(Exits[TenureDays]))),
    Exits[TenureDays]
)

-- Retention Rate
Retention Rate =
100 - [Attrition Rate]
```

---

## 3. Recruitment Measures

```dax
-- Total Applications
Total Applications =
COUNTROWS(Recruitment)

-- Total Hires
Total Hires =
CALCULATE(
    COUNTROWS(Recruitment),
    Recruitment[CandidateStage] = "Hired"
)

-- Offers Extended
Offers Extended =
CALCULATE(
    COUNTROWS(Recruitment),
    Recruitment[OfferExtended] = TRUE()
)

-- Offer Acceptance Rate
Offer Acceptance Rate =
DIVIDE(
    [Total Hires],
    [Offers Extended],
    0
) * 100

-- Average Time to Fill (Days)
Avg Time to Fill =
CALCULATE(
    AVERAGEX(
        FILTER(Recruitment, Recruitment[CandidateStage] = "Hired"),
        Recruitment[TimeToFill_Days]
    )
)

-- Average Cost per Hire
Avg Cost per Hire =
CALCULATE(
    AVERAGEX(
        FILTER(Recruitment, Recruitment[CandidateStage] = "Hired"),
        Recruitment[HiringCost_USD]
    )
)

-- Total Recruiting Cost
Total Recruiting Cost =
SUMX(Recruitment, Recruitment[HiringCost_USD])

-- Applicant-to-Hire Ratio
Applicant to Hire Ratio =
DIVIDE(
    [Total Applications],
    [Total Hires],
    0
)

-- Hiring Funnel Conversion (Application → Hire)
Hiring Conversion Rate =
DIVIDE(
    [Total Hires],
    [Total Applications],
    0
) * 100

-- Diversity Hire %
Diversity Hire Pct =
CALCULATE(
    DIVIDE(
        COUNTROWS(FILTER(Recruitment, Recruitment[DiversityHire] = TRUE())),
        [Total Hires],
        0
    ) * 100,
    Recruitment[CandidateStage] = "Hired"
)

-- Top Source Channel (by hires)
Top Source Channel =
CALCULATE(
    TOPN(1,
        SUMMARIZE(Recruitment, Recruitment[SourceChannel], "Hires", [Total Hires]),
        [Hires], DESC
    ),
    ALLEXCEPT(Recruitment, Recruitment[SourceChannel])
)
```

---

## 4. Satisfaction & Engagement Measures

```dax
-- Average eNPS Score
Avg eNPS Score =
AVERAGE(Survey[eNPS_Score])

-- eNPS (Net Promoter Score)
eNPS =
VAR TotalResponses = COUNTROWS(Survey)
VAR Promoters =
    CALCULATE(COUNTROWS(Survey), Survey[eNPS_Score] >= 9) / TotalResponses * 100
VAR Detractors =
    CALCULATE(COUNTROWS(Survey), Survey[eNPS_Score] <= 6) / TotalResponses * 100
RETURN
    ROUND(Promoters - Detractors, 1)

-- % Promoters
Pct Promoters =
DIVIDE(
    CALCULATE(COUNTROWS(Survey), Survey[eNPS_Category] = "Promoter"),
    COUNTROWS(Survey),
    0
) * 100

-- % Passives
Pct Passives =
DIVIDE(
    CALCULATE(COUNTROWS(Survey), Survey[eNPS_Category] = "Passive"),
    COUNTROWS(Survey),
    0
) * 100

-- % Detractors
Pct Detractors =
DIVIDE(
    CALCULATE(COUNTROWS(Survey), Survey[eNPS_Category] = "Detractor"),
    COUNTROWS(Survey),
    0
) * 100

-- Avg Engagement Score
Avg Engagement Score =
AVERAGE(Survey[EngagementScore])

-- Avg Manager Satisfaction
Avg Manager Satisfaction =
AVERAGE(Survey[ManagerSatisfaction])

-- Avg Work-Life Balance Score
Avg Work-Life Balance =
AVERAGE(Survey[WorkLifeBalance])

-- Survey Participation Rate
Survey Participation Rate =
DIVIDE(
    DISTINCTCOUNT(Survey[EmployeeID]),
    CALCULATE(COUNTROWS(Employees), Employees[IsActive] = TRUE()),
    0
) * 100

-- Absenteeism Rate
Absenteeism Rate =
DIVIDE(
    SUM(Survey[AbsenceDays]),
    CALCULATE(COUNTROWS(Employees), Employees[IsActive] = TRUE()) * 260,
    0
) * 100

-- eNPS Trend (MoM Change)
eNPS MoM Change =
[eNPS] - CALCULATE([eNPS], PREVIOUSMONTH('Date'[Date]))
```

---

## 5. Performance Measures

```dax
-- Average Performance Rating
Avg Performance Rating =
AVERAGE(Performance[PerformanceRating])

-- Average Goal Attainment %
Avg Goal Attainment =
AVERAGE(Performance[GoalAttainmentPct])

-- % High Performers (Rating 4+)
Pct High Performers =
DIVIDE(
    CALCULATE(COUNTROWS(Performance), Performance[IsHighPerformer] = TRUE()),
    COUNTROWS(Performance),
    0
) * 100

-- % Low Performers (Rating 1-2)
Pct Low Performers =
DIVIDE(
    CALCULATE(COUNTROWS(Performance), Performance[IsLowPerformer] = TRUE()),
    COUNTROWS(Performance),
    0
) * 100

-- Rating Distribution (for bell curve)
Rating Count =
COUNTROWS(Performance)

-- Performance Rating Label
Rating Label =
SWITCH(
    SELECTEDVALUE(Performance[PerformanceRating]),
    1, "Needs Improvement",
    2, "Below Expectations",
    3, "Meets Expectations",
    4, "Exceeds Expectations",
    5, "Outstanding",
    "Unknown"
)

-- 9-Box Grid Segment
9Box Segment =
VAR PerfRating = SELECTEDVALUE(Performance[PerformanceRating])
VAR PotentialScore = SELECTEDVALUE(Performance[ManagerRating])
RETURN
SWITCH(
    TRUE(),
    PerfRating >= 4 && PotentialScore >= 4, "Star / High Potential",
    PerfRating >= 4 && PotentialScore = 3,  "Consistent Star",
    PerfRating = 3  && PotentialScore >= 4, "High Potential",
    PerfRating = 3  && PotentialScore = 3,  "Core Contributor",
    PerfRating <= 2 && PotentialScore >= 4, "Enigma",
    PerfRating <= 2 && PotentialScore = 3,  "Inconsistent Player",
    PerfRating >= 4 && PotentialScore <= 2, "Trusted Professional",
    PerfRating = 3  && PotentialScore <= 2, "Effective / Good",
    "Under Performer"
)
```

---

## 6. Forecast Measures

```dax
-- Required Hires Next Month (simple formula)
Required Hires Next Month =
VAR CurrentHC = [Headcount]
VAR MonthlyAttrition = DIVIDE([Attrition Rate Rolling 12M], 100) / 12
VAR MonthlyGrowth = 0.007  -- ~8% annual ÷ 12
RETURN
    ROUND(CurrentHC * (MonthlyGrowth + MonthlyAttrition), 0)

-- Forecast Headcount (from Forecast table)
Forecast Headcount =
CALCULATE(
    SUM(Forecast[TargetHeadcount]),
    Forecast[Scenario] = "Base Case"
)

-- Forecast Net Hires (from Forecast table)
Forecast Net Hires =
CALCULATE(
    SUM(Forecast[NetHiresRequired]),
    Forecast[Scenario] = "Base Case"
)
```

---

## 7. Time Intelligence Measures

```dax
-- Headcount Previous Year
Headcount PY =
CALCULATE([Headcount], SAMEPERIODLASTYEAR('Date'[Date]))

-- Attrition Rate Previous Year
Attrition Rate PY =
CALCULATE([Attrition Rate], SAMEPERIODLASTYEAR('Date'[Date]))

-- Hires YTD
Hires YTD =
CALCULATE([Total Hires], DATESYTD('Date'[Date]))

-- Hires PYTD
Hires PYTD =
CALCULATE([Total Hires], DATESYTD(SAMEPERIODLASTYEAR('Date'[Date])))

-- Hires YTD vs PYTD
Hires YTD vs PYTD =
[Hires YTD] - [Hires PYTD]

-- Rolling 3-Month Avg Hires
Hires Rolling 3M Avg =
CALCULATE(
    DIVIDE([Total Hires], 3),
    DATESINPERIOD('Date'[Date], LASTDATE('Date'[Date]), -3, MONTH)
)
```

---

## 8. Utility / Formatting Measures

```dax
-- Dynamic Title (for visuals)
Selected Department Title =
"Department: " & IF(ISFILTERED(Employees[Department]),
    SELECTEDVALUE(Employees[Department], "Multiple Selected"),
    "All Departments"
)

-- KPI Color (Attrition — Red if high)
Attrition Color =
IF([Attrition Rate] > 15, "#E74C3C",
    IF([Attrition Rate] > 10, "#F39C12", "#27AE60")
)

-- Trend Arrow (MoM eNPS)
eNPS Trend Arrow =
IF([eNPS MoM Change] > 0, "▲ " & FORMAT([eNPS MoM Change], "0.0"),
    IF([eNPS MoM Change] < 0, "▼ " & FORMAT(ABS([eNPS MoM Change]), "0.0"), "→ 0.0")
)

-- Blank Placeholder (for spacing in card visuals)
Blank Measure = BLANK()
```

---

## Relationships Required

| From Table | From Column | To Table | To Column | Cardinality |
|------------|-------------|----------|-----------|-------------|
| Employees | HireDate | Date | Date | Many-to-One |
| Exits | TerminationDate | Date | Date | Many-to-One |
| Recruitment | RequisitionDate | Date | Date | Many-to-One |
| Survey | SurveyDate | Date | Date | Many-to-One |
| Performance | EmployeeID | Employees | EmployeeID | Many-to-One |
| Survey | EmployeeID | Employees | EmployeeID | Many-to-One |
| Exits | EmployeeID | Employees | EmployeeID | Many-to-One |

> All Date relationships should be **inactive** except the primary one — use `USERELATIONSHIP()` in DAX when filtering on alternate dates.
