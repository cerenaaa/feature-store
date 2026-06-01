"""
Point-in-time correct join.
Joins entity keys with their feature values AS OF a given timestamp.
Prevents data leakage from future feature values.
"""
from __future__ import annotations
import pandas as pd
import numpy as np


def point_in_time_join(
    entity_df: pd.DataFrame,
    feature_df: pd.DataFrame,
    entity_key: str,
    timestamp_col: str = "event_timestamp",
    feature_timestamp_col: str = "feature_timestamp",
    feature_cols: list[str] = None,
    max_age_days: float = None,
) -> pd.DataFrame:
    """
    For each row in entity_df, find the most recent feature values
    from feature_df where feature_timestamp <= event_timestamp.

    This is the core of a feature store — ensures no future leakage.
    """
    entity_df = entity_df.copy()
    feature_df = feature_df.sort_values(feature_timestamp_col)
    feature_cols = feature_cols or [c for c in feature_df.columns
                                     if c not in [entity_key, feature_timestamp_col]]

    result_rows = []
    for _, row in entity_df.iterrows():
        et = row[timestamp_col]
        ek = row[entity_key]

        # Features for this entity, on or before event timestamp
        mask = (feature_df[entity_key] == ek) & (feature_df[feature_timestamp_col] <= et)
        candidates = feature_df[mask]

        if max_age_days is not None:
            cutoff = et - pd.Timedelta(days=max_age_days)
            candidates = candidates[candidates[feature_timestamp_col] >= cutoff]

        if candidates.empty:
            feat_row = {col: np.nan for col in feature_cols}
        else:
            latest = candidates.iloc[-1]
            feat_row = {col: latest[col] for col in feature_cols if col in latest.index}

        result_rows.append({**row.to_dict(), **feat_row})

    result = pd.DataFrame(result_rows)
    n_missing = result[feature_cols].isna().any(axis=1).sum()
    print(f"PIT join: {len(result)} rows | {n_missing} with missing features")
    return result
