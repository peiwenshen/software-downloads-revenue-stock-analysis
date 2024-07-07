# software-downloads-revenue-stock-analysis

## Introduction

This project analyzes the relationship between software package downloads, the revenue of the corresponding companies, and their stock prices. By examining these variables, we aim to uncover patterns and insights that can inform business decisions and investment strategies.

Result could be found on my [Medium](https://medium.com/@k3232908/analyzing-the-relationship-between-python-package-downloads-revenue-and-stock-price-cd1171822fdb).

## Data Sources

The data for this analysis was obtained from the following sources:

1. **PyPI Downloads**: The download counts for each software package were retrieved from PyPI (Python Package Index) using BigQuery. The query aggregates monthly download counts for each package.

2. **Quarterly Revenue**: The revenue data for each company was collected from their quarterly financial reports available through Yahoo Finance.

3. **Stock Prices**: The historical stock prices were also retrieved from Yahoo Finance.

## BigQuery SQL Query

To retrieve the download counts from PyPI using BigQuery, use the following SQL query. This example fetches the download counts for the 'stripe' package for the last 18 months:

```sql
#standardSQL
SELECT
  COUNT(*) AS num_downloads,
  DATE_TRUNC(DATE(timestamp), MONTH) AS `month`
FROM `bigquery-public-data.pypi.file_downloads`
WHERE
  file.project = 'stripe'
  -- Only query the last 18 months of history
  AND DATE(timestamp)
    BETWEEN DATE_TRUNC(DATE_SUB(CURRENT_DATE(), INTERVAL 18 MONTH), MONTH)
    AND CURRENT_DATE()
GROUP BY `month`
ORDER BY `month` DESC
```
## Analysis

The script main.py performs the following steps:
1.	Load JSON Data: Load the monthly download counts from the JSON files.
2.	Fetch Stock Data: Retrieve historical stock prices from Yahoo Finance.
3.	Fetch Revenue Data: Retrieve quarterly revenue data from Yahoo Finance.
4.	Plot Data: Generate plots showing the relationships between downloads, revenue, and stock prices for each company.

## Findings

The analysis includes companies like Confluent, MongoDB, Datadog, Snowflake, Elasticsearch, and Twilio. 
And find a positive correlation between the number of downloads and quarterly revenue.

## Conclusion

This project highlights the interconnectedness of software usage, financial performance, and market valuation. By analyzing these relationships, companies can better understand the impact of their software products on their overall success, and investors can make more informed decisions.