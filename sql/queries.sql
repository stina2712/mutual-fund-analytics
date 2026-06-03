-- sql/queries.sql

-- 1. Top 5 funds by Total Assets Under Management (AUM)
SELECT amfi_code, fund_house, category, sub_category 
FROM dim_fund 
ORDER BY amfi_code DESC LIMIT 5;

-- 2. Average NAV per month per fund scheme
SELECT amfi_code, strftime('%Y-%m', date) as nav_month, AVG(nav) as avg_nav
FROM fact_nav
GROUP BY amfi_code, nav_month;

-- 3. Systematic Investment Plan (SIP) Volume
SELECT strftime('%Y', transaction_date) as tx_year, SUM(amount) as total_sip_volume
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY tx_year;

-- 4. Transactions by State location
SELECT state, COUNT(*) as total_transactions, SUM(amount) as total_volume_inr
FROM fact_transactions
GROUP BY state 
ORDER BY total_volume_inr DESC;

-- 5. Cost-Efficient Selections: Cost metrics filter
SELECT amfi_code, expense_ratio
FROM fact_performance
WHERE expense_ratio < 1.5;

-- 6. Total Capital Redemptions vs Inflows
SELECT transaction_type, SUM(amount) as net_amount_inr 
FROM fact_transactions 
GROUP BY transaction_type;

-- 7. High-Risk Asset Product Counts
SELECT risk_grade, COUNT(*) as fund_count 
FROM dim_fund 
GROUP BY risk_grade;

-- 8. Non-Compliant/Pending User Transaction Risk Pools
SELECT kyc_status, SUM(amount) as exposed_volume_inr 
FROM fact_transactions 
GROUP BY kyc_status;

-- 9. Maximum Historical Valuation peaks reached per Asset
SELECT amfi_code, MAX(nav) as historical_peak 
FROM fact_nav 
GROUP BY amfi_code;

-- 10. City Tier Distribution metrics
SELECT city_tier, COUNT(*) as transaction_count
FROM fact_transactions
GROUP BY city_tier;