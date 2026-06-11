import sqlite3
import pandas as pd

def get_fund_recommendations(risk_appetite):
    conn = sqlite3.connect('bluestock_mf.db')
    
    query = f"""
    SELECT d.amfi_code, d.scheme_name, p.sortino_ratio
    FROM dim_fund d
    JOIN fact_performance p ON d.amfi_code = p.amfi_code
    WHERE p.risk_grade = '{risk_appetite}'
    ORDER BY p.sortino_ratio DESC
    LIMIT 3
    """
    
    top_3 = pd.read_sql_query(query, conn)
    conn.close()
    return top_3

# Printing the tables for all risk levels
for risk in ['Low', 'Moderate', 'High']:
    df = get_fund_recommendations(risk)
    print(f"\n--- Top 3 Funds for {risk} Risk Appetite ---")
    # Using 'pretty' formatting with tabulate
    print(df.to_string(index=False))