"""Feature store end-to-end demo."""
from store.registry import FeatureRegistry, Entity, FeatureView
from store.online_store import OnlineStore
from store.pit_join import point_in_time_join
from data.synthetic_events import generate_customer_events


def main():
    registry = FeatureRegistry()
    registry.register_entity(Entity("customer", "customer_id", "Retail customer"))
    registry.register_feature_view(FeatureView(
        name="customer_behavior",
        entities=["customer"],
        features=["monthly_spend", "login_count_30d", "support_tickets_30d", "days_since_last_purchase"],
        ttl_days=30,
    ))

    print("Generating synthetic data...")
    entity_df, feature_df = generate_customer_events(n_customers=100, n_events=1000)

    print("Running point-in-time join...")
    training_data = point_in_time_join(
        entity_df, feature_df,
        entity_key="customer_id",
        timestamp_col="event_timestamp",
        feature_timestamp_col="feature_timestamp",
        feature_cols=["monthly_spend", "login_count_30d", "days_since_last_purchase"],
        max_age_days=30,
    )
    print("Training dataset shape:", training_data.shape)
    print(training_data[["customer_id", "monthly_spend", "login_count_30d"]].head(3).to_string())

    print("Populating online store...")
    online = OnlineStore()
    latest = feature_df.sort_values("feature_timestamp").groupby("customer_id").last().reset_index()
    online.write_batch("customer_behavior", latest.to_dict("records"), entity_key="customer_id")
    print("Online store size:", online.size)

    sample_id = entity_df["customer_id"].iloc[0]
    features = online.read("customer_behavior", sample_id)
    print("Sample features for", sample_id, ":", features)


if __name__ == "__main__":
    main()
