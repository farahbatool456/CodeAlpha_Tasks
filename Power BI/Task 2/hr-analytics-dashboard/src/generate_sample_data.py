"""
generate_sample_data.py
-----------------------
Generates synthetic HR datasets for the HR Analytics Dashboard.
All data is fictional and for demonstration purposes only.

Usage:
    python src/generate_sample_data.py
    python src/generate_sample_data.py --employees 500 --years 3
"""

import argparse
import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)
np.random.seed(42)

# ─── Configuration ────────────────────────────────────────────────────────────

DEPARTMENTS = [
    "Engineering", "Product", "Sales", "Marketing",
    "Finance", "HR", "Operations", "Legal", "Customer Success", "Data Science"
]

JOB_LEVELS = ["IC1", "IC2", "IC3", "IC4", "IC5", "M1", "M2", "M3", "D1"]

LEVEL_WEIGHTS = [0.20, 0.25, 0.20, 0.15, 0.08, 0.06, 0.04, 0.015, 0.005]

SOURCE_CHANNELS = ["LinkedIn", "Employee Referral", "Job Board", "Recruiting Agency", "Direct / Career Page", "University Recruiting"]

EXIT_REASONS = [
    "Better compensation elsewhere",
    "Career growth opportunity",
    "Work-life balance",
    "Relocation",
    "Manager relationship",
    "Company culture",
    "Role change",
    "Personal reasons",
    "Performance-based",
    "Layoff / Restructuring"
]

PERFORMANCE_RATINGS = [1, 2, 3, 4, 5]
RATING_WEIGHTS = [0.05, 0.10, 0.45, 0.30, 0.10]

AGE_GROUPS = ["18-25", "26-35", "36-45", "46-55", "55+"]
AGE_WEIGHTS = [0.10, 0.35, 0.30, 0.18, 0.07]

GENDERS = ["Male", "Female", "Non-binary / Gender non-conforming", "Prefer not to say"]
GENDER_WEIGHTS = [0.48, 0.45, 0.04, 0.03]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def random_date(start: date, end: date) -> date:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def weighted_choice(choices, weights):
    return random.choices(choices, weights=weights, k=1)[0]


# ─── Employee Master Data ─────────────────────────────────────────────────────

def generate_employees(n: int = 300, years_back: int = 5) -> pd.DataFrame:
    today = date.today()
    start_window = today - timedelta(days=365 * years_back)

    records = []
    manager_pool = []

    for i in range(1, n + 1):
        emp_id = f"EMP{i:04d}"
        dept = random.choice(DEPARTMENTS)
        level = weighted_choice(JOB_LEVELS, LEVEL_WEIGHTS)
        hire_date = random_date(start_window, today - timedelta(days=30))
        gender = weighted_choice(GENDERS, GENDER_WEIGHTS)
        age_group = weighted_choice(AGE_GROUPS, AGE_WEIGHTS)

        # ~12% attrition
        is_active = random.random() > 0.12
        termination_date = None if is_active else random_date(hire_date + timedelta(days=90), today)

        # Manager assignment (simplified)
        manager_id = random.choice(manager_pool) if manager_pool and level not in ["M3", "D1"] else None
        if level in ["M1", "M2", "M3", "D1"]:
            manager_pool.append(emp_id)

        records.append({
            "EmployeeID": emp_id,
            "Department": dept,
            "JobLevel": level,
            "HireDate": hire_date.isoformat(),
            "Gender": gender,
            "AgeGroup": age_group,
            "IsActive": is_active,
            "TerminationDate": termination_date.isoformat() if termination_date else "",
            "ManagerID": manager_id or "",
            "Location": fake.city(),
            "EmploymentType": weighted_choice(["Full-time", "Part-time", "Contract"], [0.82, 0.10, 0.08]),
            "Salary": round(random.gauss(85000, 25000), -2),
        })

    df = pd.DataFrame(records)
    df["Salary"] = df["Salary"].clip(lower=35000, upper=250000)
    return df


# ─── Recruitment Data ─────────────────────────────────────────────────────────

