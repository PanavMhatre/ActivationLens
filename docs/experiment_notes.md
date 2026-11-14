# Experiment interpretation

The notebook's synthetic generator deliberately encodes the following numbers. These are **not** measurements from a real randomized controlled experiment.

| Cohort | Signups | 7-day activated | Activation | Day-7 returned | D7 retention |
| --- | ---: | ---: | ---: | ---: | ---: |
| Control | 20,000 | 4,220 | 21.1% | 10,000 | 50.0% |
| Treatment | 20,000 | 5,160 | 25.8% | 10,000 | 50.0% |

- Difference in the generated 7-day activation metric: **+4.7 percentage points**.
- No generated difference in the day-7 retention metric: **50% for both groups**.

**What can be concluded:** The lakehouse correctly produces separate activation and retention metrics, so an analyst can see that these measure different user behaviors.

**What cannot be concluded:** A feature improved activation, a treatment should ship, an experiment reached statistical significance, or a real product will see these outcomes. The outcomes were programmed into the generator.

## What a real A/B test would need

For real events, evaluate randomization and sample-ratio mismatch, instrumentation quality, exposure definition, eligibility windows and right-censoring, confidence intervals, predefined success criteria, and relevant guardrail metrics. This repository demonstrates the data path only.

An appropriate next product question is whether a quicker first successful job predicts continued usage after day 7, using an actual event stream and a defensible analysis design.
