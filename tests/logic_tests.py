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

def test_normalize_range_swaps_reversed_inputs():

    """Verifies reversed numeric bounds are corrected so dashboard filters still behave correctly."""

    assert normalize_range(10, 2, 0, 100) == (2, 10)


def test_create_summary_table_returns_expected_aggregates():

    """Verifies grouped summary metrics are correct because KPI tables depend on exact aggregation results."""

    df = make_test_df()

    result = create_summary_table(df, "Region", "Lifetime_Value")

    asia_row = result[result["Region"] == "Asia"].iloc[0]
    assert asia_row["Count"] == 2
    assert asia_row["Mean"] == 750.00
    assert asia_row["Median"] == 750.00
    assert asia_row["Maximum"] == 1000.00
    assert asia_row["Total"] == 1500.00


def test_filter_sales_data_applies_reduced_churn_threshold():

    """Verifies churn reduction filtering removes records above the reduced threshold because several charts depend on this scenario logic."""

    df = make_test_df()

    result = filter_sales_data(
        df,
        churn_min=0.0,
        churn_max=1.0,
        pct_decrease=50,
        apply_reduced_churn=True,
    )

    assert set(result["Customer_ID"]) == {1, 2, 3}


def test_filter_sales_data_keeps_only_selected_region_and_category():

    """Verifies categorical filters combine correctly so the dashboard does not show rows from unselected segments."""

    df = make_test_df()

    result = filter_sales_data(
        df,
        regions=["Asia"],
        types=["Electronics"],
        date_start="2024-01-01",
        date_end="2024-12-31",
    )

    assert len(result) == 1
    assert result.iloc[0]["Customer_ID"] == 2