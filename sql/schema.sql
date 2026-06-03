-- sql/schema.sql
-- Final verified structural layout for bluestock_mf.db

CREATE TABLE dim_fund (
    amfi_code INTEGER,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

CREATE TABLE fact_nav (
    date TEXT,
    nav REAL,
    amfi_code INTEGER
);

CREATE TABLE fact_transactions (
    investor_id TEXT,
    transaction_date TEXT,
    amfi_code INTEGER,
    transaction_type TEXT,
    amount REAL,
    state TEXT,
    kyc_status TEXT
);

CREATE TABLE fact_performance (
    amfi_code INTEGER,
    expense_ratio REAL
);