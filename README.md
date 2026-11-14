# ActivationLens

**Product analytics on Databricks, from messy events to trustworthy activation, engagement, retention, and experiment readouts.**

`Databricks` · `PySpark` · `Spark SQL` · `Delta Lake` · `Unity Catalog` · `Genie` · `AI/BI`

ActivationLens is a reproducible **Bronze / Silver / Gold lakehouse** for a simulated product onboarding journey. It generates event data, injects known quality issues, validates and deduplicates records, and materializes SQL-ready product metrics. It was built to demonstrate both **data engineering** and **product analytics**, rather than to claim a real experiment or production deployment.

> **Verified scope:** The notebook ran successfully in a Databricks workspace on November 14, 2026. The repository includes the runnable notebook, local contract tests, SQL examples, and technical documentation. The Genie space and AI/BI dashboard were configured in the workspace separately; they are not automatically provisioned from this repo.

## At a glance

| Measure | Result from deterministic synthetic data |
| --- | ---: |
| Simulated users / signups | 40,000 |
| Original events | 380,000 |
| Bronze events, including injected faults | 392,754 |
| Invalid events quarantined | 7,127 |
| Duplicate events removed | 5,627 |
| Silver events after cleaning | 380,000 |
| 7-day activation: control | 21.1% |
| 7-day activation: treatment | 25.8% |
| Day-7 retention: both groups | 50% |

The **+4.7 percentage-point activation gap was intentionally encoded** in the synthetic generator. It is a demonstration of the measurement pipeline, **not a causal A/B-test result**.

## Architecture

```text
40,000 synthetic signups           380,000 base events
            |                  + 5,627 duplicates
            |                  + 7,127 invalid events
            v                            v
      bronze_signups                bronze_events
            |                            |
            |                  validation / quarantine
            |                       + event-ID dedup
            |                            |
            |           +----------------+------------------+
            |           v                v                  v
            |      silver_events  silver_event_quarantine  dq_run_metrics
            |           |
            +-----------+
                        v
                Gold Delta tables
          - gold_user_activation
          - gold_experiment_summary
          - gold_daily_engagement
          - gold_retention_d7
                        |
                        v
             Databricks SQL / Genie / AI/BI
```

Read [architecture](docs/architecture.md) and [table definitions](docs/data_model.md) for metric grains, validation logic, and the exact nine output tables.

## Quick start

1. Open Databricks with permission to create managed Delta tables and attach a Spark-compatible Python compute resource.
2. Import [`notebooks/ActivationLens_Databricks_Lakehouse.ipynb`](notebooks/ActivationLens_Databricks_Lakehouse.ipynb).
3. Run all cells. The notebook creates an `activationlens` schema when permitted and falls back to `default` otherwise. **It overwrites its nine project-named Delta tables on each run.**
4. Inspect `gold_experiment_summary`, `gold_daily_engagement`, `gold_retention_d7`, and `dq_run_metrics` in Databricks SQL.
5. Run the read-only examples in [`sql/product_analytics.sql`](sql/product_analytics.sql), adjusting the sample catalog/schema to match your workspace.

No customer datasets, secrets, paid APIs, or external downloads are needed to generate the events. Full steps: [Reproduce in Databricks](docs/reproduce.md).

## Quality and validation

The pipeline quarantines rows with invalid required fields or event types and deduplicates valid `event_id` values. An accounting invariant is checked on the data:

```text
392,754 Bronze = 7,127 quarantined + 5,627 duplicates removed + 380,000 Silver
```

Local tests check the generator's arithmetic, synthetic activation/retention contracts, and notebook syntax/table writes. They do **not** run Spark:

```bash
python -m unittest discover -s tests -v
```

See [experiment interpretation](docs/experiment_notes.md) for why the synthetic difference cannot be treated as proof of a feature's impact.

## Repository guide

| Path | Purpose |
| --- | --- |
| [`notebooks/`](notebooks/) | Self-contained Databricks implementation and assertions |
| [`sql/`](sql/) | Read-only product metrics and data-quality queries |
| [`docs/architecture.md`](docs/architecture.md) | Design and limitations |
| [`docs/data_model.md`](docs/data_model.md) | Delta table grains and fields |
| [`docs/product_brief.md`](docs/product_brief.md) | Product question, success metrics, and analytical next steps |
| [`docs/reproduce.md`](docs/reproduce.md) | End-to-end rerun instructions |
| [`tests/`](tests/) | Standard-library offline regression checks |

## What this project does not claim

- It is **batch-based**, not streaming/CDC, incremental ETL, or an always-on job.
- The notebook overwrites the nine project tables; `dq_run_metrics` stores a **latest-run snapshot**, not historical monitoring.
- The treatment/control outcomes are **simulated**, not randomized customer experiments. No statistical significance or causal uplift is claimed.
- A Genie agent and eight-widget AI/BI dashboard were built in a workspace but **are not bundled or automatically published** by the notebook.

**Author:** [Panav Mhatre](https://github.com/PanavMhatre)
