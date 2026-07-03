# A/B Test Decision Memo

## Objective

The objective of this analysis was to determine whether the test marketing campaign improved purchase conversion compared with the control campaign.

## Primary Metric

The primary metric was purchase conversion rate:

purchase conversion rate = purchases / website clicks

## Data Quality

The dataset included daily campaign-level metrics for control and test campaigns.
One control row contained missing values and was removed before analysis.

## Results

The control campaign achieved a purchase conversion rate of approximately 9.83%.
The test campaign achieved a purchase conversion rate of approximately 8.64%.

Although the test campaign generated more total purchases, it also generated more clicks and spend.
The lower conversion rate suggests that the test campaign attracted less qualified traffic.

## Statistical Test

A two-proportion z-test was used to compare purchase conversion rates between groups.
Confidence intervals were calculated for the difference in conversion rates.

## Business Interpretation

The test campaign increased volume but reduced conversion efficiency.
From a business perspective, this means the campaign may be useful for awareness or traffic generation,
but it does not clearly improve conversion quality.

## Recommendation

Do not fully ship the test campaign yet.

Recommended next steps:
1. Continue testing with audience or creative refinements.
2. Monitor cost per purchase as a guardrail metric.
3. Run a follow-up experiment with user-level randomization if possible.
