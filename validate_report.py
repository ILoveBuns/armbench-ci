#!/usr/bin/env python3
"""Validate an ArmBench report against an explicit optimization policy."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Check:
    name: str
    actual: str
    requirement: str
    passed: bool


def evaluate(report: dict[str, Any], policy: dict[str, Any]) -> list[Check]:
    """Return every policy check so failures remain explainable in CI."""
    comparison = report["comparison"]
    architecture = str(report["system"]["architecture"]).lower()
    allowed = [str(value).lower() for value in policy["allowed_architectures"]]
    checks = [Check("Native Arm architecture", architecture, "one of " + ", ".join(allowed), architecture in allowed)]
    metrics = [
        ("Size reduction", "size_reduction_percent", "minimum_size_reduction_percent", "%"),
        ("Median throughput speedup", "throughput_speedup", "minimum_throughput_speedup", "×"),
        ("p50 latency speedup", "p50_speedup", "minimum_p50_speedup", "×"),
        ("p95 latency speedup", "p95_speedup", "minimum_p95_speedup", "×"),
        ("Accuracy delta", "accuracy_delta", "minimum_accuracy_delta", ""),
    ]
    for label, report_key, policy_key, suffix in metrics:
        actual = float(comparison[report_key])
        minimum = float(policy[policy_key])
        checks.append(Check(label, f"{actual:.4f}{suffix}", f">= {minimum:.4f}{suffix}", actual >= minimum))
    return checks


def render(checks: list[Check]) -> str:
    """Render a compact Markdown report suitable for a workflow summary."""
    verdict = "PASS" if all(check.passed for check in checks) else "FAIL"
    lines = [f"# ArmBench optimization gate: {verdict}", "", "| Check | Actual | Requirement | Result |", "|---|---:|---:|:---:|"]
    lines.extend(
        f"| {check.name} | {check.actual} | {check.requirement} | {'PASS' if check.passed else 'FAIL'} |"
        for check in checks
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--policy", type=Path, default=Path("armbench-policy.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    policy = json.loads(args.policy.read_text(encoding="utf-8"))
    checks = evaluate(report, policy)
    rendered = render(checks)
    print(rendered, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if all(check.passed for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
