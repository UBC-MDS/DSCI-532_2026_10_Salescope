import ibis
from pathlib import Path

DATA_PATH = Path("data/processed/sales_and_customer_insights.parquet")

con = ibis.duckdb.connect()

def get_base_table():
    """
    Returns the base ibis table connected to the parquet dataset.
    """
    return con.read_parquet(DATA_PATH)


def get_base_dataframe():
    """
    Convenience helper to return the full dataset as a pandas DataFrame.
    Useful for quick tests or compatibility with existing code.
    """
    return get_base_table().execute()

def build_filtered_query(
    churn_min=None,
    churn_max=None,
    clv_min=None,
    clv_max=None,
    order_min=None,
    order_max=None,
    freq_min=None,
    freq_max=None,
    date_start=None,
    date_end=None,
    types=None,
    regions=None,
    strategies=None,
):
    """
    Build a filtered ibis query that applies dashboard filters in DuckDB
    before materializing the result into a pandas DataFrame.
    """

    t = get_base_table()

    if churn_min is not None:
        t = t.filter(t.Churn_Probability >= churn_min)

    if churn_max is not None:
        t = t.filter(t.Churn_Probability <= churn_max)

    if clv_min is not None:
        t = t.filter(t.Lifetime_Value >= clv_min)

    if clv_max is not None:
        t = t.filter(t.Lifetime_Value <= clv_max)

    if order_min is not None:
        t = t.filter(t.Average_Order_Value >= order_min)

    if order_max is not None:
        t = t.filter(t.Average_Order_Value <= order_max)

    if freq_min is not None:
        t = t.filter(t.Purchase_Frequency >= freq_min)

    if freq_max is not None:
        t = t.filter(t.Purchase_Frequency <= freq_max)

    if date_start is not None:
        t = t.filter(t.Launch_Date >= date_start)

    if date_end is not None:
        t = t.filter(t.Launch_Date <= date_end)

    if types:
        t = t.filter(t.Most_Frequent_Category.isin(types))

    if regions:
        t = t.filter(t.Region.isin(regions))

    if strategies:
        t = t.filter(t.Retention_Strategy.isin(strategies))

    return t

def execute_filtered_query(**filters):
    """
    Run the filtered ibis query and return a pandas DataFrame.
    """
    return build_filtered_query(**filters).execute()