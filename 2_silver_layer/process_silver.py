import pandas as pd
import os

def process_silver_data(bronze_path, silver_path):
    print("[*] Starting Silver Layer processing...")
    
    # 1. Read Bronze Data
    try:
        df = pd.read_csv(bronze_path)
        print(f"[*] Initial shape: {df.shape}")
    except Exception as e:
        print(f"[!] Error reading Bronze data: {e}")
        return
        
    # 2. Data Cleaning
    # Drop the useless 'Unnamed: 0' column
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        print("[*] Dropped 'Unnamed: 0' column.")
        
    # 3. Feature Engineering (Transformations)
    # Split 'source_file' into 'city' and 'day_type'
    # Example: "amsterdam_weekdays" -> city: "amsterdam", day_type: "weekdays"
    if 'source_file' in df.columns:
        df[['city', 'day_type']] = df['source_file'].str.split('_', expand=True)
        df = df.drop(columns=['source_file'])
        print("[*] Extracted 'city' and 'day_type' from source_file.")
        
    # 4. Remove Duplicates
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        df = df.drop_duplicates()
        print(f"[*] Removed {duplicates_count} duplicate rows.")
    else:
        print("[*] No duplicate rows found.")
        
    # 5. Save to Silver Layer
    try:
        df.to_csv(silver_path, index=False)
        print(f"[+] Silver layer cleaning complete! Final Shape: {df.shape}")
        print(f"[+] Data saved to: {silver_path}")
    except Exception as e:
        print(f"[!] Error saving to Silver layer: {e}")

if __name__ == "__main__":
    # Define paths (pointing to the Bronze layer output)
    BRONZE_FILE = os.path.join("..", "1_bronze_layer", "bronze_airbnb_data.csv")
    SILVER_FILE = "silver_airbnb_cleaned.csv"
    
    process_silver_data(BRONZE_FILE, SILVER_FILE)