def generate_recruitment(n: int = 400, years_back: int = 3) -> pd.DataFrame:
    today = date.today()
    start_window = today - timedelta(days=365 * years_back)
    stages = ["Application", "Phone Screen", "Technical Interview", "Final Interview", "Offer", "Hired", "Rejected"]

    records = []
    for i in range(1, n + 1):
        req_date = random_date(start_window, today - timedelta(days=10))
        dept = random.choice(DEPARTMENTS)
        level = weighted_choice(JOB_LEVELS, LEVEL_WEIGHTS)
        channel = weighted_choice(SOURCE_CHANNELS, [0.30, 0.25, 0.20, 0.12, 0.08, 0.05])

        is_hired = random.random() < 0.55
        final_stage = "Hired" if is_hired else random.choice(["Rejected", "Offer", "Final Interview"])

        time_to_fill = int(random.gauss(32, 12)) if is_hired else None
        offer_accepted_date = (req_date + timedelta(days=time_to_fill)).isoformat() if is_hired and time_to_fill else ""

        hiring_cost = round(random.uniform(2500, 18000), 2) if is_hired else round(random.uniform(500, 3000), 2)

        records.append({
            "ReqID": f"REQ{i:04d}",
            "Department": dept,
            "JobLevel": level,
            "RequisitionDate": req_date.isoformat(),
            "OfferAcceptedDate": offer_accepted_date,
            "TimeToFill_Days": time_to_fill or "",
            "SourceChannel": channel,
            "CandidateStage": final_stage,
            "HiringCost_USD": hiring_cost,
            "OfferExtended": final_stage in ["Offer", "Hired"],
            "OfferAccepted": final_stage == "Hired",
            "DiversityHire": random.random() < 0.42,
        })

    return pd.DataFrame(records)


# ─── Performance Reviews ──────────────────────────────────────────────────────

def generate_performance(employee_ids: list, years_back: int = 3) -> pd.DataFrame:
    today = date.today()
    records = []

    for emp_id in employee_ids:
        # 1–3 review cycles per employee
        for _ in range(random.randint(1, min(3, years_back))):
            review_year = random.randint(today.year - years_back + 1, today.year)
            cycle = weighted_choice(["Annual", "Mid-Year"], [0.65, 0.35])
            rating = weighted_choice(PERFORMANCE_RATINGS, RATING_WEIGHTS)

            records.append({
                "EmployeeID": emp_id,
                "ReviewYear": review_year,
                "ReviewCycle": cycle,
                "PerformanceRating": rating,
                "GoalAttainmentPct": round(random.gauss(85, 15), 1),
                "ManagerRating": weighted_choice(PERFORMANCE_RATINGS, RATING_WEIGHTS),
                "PeerRating": weighted_choice(PERFORMANCE_RATINGS, RATING_WEIGHTS),
                "IsHighPerformer": rating >= 4,
                "IsLowPerformer": rating <= 2,
            })

    df = pd.DataFrame(records)
    df["GoalAttainmentPct"] = df["GoalAttainmentPct"].clip(0, 120)
    return df


# ─── Satisfaction Surveys ─────────────────────────────────────────────────────

def generate_surveys(employee_ids: list, years_back: int = 3) -> pd.DataFrame:
    today = date.today()
    records = []

    for emp_id in random.sample(employee_ids, int(len(employee_ids) * 0.80)):  # 80% participation
        for _ in range(random.randint(1, years_back * 2)):  # pulse surveys
            survey_date = random_date(today - timedelta(days=365 * years_back), today)
            enps_score = random.randint(0, 10)
            category = "Promoter" if enps_score >= 9 else ("Detractor" if enps_score <= 6 else "Passive")

            records.append({
                "EmployeeID": emp_id,
                "SurveyDate": survey_date.isoformat(),
                "eNPS_Score": enps_score,
                "eNPS_Category": category,
                "EngagementScore": round(random.gauss(3.6, 0.8), 2),
                "ManagerSatisfaction": round(random.gauss(3.7, 0.9), 2),
                "WorkLifeBalance": round(random.gauss(3.4, 0.9), 2),
                "CompensationSatisfaction": round(random.gauss(3.2, 0.9), 2),
                "AbsenceDays": max(0, int(random.gauss(4, 3))),
                "SurveyType": weighted_choice(["Annual Engagement", "Pulse", "Onboarding", "Exit"], [0.4, 0.4, 0.1, 0.1]),
            })

    df = pd.DataFrame(records)
    for col in ["EngagementScore", "ManagerSatisfaction", "WorkLifeBalance", "CompensationSatisfaction"]:
        df[col] = df[col].clip(1.0, 5.0)
    return df


# ─── Exit Records ─────────────────────────────────────────────────────────────

