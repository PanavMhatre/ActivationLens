# Data model and contracts

All nine datasets are materialized as managed Delta tables in the active catalog and, when permitted, the `activationlens` schema (otherwise `default`).

| Table | Grain | Fields | Role |
| --- | --- | --- | --- |
| `bronze_signups` | One user | `user_id`, `signup_date`, `variant` | Simulated signup source |
| `bronze_events` | One ingested row, may duplicate | `event_id`, `user_id`, `event_type`, `event_ts`, `ingest_source` | Fault-injected raw events |
| `silver_events` | One valid row per `event_id` | Same event fields | Deduplicated clean stream |
| `silver_event_quarantine` | One invalid row | Same event fields | Rejected-record audit |
| `dq_run_metrics` | One row for latest execution | `run_utc`, `bronze_rows`, `quarantined_rows`, `duplicate_rows_removed`, `silver_rows` | Quality counts |
| `gold_user_activation` | One signup user | `user_id`, `signup_date`, `variant`, `first_job_date`, `is_activated_7d` | Activation indicator |
| `gold_experiment_summary` | One simulated variant | `variant`, `signups`, `activated_7d`, `activation_rate` | Variant summary |
| `gold_daily_engagement` | One activity date | `activity_date`, `daily_active_users`, `event_count` | Engagement trend |
| `gold_retention_d7` | One signup date + variant | `signup_date`, `variant`, `cohort_size`, `retained_day_7`, `retention_rate_d7` | Cohort retention |

## Semantic choices

- Activation is inclusive of day 7 and uses **calendar dates**, not a rolling 168-hour window.
- Day-7 retention is an exact calendar-day return event, not a rolling weekly retention measure.
- Daily activity excludes `email_delivered`.
- Product outcomes are **synthetic by design**. These are useful SQL and modeling examples, not observational findings.

See [architecture](architecture.md) for validation logic and [experiment notes](experiment_notes.md) for interpretation.
