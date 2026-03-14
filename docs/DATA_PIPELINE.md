# Data Pipeline

## Regenerating processed data

To regenerate the processed parquet dataset, run:

```bash
python scripts/make_parquet.py
```

This script reads:

- `data/raw/sales_and_customer_insights.csv`

and writes:

- `data/processed/sales_and_customer_insights.parquet`

It also reproduces the current dashboard preprocessing logic by:

- creating `Value_At_Risk`
- parsing `Launch_Date` as a datetime column