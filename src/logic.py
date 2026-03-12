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
