```python
   import os
   import pandas as pd
   import glob

   def setup_folder_hierarchy():
       folders = ["data/raw", "data/processed", "notebooks", "sql", "dashboard", "reports"]
       for folder in folders:
           os.makedirs(folder, exist_ok=True)
       print("✓ Folder structure verified.")

   def profile_local_datasets():
       print("\n--- Profiling Local Datasets ---")
       csv_files = glob.glob("data/raw/*_raw.csv")
       if not csv_files:
           print("No CSV files found in data/raw yet.")
           return
       for file in csv_files:
           df = pd.read_csv(file)
           print(f"File: {os.path.basename(file)} | Shape: {df.shape} | Columns: {list(df.columns)}")

   if __name__ == "__main__":
       setup_folder_hierarchy()
       profile_local_datasets()