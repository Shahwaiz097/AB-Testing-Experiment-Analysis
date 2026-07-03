# A/B Testing Experiment Analysis

A simple A/B testing project comparing a **control campaign** with a **test campaign**.

The goal is to check whether the test campaign improved purchase conversion.

## Project Structure

```text
AB-Testing-Experiment-Analysis/
├── data/
│   ├── control_group.csv
│   ├── test_group.csv
│   └── combined_clean_campaign_data.csv
├── models/
│   └── README.md
├── notebooks/
│   └── experiment_analysis.ipynb
├── outputs/
│   ├── campaign_summary.csv
│   ├── statistical_test_results.csv
│   ├── power_analysis_results.csv
│   ├── missing_values_report.csv
│   ├── decision_memo.md
│   ├── experiment_metrics.sql
│   └── charts
├── src/
│   ├── analyze_ab_test.py
│   ├── stats_tests.py
│   ├── power_analysis.py
│   └── validate.py
├── README.md
└── requirements.txt
```

## Dataset

The project uses daily marketing campaign data for two groups:

- Control campaign
- Test campaign

Each file includes spend, impressions, reach, website clicks, searches, view content events, add-to-cart events, and purchases.

## Primary Metric

```text
purchase conversion rate = purchases / website clicks
```

## What Was Added

This project includes the key missing parts needed for a proper A/B testing portfolio project:

- Data validation
- Missing-value report
- Clean combined dataset
- Purchase conversion rate
- Two-proportion z-test
- Confidence interval
- Power analysis
- Guardrail metrics such as cost per purchase and click-through rate
- Visualizations
- SQL metrics query
- Business decision memo

## Main Results

| Group | Purchase Conversion Rate | Cost per Purchase |
|---|---:|---:|
| Control | 9.83% | $4.41 |
| Test | 8.64% | $4.92 |

The test campaign generated more total purchases, but it had a lower purchase conversion rate than the control campaign.

## Statistical Test

A two-proportion z-test was used to compare purchase conversion rates.

| Metric | Value |
|---|---:|
| Control conversion rate | 9.83% |
| Test conversion rate | 8.64% |
| Difference, test - control | -1.18% |
| Relative lift | -12.06% |
| p-value | 2.463e-32 |
| 95% CI lower | -1.38% |
| 95% CI upper | -0.99% |

## Business Recommendation

Do not fully roll out the test campaign yet.

The test campaign increased traffic and total purchases, but it reduced conversion efficiency. It should be optimized and tested again before a full launch.

## How to Run

Install requirements:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python src/analyze_ab_test.py
```

The results will be saved in the `outputs/` folder.

## Tools Used

- Python
- pandas
- matplotlib
- statsmodels
- SQL
- Jupyter Notebook
