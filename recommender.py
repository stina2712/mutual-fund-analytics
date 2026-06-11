import pandas as pd

def get_fund_recommendations(risk_appetite):
    # 1. Load performance data
    df_perf = pd.read_csv('07_scheme_performance.csv')
    
    # 2. Filter by risk grade (assuming column is named 'risk_grade')
    recommended = df_perf[df_perf['risk_grade'] == risk_appetite]
    
    # 3. Sort by Sharpe Ratio and return top 3
    top_3 = recommended.sort_values(by='sharpe_ratio', ascending=False).head(3)
    
    return top_3[['amfi_code', 'scheme_name', 'sharpe_ratio']]

# Example usage:
print(get_fund_recommendations('Moderate'))