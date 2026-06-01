"""Synthetic entity + feature event data for feature store demo."""
import numpy as np
import pandas as pd


def generate_customer_events(n_customers: int = 500, n_events: int = 5000,
                               seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    customer_ids = [f"CUST_{i:04d}" for i in range(n_customers)]
    start = pd.Timestamp("2024-01-01")

    # Feature events: customer behavioral features logged over time
    events = []
    for _ in range(n_events):
        cust = rng.choice(customer_ids)
        ts = start + pd.Timedelta(hours=int(rng.integers(0, 365*24)))
        events.append({
            "customer_id": cust,
            "feature_timestamp": ts,
            "monthly_spend": round(float(rng.lognormal(4, 0.5)), 2),
            "login_count_30d": int(rng.poisson(8)),
            "support_tickets_30d": int(rng.poisson(0.5)),
            "days_since_last_purchase": int(rng.exponential(14)),
        })
    feature_df = pd.DataFrame(events).sort_values("feature_timestamp").reset_index(drop=True)

    # Entity df: prediction requests at specific timestamps
    entity_records = []
    for cust in rng.choice(customer_ids, size=200, replace=True):
        ts = start + pd.Timedelta(hours=int(rng.integers(180*24, 365*24)))
        entity_records.append({"customer_id": cust, "event_timestamp": ts,
                                "label": int(rng.binomial(1, 0.15))})
    entity_df = pd.DataFrame(entity_records).sort_values("event_timestamp").reset_index(drop=True)

    print(f"Features: {len(feature_df)} events | Entity requests: {len(entity_df)}")
    return entity_df, feature_df
