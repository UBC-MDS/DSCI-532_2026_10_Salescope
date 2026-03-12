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