import pandas as pd
import os

def build_gold_layer(cleaned_data_path, enrichment_data_path, gold_fact_path, gold_summary_path):
    print("[*] Starting Gold Layer processing (Data Warehouse construction)...")
    
    # 1. Load Silver Data
    try:
        fact_df = pd.read_csv(cleaned_data_path)
        dim_city_df = pd.read_csv(enrichment_data_path)
        print(f"[*] Loaded Cleaned Data: {fact_df.shape}")
        print(f"[*] Loaded Enrichment Data: {dim_city_df.shape}")
    except Exception as e:
        print(f"[!] Error loading Silver data: {e}")
        return
        
    # 2. Join (Merge) Fact and Dimension tables (Star Schema concept)
    try:
        # We do a LEFT JOIN to keep all our fact records even if a city wasn't scraped
        gold_df = pd.merge(fact_df, dim_city_df, on='city', how='left')
        print(f"[*] Joined Data Shape: {gold_df.shape}")
    except Exception as e:
        print(f"[!] Error merging data: {e}")
        return
        
    # 3. Create Business Aggregations (Data Marts)
    print("[*] Creating Business Summary Metrics...")
    # Example: Average Price (realSum) and Satisfaction by City and Room Type
    summary_df = gold_df.groupby(['city', 'room_type']).agg(
        avg_price=('realSum', 'mean'),
        avg_satisfaction=('guest_satisfaction_overall', 'mean'),
        total_listings=('realSum', 'count')
    ).reset_index()
    
    # Round the numbers for clean reporting
    summary_df = summary_df.round(2)
    
    # 4. Save Gold Tables
    try:
        gold_df.to_csv(gold_fact_path, index=False)
        summary_df.to_csv(gold_summary_path, index=False)
        print(f"[+] Gold Fact Table saved to: {gold_fact_path}")
        print(f"[+] Gold Summary Table saved to: {gold_summary_path}")
        print("[+] GOLD LAYER COMPLETE! 🏆")
    except Exception as e:
        print(f"[!] Error saving Gold data: {e}")

if __name__ == "__main__":
    # Paths pointing to the Silver layer output
    CLEANED_SILVER = os.path.join("..", "2_silver_layer", "silver_airbnb_cleaned.csv")
    ENRICHED_SILVER = os.path.join("..", "2_silver_layer", "silver_city_enrichment.csv")
    
    # Output paths for Gold layer
    GOLD_FACT = "gold_fact_airbnb.csv"
    GOLD_SUMMARY = "gold_summary_metrics.csv"
    
    build_gold_layer(CLEANED_SILVER, ENRICHED_SILVER, GOLD_FACT, GOLD_SUMMARY)