# Product brief: onboarding activation versus retention

## User problem

Product teams need to distinguish **getting a new user to first value** from **bringing them back**. Duplicated or invalid telemetry can distort conversion and retention denominators before the product decision even begins.

## Intended users

- **Product manager:** Compare activation, engagement and retention without conflating them.
- **Analyst / data scientist:** Trust metric grains, denominators and cohorts.
- **Data engineer:** Reconcile every clean Gold metric to validated event inputs.

## Success metrics

| Measure | Definition | Business interpretation |
| --- | --- | --- |
| 7-day activation | First `job_created` within signup date through signup + 7 days | First-value milestone |
| Daily active users | Distinct eligible event users by date | Engagement pattern |
| D7 retention | A `session_started` exactly 7 days after signup | Return behavior |
| Data quality | Bronze = invalid + removed duplicates + Silver | Metric trustworthiness |

## Demonstrated output

On **synthetically generated** data, control and treatment activation are 21.1% and 25.8%; retention is 50% in both variants. The +4.7 percentage-point activation difference is deliberately encoded in the generator. It is a useful illustration of metric separation, **not evidence that a real feature caused the difference**.

## Next questions

1. Does time to first successful job correlate with later engagement?
2. Which activity between first value and day 7 best predicts return sessions?
3. How do late, missing or duplicated events alter key product rates?
4. What guardrails and statistical checks would be necessary for a real randomized experiment?

## Project boundary

The shipped open-source artifact is the notebook, nine Delta table definitions and reproducible synthetic metric readouts. Databricks Genie and AI/BI dashboard assets exist as workspace-level interfaces, not as automatically provisioned services in this repository.
