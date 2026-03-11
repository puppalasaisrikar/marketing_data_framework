# Marketing Data Framework: Multi-Source Ingestion & Audit Engine

An enterprise-grade Python framework designed to unify fragmented marketing data from various platforms (Google, Meta, TikTok) into a standardized, audit-ready schema. This tool automates the data solutions pipeline by handling multi-currency normalization, identifying marketing logic failures, and using Machine Learning to detect spend anomalies.



## Key Features

* **Unified Ingestion Engine:** Automates the mapping of inconsistent schemas across major advertising platforms (e.g., mapping Google's "Cost" and Meta's "Amount Spent" to a single "Spend" metric).
* **Global Currency Normalization:** Handles multi-region data by converting diverse currencies (EUR, GBP, USD) into a unified base currency for accurate cross-platform analysis.
* **Integrity Auditing (Marketing Physics):** Identifies "Ghost Impressions" impossible data states where spend or clicks exist despite zero impressions, indicating broken tracking pixels or API desyncs.

* **ML-Powered Anomaly Detection:** Utilizes the **Isolation Forest** algorithm to automatically flag statistical spend irregularities that bypass standard rule-based filters.
* **Executive Diagnostic Reporting:** Translates technical data quality metrics into an "Onboarding Readiness" summary with actionable stakeholder recommendations.

## Technical Stack

* **Language:** Python 3.x
* **Data Wrangling:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (Isolation Forest)
* **Visualization:** Matplotlib, Seaborn

## How it Works

The framework follows a four-stage pipeline:

1.  **Ingestion:** Reads raw CSV exports from disparate marketing platforms.
2.  **Transformation:** Normalizes column headers, lowercases schemas, and enforces numeric types for production-ready data.
3.  **Validation:** Runs a battery of logic tests (e.g., Spend vs. Impressions) and calculates a **Data Integrity Score**.
4.  **Anomaly Detection:** Trains an Isolation Forest model on the unified spend data to highlight outliers and operational risks.


## Example Output: Onboarding Readiness Report

```text
==================================================
        MARKETING DATA INTEGRITY REPORT          
==================================================
Total Records Processed:  1,500
Unified Spend (USD):      $142,350.42
Data Integrity Score:     98.80%
ML-Flagged Anomalies:     15
--------------------------------------------------

[CRITICAL ACTION ITEMS]
 LOGIC ERROR: 11 rows found with Spend but 0 Impressions.
 Context: Identified in TikTok data.
 SPEND ANOMALY: Major $95,000.00 spike detected.
 Context: Found in Google Ads on 2024-01-11.

[ONBOARDING STATUS]
 STATUS: PENDING DATA QUALITY REVIEW
 Required: Validate TikTok pixels and Google Ads budget spikes.
==================================================
