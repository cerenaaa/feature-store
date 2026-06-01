# Feature Store

[![CI](https://github.com/cerenaaa/feature-store/actions/workflows/ci.yml/badge.svg)](https://github.com/cerenaaa/feature-store/actions)

Lightweight feature store for ML pipelines: feature registration, versioning, point-in-time correct retrieval, and online/offline serving. Eliminates training-serving skew.

## Core concepts

| Concept | Description |
|---|---|
| **Feature view** | Named group of features with transformation logic |
| **Entity** | Key used to look up feature values (e.g. customer_id) |
| **Point-in-time join** | Retrieve feature values as they were at a given timestamp (no leakage) |
| **Online store** | Low-latency key-value cache for serving |
| **Offline store** | Historical feature values for training |

## Structure
```
feature-store/
├── store/
│   ├── registry.py           # Feature and view registration
│   ├── offline_store.py      # Parquet-backed historical store
│   ├── online_store.py       # In-memory/Redis key-value store
│   └── pit_join.py           # Point-in-time correct joins
├── features/
│   └── definitions.py        # Example feature view definitions
├── data/
│   └── synthetic_events.py   # Synthetic entity + event data
└── demo.py
```

## Quickstart
```bash
pip install -r requirements.txt
python demo.py
```
