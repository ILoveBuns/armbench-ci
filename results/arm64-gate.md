# ArmBench optimization gate: PASS

| Check | Actual | Requirement | Result |
|---|---:|---:|:---:|
| Native Arm architecture | aarch64 | one of aarch64, arm64 | PASS |
| Size reduction | 73.3949% | >= 60.0000% | PASS |
| Median throughput speedup | 2.2602× | >= 1.5000× | PASS |
| p50 latency speedup | 1.0654× | >= 0.9500× | PASS |
| p95 latency speedup | 1.0986× | >= 0.9500× | PASS |
| Accuracy delta | -0.0075 | >= -0.0200 | PASS |

This committed gate corresponds to `results/arm64-report.json`. The latest
policy-enforced native run is [GitHub Actions run 30881936662](https://github.com/ILoveBuns/armbench-ci/actions/runs/30881936662).
