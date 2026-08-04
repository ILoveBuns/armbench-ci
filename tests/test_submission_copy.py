import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SubmissionCopyTest(unittest.TestCase):
    def test_submission_copy_matches_implementation(self):
        copy = (ROOT / "SUBMISSION_DRAFT.md").read_text(encoding="utf-8")
        self.assertIn("ONNX Runtime dynamic INT8 weight quantization", copy)
        self.assertIn("MLPClassifier", copy)
        self.assertIn("ubuntu-24.04-arm", copy)

    def test_demo_link_points_to_the_committed_asset(self):
        copy = (ROOT / "SUBMISSION_DRAFT.md").read_text(encoding="utf-8")
        expected = (
            "https://raw.githubusercontent.com/ILoveBuns/armbench-ci/"
            "main/assets/ArmBench-CI-demo.mp4"
        )
        self.assertIn(expected, copy)
        self.assertTrue((ROOT / "assets/ArmBench-CI-demo.mp4").is_file())

    def test_video_source_has_no_stale_quantization_claims(self):
        source = (ROOT / "scripts/build_demo_video.py").read_text(encoding="utf-8")
        self.assertNotIn("statically quantized", source)
        self.assertNotIn("Static INT8 calibration", source)
        self.assertIn("Dynamic INT8 weights", source)

    def test_claimed_metrics_match_committed_report(self):
        copy = (ROOT / "SUBMISSION_DRAFT.md").read_text(encoding="utf-8")
        report = json.loads(
            (ROOT / "results/arm64-report.json").read_text(encoding="utf-8")
        )
        expected = {
            "size": f"{report['comparison']['size_reduction_percent']:.2f}%",
            "p50": f"{report['comparison']['p50_speedup']:.2f}×",
            "p95": f"{report['comparison']['p95_speedup']:.2f}×",
            "throughput": f"{report['comparison']['throughput_speedup']:.2f}×",
            "accuracy": f"{report['comparison']['accuracy_delta']:.4f}",
        }
        for metric in expected.values():
            self.assertRegex(copy, re.escape(metric))


if __name__ == "__main__":
    unittest.main()
