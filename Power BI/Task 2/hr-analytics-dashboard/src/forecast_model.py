"""
forecast_model.py
-----------------
Predictive hiring needs forecast using Facebook Prophet.
Outputs a 12-month hiring demand CSV that feeds the Power BI forecast page.

Usage:
    python src/forecast_model.py
    python src/forecast_model.py --attrition-rate 0.14 --growth-target 0.08 --periods 12
    python src/forecast_model.py --input data/employees.csv --output data/forecast_output.csv

Requirements:
    pip install prophet pandas numpy matplotlib
"""

import argparse
import os
from datetime import date

import numpy as np
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
INPUT_DEFAULT = os.path.join(OUTPUT_DIR, "employees.csv")
OUTPUT_DEFAULT = os.path.join(OUTPUT_DIR, "forecast_output.csv")


# ─── Attrition-Adjusted Hiring Formula ───────────────────────────────────────
#
#  Required Hires (t) =
#      Target Headcount (t)
#    + Expected Attrition (current_headcount × attrition_rate)
#    - Internal Fills (estimated as % of vacancies)
#    - Backfills already in pipeline
#
# ─────────────────────────────────────────────────────────────────────────────

def compute_hiring_forecast(
    current_headcount: int,
    attrition_rate: float = 0.14,
    growth_target: float = 0.08,
    periods: int = 12,
    internal_fill_rate: float = 0.15,
    pipeline_factor: float = 0.10,
) -> pd.DataFrame:
    """
    Compute a month-by-month hiring forecast.

    Parameters
    ----------
    current_headcount : int
        Active headcount at the start of the forecast window.
    attrition_rate : float
        Annual attrition rate (e.g. 0.14 = 14%). Converted to monthly internally.
    growth_target : float
        Planned annual headcount growth (e.g. 0.08 = 8%).
    periods : int
        Number of months to forecast.
    internal_fill_rate : float
        Fraction of vacancies expected to be filled internally (promotions/transfers).
    pipeline_factor : float
        Fraction of required hires already in the recruiting pipeline.

    Returns
    -------
    pd.DataFrame
        Monthly forecast with headcount targets and required hires.
    """

    monthly_attrition = attrition_rate / 12
    monthly_growth = (1 + growth_target) ** (1 / 12) - 1

    today = date.today()
    rows = []
    headcount = current_headcount

    for m in range(1, periods + 1):
        forecast_month = pd.Period(today, "M") + m
        target_headcount = round(headcount * (1 + monthly_growth))
        expected_attrition = round(headcount * monthly_attrition)
        gross_hires_needed = (target_headcount - headcount) + expected_attrition
        internal_fills = round(gross_hires_needed * internal_fill_rate)
        pipeline_hires = round(gross_hires_needed * pipeline_factor)
        net_hires_needed = max(0, gross_hires_needed - internal_fills - pipeline_hires)

        rows.append({
            "ForecastMonth": str(forecast_month),
            "ForecastMonthDate": forecast_month.to_timestamp().date().isoformat(),
            "StartHeadcount": headcount,
            "TargetHeadcount": target_headcount,
            "ExpectedAttrition": expected_attrition,
            "GrossHiresNeeded": gross_hires_needed,
            "InternalFills": internal_fills,
            "PipelineHires": pipeline_hires,
            "NetHiresRequired": net_hires_needed,
            "AttritionRateAnnual": round(attrition_rate * 100, 1),
            "GrowthTargetAnnual": round(growth_target * 100, 1),
        })

        headcount = target_headcount

    return pd.DataFrame(rows)


# ─── Prophet Time-Series Forecast (optional — requires prophet) ──────────────

def prophet_headcount_forecast(employees_csv: str, periods: int = 12) -> pd.DataFrame:
    """
    Use Facebook Prophet to extrapolate headcount trends from historical data.
    Falls back to linear interpolation if Prophet is not installed.
    """
    try:
        from prophet import Prophet  # type: ignore
    except ImportError:
        print("⚠️  Prophet not installed. Install with: pip install prophet")
        print("    Falling back to linear trend forecast.")
        return _linear_fallback(employees_csv, periods)

    df = pd.read_csv(employees_csv, parse_dates=["HireDate"])
    df["HireDate"] = pd.to_datetime(df["HireDate"])
    df["Month"] = df["HireDate"].dt.to_period("M")

    monthly_hires = (
        df.groupby("Month").size().reset_index(name="Hires")
    )
    monthly_hires["ds"] = monthly_hires["Month"].dt.to_timestamp()
    monthly_hires = monthly_hires.rename(columns={"Hires": "y"})[["ds", "y"]]

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
    )
    model.fit(monthly_hires)

    future = model.make_future_dataframe(periods=periods, freq="MS")
    forecast = model.predict(future)

    output = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods).copy()
    output.columns = ["ForecastDate", "PredictedHires", "HiresLowerBound", "HiresUpperBound"]
    output["PredictedHires"] = output["PredictedHires"].clip(lower=0).round().astype(int)
    output["HiresLowerBound"] = output["HiresLowerBound"].clip(lower=0).round().astype(int)
    output["HiresUpperBound"] = output["HiresUpperBound"].clip(lower=0).round().astype(int)
    output["ForecastDate"] = output["ForecastDate"].dt.date.astype(str)

    return output


