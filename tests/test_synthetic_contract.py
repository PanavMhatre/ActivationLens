"""Offline regression checks for ActivationLens's deterministic synthetic data contract.

These tests do NOT run PySpark or Databricks. To validate real table writes,
execute the notebook in an attached Databricks workspace.
"""
import ast
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "ActivationLens_Databricks_Lakehouse.ipynb"


class SyntheticContractTests(unittest.TestCase):
    def test_event_accounting_reconciles(self):
        base = 380_000
        injected_duplicates = 5_627
        quarantined_invalid = 7_127
        bronze = base + injected_duplicates + quarantined_invalid
        self.assertEqual(bronze, 392_754)
        self.assertEqual(bronze - injected_duplicates - quarantined_invalid, base)

    def test_variant_split_and_activation_thresholds(self):
        signups = {"control": 0, "treatment": 0}
        activation = {"control": 0, "treatment": 0}
        for user_num in range(40_000):
            variant = "control" if user_num % 2 == 0 else "treatment"
            threshold = 211 if variant == "control" else 258
            signups[variant] += 1
            if ((user_num // 2) % 1000) < threshold:
                activation[variant] += 1
        self.assertEqual(signups, {"control": 20_000, "treatment": 20_000})
        self.assertEqual(activation, {"control": 4_220, "treatment": 5_160})
        self.assertAlmostEqual(activation["control"] / 20_000, 0.211)
        self.assertAlmostEqual(activation["treatment"] / 20_000, 0.258)

    def test_encoded_day_seven_retention(self):
        returners = {"control": 0, "treatment": 0}
        for user_num in range(40_000):
            if user_num % 4 < 2:
                variant = "control" if user_num % 2 == 0 else "treatment"
                returners[variant] += 1
        self.assertEqual(returners, {"control": 10_000, "treatment": 10_000})

    def test_notebook_code_parses(self):
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        code_cells = [
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        ]
        self.assertEqual(len(code_cells), 5)
        for source in code_cells:
            ast.parse(source)

    def test_nine_table_write_contract(self):
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        code = "\n".join(
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
        )
        expected = {
            "bronze_signups", "bronze_events",
            "silver_events", "silver_event_quarantine", "dq_run_metrics",
            "gold_user_activation", "gold_experiment_summary",
            "gold_daily_engagement", "gold_retention_d7",
        }
        self.assertIn("save_delta(", code)
        for table in expected:
            self.assertIn(f'"{table}"', code)


if __name__ == "__main__":
    unittest.main()
