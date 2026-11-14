# Reproduce ActivationLens in Databricks

## Requirements

- A Databricks workspace with Python notebook compute and permission to create managed Delta tables.
- Spark and Delta Lake supplied by the Databricks runtime.
- No real customer data, external files, secrets, API keys, or additional Python packages required.

## Run

1. Import [ActivationLens_Databricks_Lakehouse.ipynb](../notebooks/ActivationLens_Databricks_Lakehouse.ipynb) as a notebook.
2. Attach compatible Spark compute. The initial execution used Databricks Serverless Free Edition.
3. Choose **Run all**. The notebook discovers the active catalog and attempts to create schema `activationlens`; if permission is unavailable, it falls back to `default`.
4. The notebook creates or replaces these nine managed Delta tables:

   - `bronze_signups` and `bronze_events`
   - `silver_events` and `silver_event_quarantine`
   - `dq_run_metrics`
   - `gold_user_activation`, `gold_experiment_summary`, `gold_daily_engagement`, `gold_retention_d7`

5. Confirm the notebook's printed assertions:

```text
Bronze event rows: 392754 (expected 392,754)
PASS: 40K users, 380K clean events, 7,127 quarantined invalid rows, 5,627 duplicates removed
PASS: SQL product activation rates, daily engagement, and D7 retention tables
```

6. Inspect the Gold tables in Catalog Explorer. In SQL Editor, run the read-only sample statements in [sql/product_analytics.sql](../sql/product_analytics.sql) after replacing the sample `workspace.activationlens` identifier with your active catalog and schema.

## Local validation

```bash
python -m unittest discover -s tests -v
```

The five tests require only Python's standard library. They verify synthetic arithmetic and notebook contracts, **not** end-to-end Spark execution.

## Optional workspace presentation

Create a Genie space using `gold_experiment_summary`, `gold_daily_engagement`, `gold_retention_d7`, `gold_user_activation`, and `dq_run_metrics`. Example questions:

- What is the 7-day activation rate by variant?
- How many users were active each day?
- What is the day-7 retention rate by variant?
- How many rows were rejected by the latest data quality run?

An AI/BI dashboard can be configured separately with these tables. Existing workspace dashboard and Genie configuration are not represented as deployable artifacts in this repository.

## Rerun cautions

- The notebook overwrites **its own nine named tables** on every run.
- It is not streaming, CDC, incrementally updated, or scheduled in this repository.
- `dq_run_metrics` captures only the most recent run.
- The data generator intentionally encodes the control/treatment and retention rates. No causal business impact is established.

See [architecture](architecture.md), [data model](data_model.md), and [experiment limitations](experiment_notes.md) for full definitions.
