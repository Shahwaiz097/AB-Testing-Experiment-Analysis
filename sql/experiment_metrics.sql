
SELECT
    campaign_name,
    SUM(spend_usd) AS total_spend,
    SUM(impressions) AS total_impressions,
    SUM(website_clicks) AS total_clicks,
    SUM(add_to_cart) AS total_add_to_cart,
    SUM(purchase) AS total_purchases,
    SUM(purchase) * 1.0 / SUM(website_clicks) AS purchase_conversion_rate,
    SUM(website_clicks) * 1.0 / SUM(impressions) AS click_through_rate,
    SUM(spend_usd) * 1.0 / SUM(purchase) AS cost_per_purchase
FROM campaign_data
GROUP BY campaign_name;