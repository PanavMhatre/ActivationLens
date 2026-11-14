-- ActivationLens: read-only Databricks SQL examples
-- Replace `workspace`.`activationlens` with the catalog and schema printed by the notebook.
-- All inputs are synthetic. Experiment figures are not causal evidence.

-- 1. Simulated activation experiment breakdown.
SELECT variant, signups, activated_7d, activation_rate
FROM `workspace`.`activationlens`.`gold_experiment_summary`
ORDER BY variant;

-- 2. Daily active users and eligible events by date.
SELECT activity_date, daily_active_users, event_count
FROM `workspace`.`activationlens`.`gold_daily_engagement`
ORDER BY activity_date;

-- 3. Day-7 retention by simulated variant.
SELECT
  variant,
  SUM(cohort_size) AS signups,
  SUM(retained_day_7) AS retained_users,
  ROUND(SUM(retained_day_7) / SUM(cohort_size), 4) AS retention_rate_d7
FROM `workspace`.`activationlens`.`gold_retention_d7`
GROUP BY variant
ORDER BY variant;

-- 4. Most recent data-quality snapshot, not historical monitoring.
SELECT run_utc, bronze_rows, quarantined_rows,
       duplicate_rows_removed, silver_rows
FROM `workspace`.`activationlens`.`dq_run_metrics`
ORDER BY run_utc DESC
LIMIT 1;

-- 5. Reconcile event accounting after validation and deduplication.
SELECT
  b.bronze_rows,
  q.quarantined_rows,
  q.duplicate_rows_removed,
  q.silver_rows,
  b.bronze_rows = q.quarantined_rows
                + q.duplicate_rows_removed
                + q.silver_rows AS reconciles
FROM (
  SELECT COUNT(*) AS bronze_rows
  FROM `workspace`.`activationlens`.`bronze_events`
) b
CROSS JOIN `workspace`.`activationlens`.`dq_run_metrics` q;
