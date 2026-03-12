import pandas as pd

from src.logic import normalize_range, create_summary_table, filter_sales_data

def make_test_df():
    
    return pd.DataFrame({
        "Customer_ID": [1, 2, 3, 4],
        "Region": ["Asia", "Asia", "Europe", "Europe"],
        "Most_Frequent_Category": ["Clothing", "Electronics", "Clothing", "Sports"],
        "Retention_Strategy": ["Discount", "Email Campaign", "Discount", "Loyalty Program"],
        "Lifetime_Value": [500, 1000, 1500, 2000],
        "Churn_Probability": [0.10, 0.30, 0.50, 0.80],
        "Average_Order_Value": [50, 60, 70, 80],
        "Purchase_Frequency": [2, 4, 6, 8],
        "Time_Between_Purchases": [10, 20, 30, 40],
        "Launch_Date": pd.to_datetime(["2024-01-10", "2024-02-10", "2024-03-10", "2024-04-10"]),
    })
