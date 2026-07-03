"""
Simple A/B testing analysis script.

Run from the project root:
    python src/analyze_ab_test.py
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def clean_columns(columns):
    cleaned = []
    for col in columns:
        col = col.strip().lower()
        col = col.replace("[usd]", "usd")
        col = col.replace("# of ", "")
        col = col.replace("#", "")
        col = col.replace(" ", "_")
        col = col.replace("__", "_")
        cleaned.append(col)
    return cleaned


def load_group(file_name, group_name):
    df = pd.read_csv(DATA_DIR / file_name, sep=";")
    df.columns = clean_columns(df.columns)
    df = df.rename(columns={"purchase": "purchases"})
    df["group"] = group_name
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
    return df


def main():
    control = load_group("control_group.csv", "control")
    test = load_group("test_group.csv", "test")
    df = pd.concat([control, test], ignore_index=True)

    # Save missing-value report and remove incomplete rows.
    missing = df.isna().sum().reset_index()
    missing.columns = ["column", "missing_values"]
    missing.to_csv(OUTPUT_DIR / "missing_values_report.csv", index=False)

    df = df.dropna().copy()
    df.to_csv(DATA_DIR / "combined_clean_campaign_data.csv", index=False)

    summary = df.groupby("group").agg(
        days=("date", "nunique"),
        total_spend=("spend_usd", "sum"),
        total_impressions=("impressions", "sum"),
        total_clicks=("website_clicks", "sum"),
        total_add_to_cart=("add_to_cart", "sum"),
        total_purchases=("purchases", "sum"),
    ).reset_index()

    summary["purchase_conversion_rate"] = summary["total_purchases"] / summary["total_clicks"]
    summary["click_through_rate"] = summary["total_clicks"] / summary["total_impressions"]
    summary["add_to_cart_rate"] = summary["total_add_to_cart"] / summary["total_clicks"]
    summary["cost_per_click"] = summary["total_spend"] / summary["total_clicks"]
    summary["cost_per_purchase"] = summary["total_spend"] / summary["total_purchases"]
    summary.to_csv(OUTPUT_DIR / "campaign_summary.csv", index=False)

    test_row = summary.loc[summary["group"] == "test"].iloc[0]
    control_row = summary.loc[summary["group"] == "control"].iloc[0]

    test_successes = int(test_row["total_purchases"])
    test_n = int(test_row["total_clicks"])
    control_successes = int(control_row["total_purchases"])
    control_n = int(control_row["total_clicks"])

    z_stat, p_value = proportions_ztest(
        count=np.array([test_successes, control_successes]),
        nobs=np.array([test_n, control_n])
    )
    ci_low, ci_high = confint_proportions_2indep(
        count1=test_successes,
        nobs1=test_n,
        count2=control_successes,
        nobs2=control_n,
        method="wald"
    )

    rate_diff = test_row["purchase_conversion_rate"] - control_row["purchase_conversion_rate"]
    relative_lift = rate_diff / control_row["purchase_conversion_rate"]

    results = pd.DataFrame([{
        "metric": "purchase_conversion_rate",
        "control_rate": control_row["purchase_conversion_rate"],
        "test_rate": test_row["purchase_conversion_rate"],
        "absolute_difference_test_minus_control": rate_diff,
        "relative_lift": relative_lift,
        "z_statistic": z_stat,
        "p_value": p_value,
        "confidence_interval_low": ci_low,
        "confidence_interval_high": ci_high,
    }])
    results.to_csv(OUTPUT_DIR / "statistical_test_results.csv", index=False)

    baseline = control_row["purchase_conversion_rate"]
    mde = 0.01
    effect_size = proportion_effectsize(baseline, baseline + mde)
    required_n = NormalIndPower().solve_power(
        effect_size=effect_size,
        power=0.80,
        alpha=0.05,
        ratio=1,
    )
    pd.DataFrame([{
        "baseline_rate": baseline,
        "minimum_detectable_effect": mde,
        "alpha": 0.05,
        "power": 0.80,
        "required_clicks_per_group": int(np.ceil(required_n)),
    }]).to_csv(OUTPUT_DIR / "power_analysis_results.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.bar(summary["group"], summary["purchase_conversion_rate"])
    plt.title("Purchase Conversion Rate by Group")
    plt.xlabel("Group")
    plt.ylabel("Purchase Conversion Rate")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "purchase_conversion_rate_summary.png", dpi=150)
    plt.close()

    print("Analysis complete. Check the outputs folder.")
    print(summary[["group", "purchase_conversion_rate", "cost_per_purchase"]])
    print(results)


if __name__ == "__main__":
    main()
