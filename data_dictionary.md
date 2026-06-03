# Mutual Fund Analytics - Data Dictionary (Day 2)

### 1. Table: dim_fund
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `amfi_code` | INTEGER (PK) | Unique identification tracking token code assigned to fund schemes. |
| `fund_house` | TEXT | Asset Management Company holding the fund asset. |
| `scheme_name` | TEXT | Public market registry label product description. |

### 2. Table: fact_nav
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `amfi_code` | INTEGER | Target identity tracker tracking fund association. |
| `date` | TEXT | Market timestamp track record calculation date. |
| `nav` | REAL | Net Asset Value pricing metrics calculation value closing index. |

### 3. Table: fact_transactions
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `investor_id` | TEXT | System user client database token hash tracking profile. |
| `amount` | REAL | Pure absolute financial volume value currency transaction asset volume. |
| `transaction_type`| TEXT | Operational type tracking filter category tag (SIP/Lumpsum/Redemption). |