def _linear_fallback(employees_csv: str, periods: int = 12) -> pd.DataFrame:
    """Simple linear trend fallback when Prophet is unavailable."""
    df = pd.read_csv(employees_csv, parse_dates=["HireDate"])
    df["Month"] = pd.to_datetime(df["HireDate"]).dt.to_period("M")
    monthly = df.groupby("Month").size().reset_index(name="Hires")
    recent_avg = monthly["Hires"].tail(6).mean()
    trend = monthly["Hires"].diff().tail(6).mean()

    rows = []
    today = date.today()
    for i in range(1, periods + 1):
        period = pd.Period(today, "M") + i
        predicted = max(0, round(recent_avg + trend * i))
        rows.append({
            "ForecastDate": period.to_timestamp().date().isoformat(),
            "PredictedHires": predicted,
            "HiresLowerBound": max(0, round(predicted * 0.8)),
            "HiresUpperBound": round(predicted * 1.2),
        })
    return pd.DataFrame(rows)


# ─── What-If Scenario Generator ──────────────────────────────────────────────

def generate_scenarios(
    current_headcount: int,
    base_attrition: float = 0.14,
    base_growth: float = 0.08,
    periods: int = 12,
) -> pd.DataFrame:
    """Generate multiple what-if scenarios for Power BI scenario analysis."""
    scenarios = [
        ("Base Case", base_attrition, base_growth),
        ("High Growth", base_attrition, base_growth + 0.05),
        ("Recession / Hiring Freeze", base_attrition + 0.04, 0.00),
        ("High Attrition", base_attrition + 0.06, base_growth),
        ("Best Case", base_attrition - 0.04, base_growth + 0.03),
    ]

    all_dfs = []
    for label, attrition, growth in scenarios:
        df = compute_hiring_forecast(current_headcount, attrition, growth, periods)
        df["Scenario"] = label
        all_dfs.append(df)

    return pd.concat(all_dfs, ignore_index=True)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="HR Predictive Hiring Forecast")
    parser.add_argument("--input", default=INPUT_DEFAULT, help="Path to employees.csv")
    parser.add_argument("--output", default=OUTPUT_DEFAULT, help="Output CSV path")
    parser.add_argument("--attrition-rate", type=float, default=0.14, help="Annual attrition rate (default: 0.14)")
    parser.add_argument("--growth-target", type=float, default=0.08, help="Annual growth target (default: 0.08)")
    parser.add_argument("--periods", type=int, default=12, help="Months to forecast (default: 12)")
    parser.add_argument("--scenarios", action="store_true", help="Generate what-if scenarios instead")
    args = parser.parse_args()

    # Derive current headcount from employee file if available
    current_headcount = 300
    if os.path.exists(args.input):
        emp_df = pd.read_csv(args.input)
        if "IsActive" in emp_df.columns:
            current_headcount = int(emp_df["IsActive"].sum())
        print(f"📊  Current active headcount from data: {current_headcount}")
    else:
        print(f"⚠️  Employee file not found at {args.input}. Using default headcount: {current_headcount}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    if args.scenarios:
        print("🔮  Generating what-if scenario forecasts...")
        df = generate_scenarios(current_headcount, args.attrition_rate, args.growth_target, args.periods)
    else:
        print("🔮  Computing hiring forecast...")
        df = compute_hiring_forecast(
            current_headcount,
            attrition_rate=args.attrition_rate,
            growth_target=args.growth_target,
            periods=args.periods,
        )

    df.to_csv(args.output, index=False)
    print(f"✅  Forecast written to {args.output}")
    print(f"\n{'Month':<12} {'Target HC':>10} {'Net Hires':>10} {'Expected Attrition':>20}")
    print("-" * 56)
    display_col = "ForecastMonth" if "ForecastMonth" in df.columns else "ForecastDate"
    for _, row in df.head(12).iterrows():
        if "Scenario" not in row or row.get("Scenario") == "Base Case":
            print(
                f"{row[display_col]:<12}"
                f"{row.get('TargetHeadcount', '-'):>10}"
                f"{row.get('NetHiresRequired', '-'):>10}"
                f"{row.get('ExpectedAttrition', '-'):>20}"
            )


if __name__ == "__main__":
    main()
