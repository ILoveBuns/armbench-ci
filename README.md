# ArmBench CI

ArmBench CI is a reproducible Cloud AI benchmark that trains a small intent
classifier, exports it to ONNX, quantizes it to INT8, and measures the result on
native Arm64 hardware. It is designed for the **Arm Create: AI Optimization
Challenge — Cloud AI track**.

The benchmark reports:

- model size and compression ratio;
- accuracy agreement between FP32 and INT8;
- p50/p95 inference latency and median throughput across repeated trials;
- peak resident memory;
- CPU and operating-system evidence from the runner.

GitHub Actions runs the benchmark on the official `ubuntu-24.04-arm` hosted
runner, so the published artifact is native Arm64 evidence rather than an
emulated estimate.

## Run locally

```bash
python -m pip install -r requirements.txt
python benchmark.py --output artifacts/report.json
python render_report.py artifacts/report.json artifacts/report.md
```

## Reproduce on Arm64

Run the **Arm64 benchmark** workflow manually or push to `main`. Download the
`armbench-report` artifact from the workflow run. The Markdown report includes
the exact machine architecture and package versions.

The first successful public native run and its committed evidence are available
in [`results/arm64-report.md`](results/arm64-report.md). Submission-ready wording
and evidence links are collected in [`SUBMISSION_DRAFT.md`](SUBMISSION_DRAFT.md).
The matching policy decision is committed as
[`results/arm64-gate.md`](results/arm64-gate.md); the latest main-branch Arm64
workflow also passed the same gate.

The measurement protocol uses 30 warm-up calls, 1,500 timed single-sample
inferences, and nine full-test-set throughput trials per model. Reporting a
median throughput and both p50 and p95 latency makes the optimization claim less
sensitive to a single noisy hosted-run measurement.

## Demo video

Watch the narrated 1080p [ArmBench CI demo on YouTube](https://youtu.be/ddOx7i0yGRk).
The exact published artifact remains available at
[`assets/ArmBench-CI-demo.mp4`](assets/ArmBench-CI-demo.mp4) for reproducibility.
The current 130.815-second artifact is H.264/AAC and matches the dynamic INT8
implementation and committed 2.26× median-throughput evidence.

## Why this matters

Teams often claim that quantization helps without publishing the accuracy,
memory, and tail-latency trade-off on the target architecture. ArmBench CI turns
that claim into a repeatable CI gate. `armbench-policy.json` requires native
Arm execution, at least 60% size reduction and 1.5× median throughput, no more
than 5% p50/p95 latency regression, and no more than 0.02 accuracy loss. A pull
request fails when any threshold is missed, and the Markdown gate report is
published with the benchmark artifact. The included workload is intentionally
small enough for a standard CPU-only cloud instance and can be replaced with a
larger ONNX model later.

Run the committed evidence through the same gate locally:

```bash
python validate_report.py results/arm64-report.json
python -m unittest discover -s tests -v
```

## License

Apache-2.0. See [LICENSE](LICENSE).
