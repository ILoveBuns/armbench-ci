# Arm Create: AI Optimization — Cloud AI submission draft

## Project

ArmBench CI is a reproducible CI benchmark that exports a compact intent
classifier to ONNX, applies static INT8 quantization, and measures accuracy,
model size, latency, throughput, and process memory on a native Arm64 runner.

## Verified Arm64 result

The public GitHub Actions run `30688810539` completed successfully on
`aarch64`. Relative to FP32, INT8 reduced the model by 73.39%, improved p50
latency by 1.07×, improved p95 latency by 1.20×, increased the single-run
throughput measurement by 2.08×, and changed accuracy by -0.0075. The next
native run upgrades this evidence to repeated latency trials and median
throughput, making the comparison less sensitive to hosted-run noise. The
committed JSON and Markdown reports preserve the exact runner, package, and
measurement-protocol evidence.

## Reproduce

1. Open the repository Actions page.
2. Run **Arm64 benchmark**, or push to `main`.
3. Download the `armbench-report` artifact.
4. Compare it with `results/arm64-report.json`.

## Evidence

- Repository: `https://github.com/ILoveBuns/armbench-ci`
- Successful native run: `https://github.com/ILoveBuns/armbench-ci/actions/runs/30688810539`
- Workflow: `.github/workflows/arm64-benchmark.yml`
- Committed report: `results/arm64-report.md`

## Claims boundary

This is a small, deterministic benchmark designed to make an optimization
trade-off auditable. It does not claim that INT8 accelerates every model, and it
does not present the earlier x86_64 smoke run as Arm evidence.
