# ArmBench CI

ArmBench CI is a reproducible Cloud AI benchmark that trains a small intent
classifier, exports it to ONNX, quantizes it to INT8, and measures the result on
native Arm64 hardware. It is designed for the **Arm Create: AI Optimization
Challenge — Cloud AI track**.

The benchmark reports:

- model size and compression ratio;
- accuracy agreement between FP32 and INT8;
- p50/p95 inference latency and throughput;
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

## Why this matters

Teams often claim that quantization helps without publishing the accuracy,
memory, and tail-latency trade-off on the target architecture. ArmBench CI turns
that claim into a repeatable CI gate. The included workload is intentionally
small enough for a standard CPU-only cloud instance and can be replaced with a
larger ONNX model later.

## License

Apache-2.0. See [LICENSE](LICENSE).
