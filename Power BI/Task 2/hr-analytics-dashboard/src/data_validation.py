"""
data_validation.py
------------------
Pre-load data quality checks for the HR Analytics Dashboard.
Run this before refreshing Power BI to catch schema or data issues early.

Usage:
    python src/data_validation.py
    python src/data_validation.py --strict   # Exit with error code on any warning
"""

import argparse
import os
import sys
from datetime import date

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Expected schema per file
SCHEMAS = {
    "employees.csv": {
        "required_columns": [
            "EmployeeID", "Department", "JobLevel", "HireDate",
            "Gender", "AgeGroup", "IsActive"
        ],
        "date_columns": ["HireDate", "TerminationDate"],
        "unique_columns": ["EmployeeID"],
        "not_null_columns": ["EmployeeID", "Department", "HireDate", "IsActive"],
    },
    "recruitment.csv": {
        "required_columns": [
            "ReqID", "Department", "RequisitionDate", "SourceChannel", "CandidateStage"
        ],
        "date_columns": ["RequisitionDate", "OfferAcceptedDate"],
        "unique_columns": ["ReqID"],
        "not_null_columns": ["ReqID", "Department", "RequisitionDate"],
    },
    "performance_reviews.csv": {
        "required_columns": [
            "EmployeeID", "ReviewYear", "ReviewCycle", "PerformanceRating"
        ],
        "date_columns": [],
        "unique_columns": [],
        "not_null_columns": ["EmployeeID", "ReviewYear", "PerformanceRating"],
        "range_checks": {"PerformanceRating": (1, 5), "GoalAttainmentPct": (0, 120)},
    },
    "satisfaction_survey.csv": {
        "required_columns": [
            "EmployeeID", "SurveyDate", "eNPS_Score", "eNPS_Category"
        ],
        "date_columns": ["SurveyDate"],
        "unique_columns": [],
        "not_null_columns": ["EmployeeID", "SurveyDate", "eNPS_Score"],
        "range_checks": {"eNPS_Score": (0, 10)},
    },
    "exits.csv": {
        "required_columns": [
            "EmployeeID", "Department", "ExitType", "ExitReason", "TerminationDate"
        ],
        "date_columns": ["HireDate", "TerminationDate"],
        "unique_columns": ["EmployeeID"],
        "not_null_columns": ["EmployeeID", "ExitType", "TerminationDate"],
    },
    "date_table.csv": {
        "required_columns": ["Date", "Year", "Month", "Quarter"],
        "date_columns": ["Date"],
        "unique_columns": ["Date"],
        "not_null_columns": ["Date", "Year", "Month"],
    },
}

ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_RED = "\033[91m"
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"


def ok(msg):
    print(f"  {ANSI_GREEN}✓{ANSI_RESET}  {msg}")


def warn(msg, warnings_list):
    print(f"  {ANSI_YELLOW}⚠{ANSI_RESET}  {msg}")
    warnings_list.append(msg)


def error(msg, errors_list):
    print(f"  {ANSI_RED}✗{ANSI_RESET}  {msg}")
    errors_list.append(msg)


