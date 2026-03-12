import pandas as pd

def normalize_range(min_val, max_val, default_min, default_max):
    """
    Normalize a min/max pair so reversed inputs still work.

    Parameters
    ----------
    min_val : float | int | None
        User-provided minimum value.
    max_val : float | int | None
        User-provided maximum value.
    default_min : float | int
        Default minimum when min_val is None.
    default_max : float | int
        Default maximum when max_val is None.

    Returns
    -------
    tuple
        Ordered (min, max) pair.
    """

    min_val = default_min if min_val is None else min_val
    max_val = default_max if max_val is None else max_val
    return min(min_val, max_val), max(min_val, max_val)

def create_summary_table(df, grouping, feature):
    """
    Build a grouped summary table for a dashboard metric.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe.
    grouping : str
        Column used for grouping.
    feature : str
        Numeric column to summarize.

    Returns
    -------
    pandas.DataFrame
        Summary table with count, mean, median, maximum, and total.
    """

    summary = (
        df.groupby(grouping)
        .agg(
            Count=(feature, "size"),
            Mean=(feature, "mean"),
            Median=(feature, "median"),
            Maximum=(feature, "max"),
            Total=(feature, "sum"),
        )
        .round(2)
        .reset_index()
    )
    return summary

def filter_sales_data(
    df,
    churn_min=None,
    churn_max=None,
    pct_decrease=0,
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
    apply_reduced_churn=False,
):
    """
    Filter the sales dataframe using dashboard controls.

    This function powers the dashboard filters and can optionally apply the
    reduced churn threshold used by the churn decrease scenario.

    Returns
    -------
    pandas.DataFrame
        Filtered dataframe with an `in_reduced_churn_range` helper column.
    """

    df = df.copy()

    churn_min, churn_max = normalize_range(churn_min, churn_max, 0.0, 1.0)
    clv_min, clv_max = normalize_range(clv_min, clv_max, 100, 10000)
    order_min, order_max = normalize_range(order_min, order_max, 20, 200)
    freq_min, freq_max = normalize_range(freq_min, freq_max, 1, 19)

    reduced_max = churn_max * (1 - pct_decrease / 100)

    df = df[df["Churn_Probability"].between(churn_min, churn_max)]

    if apply_reduced_churn and pct_decrease > 0:
        
        df = df[df["Churn_Probability"] <= reduced_max]

    df["in_reduced_churn_range"] = (
        (df["Churn_Probability"] >= churn_min)
        & (df["Churn_Probability"] <= reduced_max)
    )

    df = df[df["Lifetime_Value"].between(clv_min, clv_max)]
    df = df[df["Average_Order_Value"].between(order_min, order_max)]
    df = df[df["Purchase_Frequency"].between(freq_min, freq_max)]

    if date_start is not None and date_end is not None:

        df = df[df["Launch_Date"].between(pd.Timestamp(date_start), pd.Timestamp(date_end))]

    if types:

        df = df[df["Most_Frequent_Category"].isin(types)]

    if regions:

        df = df[df["Region"].isin(regions)]

    if strategies:

        df = df[df["Retention_Strategy"].isin(strategies)]

    return df
