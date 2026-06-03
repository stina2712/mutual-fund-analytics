import pandas as pd
import sqlite3
import os

print("Starting Database Load Engine...")

# Connect to SQLite
conn = sqlite3.connect("bluestock_mf.db")

# Helper function to load cleaned tables dynamically and override safely
def load_table_to_db(csv_path, table_name):
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # if_exists='replace' automatically creates the table structure based on your clean CSV columns
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"✔ Successfully loaded {len(df)} rows into table: {table_name}")
    else:
        print(f"⚠ Warning: Cleaned file not found at {csv_path}")

# =====================================================================
# Load All Cleaned Data Sets to Database Tables
# =====================================================================

# 1. Dimension Fund Table
load_table_to_db("data/processed/fund_master_clean.csv", "dim_fund")

# 2. Fact Table: Historical NAVs
load_table_to_db("data/processed/nav_history_clean.csv", "fact_nav")

# 3. Fact Table: Investor Transactions
load_table_to_db("data/processed/investor_transactions_clean.csv", "fact_transactions")

# 4. Fact Table: Scheme Performance Metrics
load_table_to_db("data/processed/scheme_performance_clean.csv", "fact_performance")

# Close connection
conn.close()
print("\n🎉 Database loading complete! 'bluestock_mf.db' is ready for analytical queries.")