def validate_file(filename: str, schema: dict) -> tuple[list, list]:
    """Validate a single CSV file against its schema. Returns (warnings, errors)."""
    filepath = os.path.join(DATA_DIR, filename)
    warnings, errors_found = [], []

    print(f"\n{ANSI_BOLD}── {filename}{ANSI_RESET}")

    # File existence
    if not os.path.exists(filepath):
        error(f"File not found: {filepath}", errors_found)
        return warnings, errors_found

    # Load
    try:
        df = pd.read_csv(filepath, low_memory=False)
    except Exception as e:
        error(f"Could not read CSV: {e}", errors_found)
        return warnings, errors_found

    ok(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

    # Required columns
    missing_cols = [c for c in schema["required_columns"] if c not in df.columns]
    if missing_cols:
        error(f"Missing required columns: {missing_cols}", errors_found)
    else:
        ok("All required columns present")

    # Row count sanity
    if len(df) == 0:
        error("File is empty (0 rows)", errors_found)
        return warnings, errors_found

    # Unique columns
    for col in schema.get("unique_columns", []):
        if col in df.columns:
            dupes = df[col].duplicated().sum()
            if dupes > 0:
                error(f"Column '{col}' has {dupes:,} duplicate values (expected unique)", errors_found)
            else:
                ok(f"'{col}' is unique")

    # Not-null columns
    for col in schema.get("not_null_columns", []):
        if col in df.columns:
            nulls = df[col].isnull().sum() + (df[col] == "").sum()
            if nulls > 0:
                warn(f"'{col}' has {nulls:,} null/empty values", warnings)
            else:
                ok(f"'{col}' has no nulls")

    # Date columns — parse check
    for col in schema.get("date_columns", []):
        if col in df.columns:
            non_empty = df[col].replace("", pd.NA).dropna()
            if len(non_empty) == 0:
                warn(f"Date column '{col}' is entirely empty", warnings)
                continue
            try:
                parsed = pd.to_datetime(non_empty, errors="coerce")
                bad = parsed.isna().sum()
                if bad > 0:
                    warn(f"Date column '{col}' has {bad:,} unparseable values", warnings)
                else:
                    ok(f"'{col}' dates parse correctly")
                # Future date check for hire/termination
                if col in ("HireDate", "TerminationDate", "OfferAcceptedDate"):
                    future = (parsed > pd.Timestamp(date.today())).sum()
                    if future > 0:
                        warn(f"'{col}' has {future:,} dates in the future", warnings)
            except Exception as e:
                warn(f"Could not parse '{col}': {e}", warnings)

    # Range checks
    for col, (low, high) in schema.get("range_checks", {}).items():
        if col in df.columns:
            numeric = pd.to_numeric(df[col], errors="coerce").dropna()
            out_of_range = ((numeric < low) | (numeric > high)).sum()
            if out_of_range > 0:
                warn(f"'{col}' has {out_of_range:,} values outside [{low}, {high}]", warnings)
            else:
                ok(f"'{col}' values within range [{low}, {high}]")

    return warnings, errors_found


def validate_referential_integrity() -> tuple[list, list]:
    """Cross-file referential integrity checks."""
    warnings, errors_found = [], []
    print(f"\n{ANSI_BOLD}── Referential Integrity{ANSI_RESET}")

    try:
        emp_file = os.path.join(DATA_DIR, "employees.csv")
        perf_file = os.path.join(DATA_DIR, "performance_reviews.csv")
        survey_file = os.path.join(DATA_DIR, "satisfaction_survey.csv")

        if not all(os.path.exists(f) for f in [emp_file, perf_file, survey_file]):
            warn("Skipping referential integrity (some files missing)", warnings)
            return warnings, errors_found

        employees = pd.read_csv(emp_file)
        emp_ids = set(employees["EmployeeID"].dropna())

        performance = pd.read_csv(perf_file)
        perf_orphans = set(performance["EmployeeID"].dropna()) - emp_ids
        if perf_orphans:
            warn(f"performance_reviews.csv has {len(perf_orphans)} EmployeeIDs not in employees.csv", warnings)
        else:
            ok("performance_reviews.csv → employees.csv: all IDs match")

        surveys = pd.read_csv(survey_file)
        survey_orphans = set(surveys["EmployeeID"].dropna()) - emp_ids
        if survey_orphans:
            warn(f"satisfaction_survey.csv has {len(survey_orphans)} EmployeeIDs not in employees.csv", warnings)
        else:
            ok("satisfaction_survey.csv → employees.csv: all IDs match")

    except Exception as e:
        warn(f"Referential integrity check failed: {e}", warnings)

    return warnings, errors_found


def main(strict: bool = False):
    print(f"\n{ANSI_BOLD}{'='*60}{ANSI_RESET}")
    print(f"{ANSI_BOLD} HR Analytics Dashboard — Data Validation Report{ANSI_RESET}")
    print(f"{ANSI_BOLD}{'='*60}{ANSI_RESET}")
    print(f"  Data directory : {os.path.abspath(DATA_DIR)}")
    print(f"  Run at         : {date.today().isoformat()}")

    all_warnings, all_errors = [], []

    for filename, schema in SCHEMAS.items():
        w, e = validate_file(filename, schema)
        all_warnings.extend(w)
        all_errors.extend(e)

    ri_w, ri_e = validate_referential_integrity()
    all_warnings.extend(ri_w)
    all_errors.extend(ri_e)

    # Summary
    print(f"\n{ANSI_BOLD}── Summary{ANSI_RESET}")
    print(f"  Total warnings : {ANSI_YELLOW}{len(all_warnings)}{ANSI_RESET}")
    print(f"  Total errors   : {ANSI_RED}{len(all_errors)}{ANSI_RESET}")

    if all_errors:
        print(f"\n{ANSI_RED}{ANSI_BOLD}❌  Validation FAILED — fix errors before loading into Power BI.{ANSI_RESET}")
        sys.exit(1)
    elif all_warnings and strict:
        print(f"\n{ANSI_YELLOW}{ANSI_BOLD}⚠️  Strict mode: warnings treated as errors.{ANSI_RESET}")
        sys.exit(1)
    else:
        print(f"\n{ANSI_GREEN}{ANSI_BOLD}✅  Validation PASSED — data is ready for Power BI.{ANSI_RESET}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate HR dashboard CSV files.")
    parser.add_argument("--strict", action="store_true", help="Exit with error on warnings too")
    args = parser.parse_args()
    main(strict=args.strict)
