import os
import pandas as pd
import glob

def setup_folder_hierarchy():
    """Creates the required project folder structure."""
    folders = ["data/raw", "data/processed", "notebooks", "sql", "dashboard", "reports"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    print("✓ Folder structure verified.")

def profile_local_datasets():
    """Profiles the shapes of raw data files."""
    print("\n--- Profiling Local Datasets ---")
    csv_files = glob.glob("data/raw/*.csv")
    if not csv_files:
        print("No CSV files found in data/raw yet.")
        return
    for file in csv_files:
        df = pd.read_csv(file)
        print(f"File: {os.path.basename(file)} | Shape: {df.shape}")

def explore_fund_master(fund_master_path):
    """Explores unique fund houses, categories, sub-categories, and risk grades."""
    print("\n--- Exploring Fund Master Metadata ---")
    if not os.path.exists(fund_master_path):
        print(f"⚠ fund_master.csv not found at {fund_master_path}. skipping exploration.")
        return
        
    df = pd.read_csv(fund_master_path)
    
    # Dynamically find columns even if case-sensitive variations exist
    col_mapping = {col.lower().replace("_", "").replace(" ", ""): col for col in df.columns}
    
    target_fields = {
        'fundhouse': 'Fund Houses',
        'category': 'Categories',
        'subcategory': 'Sub-Categories',
        'riskgrade': 'Risk Grades'
    }
    
    for key, label in target_fields.items():
        matched_col = None
        for col_clean in col_mapping:
            if key in col_clean:
                matched_col = col_mapping[col_clean]
                break
        
        if matched_col:
            unique_vals = df[matched_col].dropna().unique()
            print(f"\nUnique {label} count: {len(unique_vals)}")
            print(f"Sample values: {list(unique_vals)[:5]}")
        else:
            print(f"⚠ Could not find a column matching '{label}' in Fund Master.")

if __name__ == "__main__":
    setup_folder_hierarchy()
    profile_local_datasets()
    
    # ALERT: Make sure 'fund_master.csv' is saved in your data/raw/ folder!
    explore_fund_master("data/raw/fund_master.csv")