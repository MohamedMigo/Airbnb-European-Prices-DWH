import pandas as pd
import os
import glob

def load_to_bronze(source_folder, bronze_target_path):
    """
    Reads multiple raw CSV files from a folder, combines them, 
    and loads them into the Bronze layer as a single file.
    """
    print(f"[*] Starting ingestion from folder: {source_folder}")
    
    # 1. Check if the folder exists
    if not os.path.exists(source_folder):
        print("[!] Error: Raw data folder not found. Check the path.")
        return

    # 2. Get all CSV files in the folder
    csv_files = glob.glob(os.path.join(source_folder, "*.csv"))
    
    if not csv_files:
        print("[!] Error: No CSV files found inside the folder.")
        return
        
    print(f"[*] Found {len(csv_files)} CSV files. Combining them now...")
    
    # 3. Read and combine all files
    df_list = []
    for file in csv_files:
        try:
            temp_df = pd.read_csv(file)
            # Add a column to know which city/file this data came from
            file_name = os.path.basename(file).replace('.csv', '')
            temp_df['source_file'] = file_name 
            df_list.append(temp_df)
        except Exception as e:
            print(f"[!] Error reading {file}: {e}")
            
    # 4. Concatenate into one massive DataFrame
    try:
        raw_df = pd.concat(df_list, ignore_index=True)
        print(f"[*] Successfully combined data. Total Shape: {raw_df.shape}")
    except Exception as e:
        print(f"[!] Error combining data: {e}")
        return

    # 5. Save the combined data to the Bronze layer
    try:
        raw_df.to_csv(bronze_target_path, index=False)
        print(f"[+] Bronze layer ingestion complete! Data saved to: {bronze_target_path}")
    except Exception as e:
        print(f"[!] Error saving to Bronze layer: {e}")

if __name__ == "__main__":
    # Pointing to the folder that contains all the city CSVs
    RAW_DATA_FOLDER = os.path.join("..", "raw_data", "airbnb_prices.csv") 
    BRONZE_OUTPUT_FILE = "bronze_airbnb_data.csv"
    
    # Execute the ingestion process
    load_to_bronze(RAW_DATA_FOLDER, BRONZE_OUTPUT_FILE)