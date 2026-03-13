import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/sales_and_customer_insights.csv")
OUT_PATH = Path("data/processed/sales_and_customer_insights.parquet")

def main():
    df = pd.read_csv(RAW_PATH, parse_dates=True)

    df["risk_value"] = df["Lifetime_Value"] * df["Churn_Probability"]
    df["Launch_Date"] = pd.to_datetime(df["Launch_Date"], format="%Y-%m-%d")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(OUT_PATH, index=False)

    print(f"Saved processed dataset to {OUT_PATH}")
    print(f"Shape: {df.shape}")

if __name__ == "__main__":
    main()