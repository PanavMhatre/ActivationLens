# Architecture

ActivationLens is a repeatable batch **Bronze / Silver / Gold** lakehouse built with PySpark, Spark SQL, and managed Delta tables in Databricks.

```text
40,000 simulated signups          380,000 generated base events
        |                         + 5,627 duplicate event IDs
        |                         + 7,127 invalid rows
        v                                      v
  bronze_signups                         bronze_events
        |                                      |
        |                     validation + quarantine + deduplication
        |                           /                    \
        |                          v                      v
        |                     silver_events      silver_event_quarantine
        |                          |
        +--------------------------+
                                   v
                              Gold Delta tables
                gold_user_activation    gold_experiment_summary
                gold_daily_engagement   gold_retention_d7
                                   |
                                   v
                      Databricks SQL / Genie / AI/BI
```

## Synthetic event generation

- 40,000 deterministic user IDs, split evenly between control and treatment by user number parity.
- Signup dates distributed across 20 days beginning September 1, 2026.
- 380,000 generated base events, 5,627 injected duplicates, and 7,127 rows with missing user IDs.
- Synthetic outcomes encode 21.1% control activation, 25.8% treatment activation, and 50% day-7 retention in both groups.

## Quality controls

Records missing required `event_id`, `user_id`, or `event_ts` values, or with unrecognized event types, go to `silver_event_quarantine`. Remaining events are deduplicated on `event_id`; original `base` rows take priority over injected `duplicated` rows.

**Invariant:** `392,754 Bronze = 7,127 quarantined + 5,627 duplicates + 380,000 Silver`.

The `dq_run_metrics` table stores the counts from the latest notebook execution.

## Gold definitions

| Product metric | Implementation |
| --- | --- |
| Seven-day activation | First `job_created` event from signup through signup + 7 calendar days, inclusive |
| Daily active users | Distinct users with eligible activity (`signed_up`, `job_created`, `session_started`, `feature_viewed`) per date |
| Day-seven retention | A `session_started` event exactly seven calendar days after signup |
| Experiment readout | Signups, activated users, and activation rate by simulated variant |

## Operational limitations

The notebook uses `mode("overwrite")` for nine project-owned Delta tables. This is **not** streaming, CDC, incremental refresh, scheduled orchestration, or a production service. `dq_run_metrics` is a latest-run snapshot, not a historical run log.

The generated data is not actual customer activity. The control/treatment difference is built into the synthetic generator and is not causal evidence.

For individual table schemas see [data model](data_model.md). For how to rerun see [reproduction guide](reproduce.md).
