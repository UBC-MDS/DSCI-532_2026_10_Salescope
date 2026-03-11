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
):
    """
    Build a filtered ibis query that runs inside DuckDB.
    This will later replace pandas filtering in the dashboard.
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

    return t

def execute_filtered_query(**filters):
    """
    Run the filtered ibis query and return a pandas DataFrame.
    """
    return build_filtered_query(**filters).execute()