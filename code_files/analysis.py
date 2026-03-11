import pandas as pd
import numpy as np

google_raw = pd.read_csv("google_ads_raw.csv")
meta_raw = pd.read_csv("meta_ads_raw.csv")
tiktok_raw = pd.read_csv("tiktok_ads_raw.csv")

class Marketing_Ingestor:
    def __init__(self):
        self.mappings = {
            'google': {'date': 'date', 'campaign': 'campaign', 'cost': 'spend', 'imps': 'impressions', 'clicks': 'clicks', 'currency': 'currency'},
            'meta': {'date': 'date', 'campaign_name': 'campaign', 'amount_spent': 'spend', 'impressions': 'impressions', 'clicks': 'clicks', 'currency': 'currency'},
            'tiktok': {'day': 'date', 'tk_campaign': 'campaign', 'spend_total': 'spend', 'view_count': 'impressions', 'click_count': 'clicks', 'currency': 'currency'}
        }
        # Exchange rates to USD
        self.exchange_rates = {'USD': 1.0, 'EUR': 1.08, 'GBP': 1.27}

    def process_source(self, df, source_name):
        """Standardizes and cleans individual source files with strict schema enforcement."""
        
        # 1. IMMEDIATE NORMALIZATION: Lowercase all column names to fix 'Currency' vs 'currency'
        df.columns = [c.lower() for c in df.columns]
        
        # 2. SCHEMA MAPPING: Rename based on our source-specific dictionary
        df = df.rename(columns=self.mappings[source_name])
        
        # 3. TYPE CONVERSION: Ensure numeric columns are actually numbers (vital for real CSVs)
        numeric_cols = ['spend', 'impressions', 'clicks']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 4. CURRENCY NORMALIZATION: Create a 'spend_usd' column for unified analysis
        # We use .upper() to ensure 'usd' or 'USD' both work
        df['spend_usd'] = df.apply(
            lambda x: x['spend'] * self.exchange_rates.get(str(x['currency']).upper(), 1.0), 
            axis=1
        )
        
        # 5. METADATA: Track source and validation status
        df['source_platform'] = source_name
        df['is_valid_logic'] = ~((df['spend_usd'] > 0) & (df['impressions'] == 0))
        
        # Keep only the standardized columns to ensure a clean concat
        final_cols = ['date', 'campaign', 'spend_usd', 'impressions', 'clicks', 'currency', 'source_platform', 'is_valid_logic']
        return df[final_cols]


# Let's run the Ingestion
ingestor = Marketing_Ingestor()

# Processing our 3 raw files
google_processed = ingestor.process_source(google_raw, 'google')
meta_processed = ingestor.process_source(meta_raw, 'meta')
tiktok_processed = ingestor.process_source(tiktok_raw, 'tiktok')

# Combine them into one "Master Marketing Table"
master_df = pd.concat([google_processed, meta_processed, tiktok_processed], ignore_index=True)


pd.set_option('display.max_columns', None)
print(master_df.head())


# ANomaly Detection
from sklearn.ensemble import IsolationForest

def detect_spend_anomalies(df):
    # We only look at 'spend_usd' for this model
    model = IsolationForest(contamination=0.01, random_state=42) # Assuming ~1% of data is anomalous
    
    # Fit the model on the spend column
    df['anomaly_score'] = model.fit_predict(df[['spend_usd']])
    
    # -1 indicates an anomaly, 1 indicates normal
    anomalies = df[df['anomaly_score'] == -1]
    
    return anomalies

# Execute Detection
flagged_spend = detect_spend_anomalies(master_df)

print(f"Total Anomalies Detected: {len(flagged_spend)}")
print("Top 3 Flagged Outliers:")
print(flagged_spend[['date', 'source_platform', 'spend_usd']].sort_values(by='spend_usd', ascending=False).head(3))

def generate_growthos_report(df, anomalies_df):
    # 1. High-Level Metrics
    total_records = len(df)
    integrity_score = (df['is_valid_logic'].sum() / total_records) * 100
    total_spend = df['spend_usd'].sum()
    anomaly_count = len(anomalies_df)
    
    print("\n" + "="*50)
    print(" Marketing Data Framework REPORT ")
    print("="*50)
    print(f"Total Records Processed:  {total_records:,}")
    print(f"Unified Spend (USD):      ${total_spend:,.2f}")
    print(f"Data Integrity Score:     {integrity_score:.2f}%")
    print(f"Anomalies Detected:       {anomaly_count}")
    print("-" * 50)
    
    # 2. Critical Findings
    print("\n[CRITICAL ACTION ITEMS]")
    
    # Logic Errors (Ghost Impressions)
    logic_errors = df[~df['is_valid_logic']]
    if not logic_errors.empty:
        print(f"LOGIC ERROR: {len(logic_errors)} rows found with Spend but 0 Impressions.")
        print(f"Context: Mostly identified in {logic_errors['source_platform'].unique()} data.")
    
    # Statistical Outliers 
    if not anomalies_df.empty:
        top_spike = anomalies_df.sort_values(by='spend_usd', ascending=False).iloc[0]
        print(f"SPEND ANOMALY: Major ${top_spike['spend_usd']:,.2f} spike detected.")
        print(f"Context: Found in {top_spike['source_platform']} on {top_spike['date']}.")

    # 3. Final Recommendation
    print("\n[ONBOARDING STATUS]")
    if integrity_score > 98 and anomaly_count < (total_records * 0.01):
        print("STATUS: READY FOR GROWTHOS MODELING")
    else:
        print("STATUS: PENDING DATA QUALITY REVIEW")
        print("Required: Validate TikTok pixels and Google Ads budget spikes.")
    print("="*50 + "\n")


generate_growthos_report(master_df, flagged_spend)


















































