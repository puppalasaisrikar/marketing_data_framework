import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_complex_marketing_data():
    
    np.random.seed(42)
    base_date = datetime(2024, 1, 1)
    rows_per_source = 500
    
    # --- SOURCE 1: GOOGLE ADS (Clean-ish, but different naming) ---
    google_data = pd.DataFrame({
        'Date': [base_date + timedelta(days=i%30) for i in range(rows_per_source)],
        'Campaign': [f"G_Search_Brand_{i%5}" for i in range(rows_per_source)],
        'Cost': np.random.uniform(100, 1000, rows_per_source),
        'Imps': np.random.randint(5000, 20000, rows_per_source),
        'Clicks': np.random.randint(100, 1000, rows_per_source),
        'Currency': 'USD'
    })

    # --- SOURCE 2: META (The Global/Currency Headache) ---
    meta_data = pd.DataFrame({
        'date': [base_date + timedelta(days=i%30) for i in range(rows_per_source)],
        'campaign_name': [f"FB_Video_Awareness_{i%3}" for i in range(rows_per_source)],
        'amount_spent': np.random.uniform(50, 800, rows_per_source),
        'impressions': np.random.randint(1000, 15000, rows_per_source),
        'clicks': np.random.randint(50, 500, rows_per_source),
        'currency': np.random.choice(['USD', 'EUR', 'GBP'], rows_per_source)
    })

    # --- SOURCE 3: TIKTOK (The Logic & Anomaly Headache) ---
    tiktok_data = pd.DataFrame({
        'day': [base_date + timedelta(days=i%30) for i in range(rows_per_source)],
        'tk_campaign': [f"TT_Influencer_{i%2}" for i in range(rows_per_source)],
        'spend_total': np.random.uniform(200, 2000, rows_per_source),
        'view_count': np.random.randint(10000, 50000, rows_per_source),
        'click_count': np.random.randint(200, 2000, rows_per_source),
        'currency': 'USD'
    })


    

    tiktok_data.loc[0:10, 'view_count'] = 0  # Spend/Clicks > 0 but 0 Views
    

    google_data.loc[250, 'Cost'] = 95000.00  # Massive outlier for one day
    

    meta_data.loc[100:110, 'amount_spent'] = np.nan # Missing spend records
    
    return google_data, meta_data, tiktok_data

# Generate the raw assets
google_raw, meta_raw, tiktok_raw = generate_complex_marketing_data()


google_raw.to_csv("google_ads_raw.csv", index=False)
meta_raw.to_csv("meta_ads_raw.csv", index=False)
tiktok_raw.to_csv("tiktok_ads_raw.csv", index=False)