def generate_exits(employees_df: pd.DataFrame) -> pd.DataFrame:
    leavers = employees_df[employees_df["IsActive"] == False].copy()
    records = []

    for _, row in leavers.iterrows():
        exit_type = weighted_choice(["Voluntary", "Involuntary"], [0.72, 0.28])
        reason = weighted_choice(EXIT_REASONS, [0.20, 0.18, 0.15, 0.08, 0.12, 0.08, 0.07, 0.05, 0.04, 0.03])
        last_rating = weighted_choice(PERFORMANCE_RATINGS, RATING_WEIGHTS)

        records.append({
            "EmployeeID": row["EmployeeID"],
            "Department": row["Department"],
            "JobLevel": row["JobLevel"],
            "HireDate": row["HireDate"],
            "TerminationDate": row["TerminationDate"],
            "ExitType": exit_type,
            "ExitReason": reason,
            "LastPerformanceRating": last_rating,
            "IsRegrettable": exit_type == "Voluntary" and last_rating >= 4,
            "TenureDays": (
                pd.to_datetime(row["TerminationDate"]) - pd.to_datetime(row["HireDate"])
            ).days if row["TerminationDate"] else None,
            "ConductedExitInterview": random.random() < 0.65,
        })

    return pd.DataFrame(records)


# ─── Date Dimension ───────────────────────────────────────────────────────────

def generate_date_table(years_back: int = 5) -> pd.DataFrame:
    today = date.today()
    start = date(today.year - years_back, 1, 1)
    end = date(today.year + 2, 12, 31)

    dates = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({"Date": dates})
    df["Year"] = df["Date"].dt.year
    df["Quarter"] = df["Date"].dt.quarter
    df["QuarterLabel"] = "Q" + df["Quarter"].astype(str) + " " + df["Year"].astype(str)
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%B")
    df["MonthShort"] = df["Date"].dt.strftime("%b")
    df["WeekNumber"] = df["Date"].dt.isocalendar().week.astype(int)
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["IsWeekend"] = df["Date"].dt.weekday >= 5
    df["FiscalYear"] = df.apply(lambda r: r["Year"] if r["Month"] >= 7 else r["Year"] - 1, axis=1)
    df["FiscalQuarter"] = df.apply(lambda r: ((r["Month"] - 7) % 12) // 3 + 1, axis=1)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df


# ─── Main ─────────────────────────────────────────────────────────────────────

def main(n_employees: int = 300, years_back: int = 3):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("🔄  Generating employee master data...")
    employees = generate_employees(n=n_employees, years_back=years_back + 2)
    employees.to_csv(os.path.join(OUTPUT_DIR, "employees.csv"), index=False)
    print(f"    ✅  {len(employees)} employee records → data/employees.csv")

    print("🔄  Generating recruitment data...")
    recruitment = generate_recruitment(n=int(n_employees * 1.4), years_back=years_back)
    recruitment.to_csv(os.path.join(OUTPUT_DIR, "recruitment.csv"), index=False)
    print(f"    ✅  {len(recruitment)} recruitment records → data/recruitment.csv")

    active_ids = employees["EmployeeID"].tolist()

    print("🔄  Generating performance review data...")
    performance = generate_performance(active_ids, years_back=years_back)
    performance.to_csv(os.path.join(OUTPUT_DIR, "performance_reviews.csv"), index=False)
    print(f"    ✅  {len(performance)} review records → data/performance_reviews.csv")

    print("🔄  Generating satisfaction survey data...")
    surveys = generate_surveys(active_ids, years_back=years_back)
    surveys.to_csv(os.path.join(OUTPUT_DIR, "satisfaction_survey.csv"), index=False)
    print(f"    ✅  {len(surveys)} survey records → data/satisfaction_survey.csv")

    print("🔄  Generating exit records...")
    exits = generate_exits(employees)
    exits.to_csv(os.path.join(OUTPUT_DIR, "exits.csv"), index=False)
    print(f"    ✅  {len(exits)} exit records → data/exits.csv")

    print("🔄  Generating date dimension table...")
    date_table = generate_date_table(years_back=years_back + 2)
    date_table.to_csv(os.path.join(OUTPUT_DIR, "date_table.csv"), index=False)
    print(f"    ✅  {len(date_table)} date rows → data/date_table.csv")

    print("\n✅  All datasets generated successfully in /data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic HR data for the dashboard.")
    parser.add_argument("--employees", type=int, default=300, help="Number of employees to generate (default: 300)")
    parser.add_argument("--years", type=int, default=3, help="Years of historical data (default: 3)")
    args = parser.parse_args()

    main(n_employees=args.employees, years_back=args.years)
