import pandas as pd
import numpy as np
import os

# Ensure the processed folder exists
os.makedirs("data/processed", exist_ok=True)

print("Starting Day 2 Data Cleaning Pipeline...\n")

# =====================================================================
# 1. CLEANING 02_nav_history.csv
# =====================================================================
print("Cleaning 02_nav_history.csv...")
nav_path = "data/raw/02_nav_history.csv"

if os.path.exists(nav_path):
    nav_df = pd.read_csv(nav_path)
    nav_df['date'] = pd.to_datetime(nav_df['date'])
    nav_df = nav_df.drop_duplicates(subset=['amfi_code', 'date'])
    nav_df = nav_df[nav_df['nav'] > 0]
    nav_df = nav_df.sort_values(by=['amfi_code', 'date'])
    nav_df['nav'] = nav_df.groupby('amfi_code')['nav'].ffill()
    nav_df.to_csv("data/processed/nav_history_clean.csv", index=False)
    print(f"✔ nav_history cleaned. Shape: {nav_df.shape}")
else:
    print("⚠ nav_history_clean.csv already generated or raw file skipped.")


# =====================================================================
# 2. CLEANING 08_investor_transactions.csv
# =====================================================================
print("\nCleaning 08_investor_transactions.csv...")
tx_path = "data/raw/08_investor_transactions.csv"
tx_df = pd.read_csv(tx_path)

# Standardize column names: Strip whitespace and convert to lowercase for uniform tracking
print(f"   -> Original columns found: {list(tx_df.columns)}")
tx_df.columns = tx_df.columns.str.strip().str.lower()
print(f"   -> Standardized columns: {list(tx_df.columns)}")

# Dynamically identify the transaction date column
date_col = [col for col in tx_df.columns if 'date' in col][0]
tx_df[date_col] = pd.to_datetime(tx_df[date_col])

# Dynamically identify the type column
type_col = [col for col in tx_df.columns if 'type' in col][0]
tx_df[type_col] = tx_df[type_col].astype(str).str.strip().str.upper()
type_map = {'SIP': 'SIP', 'LUMPSUM': 'Lumpsum', 'REDEMPTION': 'Redemption', 'PURCHASE': 'Lumpsum'}
tx_df[type_col] = tx_df[type_col].map(type_map).fillna('Lumpsum')

# Dynamically identify the amount column to prevent KeyErrors
amt_col = [col for col in tx_df.columns if 'amount' in col or 'amt' in col][0]
print(f"   -> Mapping tracking column '{amt_col}' as target transaction value.")

# Validate value criteria
tx_df = tx_df[tx_df[amt_col] > 0]

# Dynamically identify and clean KYC status
kyc_cols = [col for col in tx_df.columns if 'kyc' in col]
if kyc_cols:
    tx_df[kyc_cols[0]] = tx_df[kyc_cols[0]].astype(str).str.strip().str.capitalize()

# Restore standard submission names for the output CSV column headers
tx_df = tx_df.rename(columns={amt_col: 'amount', date_col: 'transaction_date', type_col: 'transaction_type'})

tx_df.to_csv("data/processed/investor_transactions_clean.csv", index=False)
print(f"✔ investor_transactions cleaned. Shape: {tx_df.shape}")


# =====================================================================
# 3. CLEANING 07_scheme_performance.csv
# =====================================================================
print("\nCleaning 07_scheme_performance.csv...")
perf_path = "data/raw/07_scheme_performance.csv"
perf_df = pd.read_csv(perf_path)

# Standardize column strings
perf_df.columns = perf_df.columns.str.strip().str.lower()

# Coerce return metrics to numeric values
return_cols = [col for col in perf_df.columns if 'return' in col]
for col in return_cols:
    perf_df[col] = pd.to_numeric(perf_df[col], errors='coerce').fillna(0.0)

# Clean and filter the expense ratio column safely
exp_col = [col for col in perf_df.columns if 'expense' in col or 'ratio' in col][0]
perf_df[exp_col] = pd.to_numeric(perf_df[exp_col], errors='coerce')
perf_df = perf_df[(perf_df[exp_col] >= 0.1) & (perf_df[exp_col] <= 2.5)]
perf_df = perf_df.rename(columns={exp_col: 'expense_ratio'})

perf_df.to_csv("data/processed/scheme_performance_clean.csv", index=False)
print(f"✔ scheme_performance cleaned. Shape: {perf_df.shape}")


# =====================================================================
# 4. BATCH PROCESSING REMAINING FILES
# =====================================================================
print("\nBatch processing remaining support files...")
already_processed = ['02_nav_history.csv', '08_investor_transactions.csv', '07_scheme_performance.csv']

for file_name in os.listdir("data/raw"):
    if file_name.endswith('.csv') and file_name not in already_processed:
        print(f"-> Processing: {file_name}")
        df = pd.read_csv(f"data/raw/{file_name}")
        df = df.drop_duplicates()
        
        # Format the name safely to 'filename_clean.csv'
        clean_name = file_name
        if clean_name[:2].isdigit() and clean_name[2] == '_':
            clean_name = clean_name[3:]
        clean_name = clean_name.replace("_raw.csv", ".csv").replace(".csv", "_clean.csv")
        
        df.to_csv(f"data/processed/{clean_name}", index=False)

print("\n🎉 All datasets successfully cleaned and saved to data/processed/")