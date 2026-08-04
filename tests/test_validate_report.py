import json
import unittest
from pathlib import Path

from validate_report import evaluate, render


ROOT = Path(__file__).resolve().parents[1]


class ValidationTest(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / "results/arm64-report.json").read_text())
        self.policy = json.loads((ROOT / "armbench-policy.json").read_text())

    def test_committed_arm64_report_passes_policy(self):
        checks = evaluate(self.report, self.policy)
        self.assertTrue(all(check.passed for check in checks))
        self.assertIn("optimization gate: PASS", render(checks))

    def test_rejects_non_arm_result(self):
        self.report["system"]["architecture"] = "x86_64"
        checks = evaluate(self.report, self.policy)
        self.assertFalse(checks[0].passed)

    def test_rejects_accuracy_regression(self):
        self.report["comparison"]["accuracy_delta"] = -0.5
        checks = evaluate(self.report, self.policy)
        accuracy = next(check for check in checks if check.name == "Accuracy delta")
        self.assertFalse(accuracy.passed)

    def test_rejects_insufficient_throughput_gain(self):
        self.report["comparison"]["throughput_speedup"] = 1.1
        checks = evaluate(self.report, self.policy)
        throughput = next(check for check in checks if check.name == "Median throughput speedup")
        self.assertFalse(throughput.passed)


if __name__ == "__main__":
    unittest.main()
