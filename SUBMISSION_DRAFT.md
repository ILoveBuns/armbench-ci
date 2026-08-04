# Arm Create: AI Optimization — Cloud AI submission draft

## Project

ArmBench CI is a reproducible CI benchmark that exports a compact intent
classifier to ONNX, applies dynamic INT8 quantization, and measures accuracy,
model size, latency, throughput, and process memory on a native Arm64 runner.

## Verified Arm64 result

The public GitHub Actions run `30758735011` completed successfully on
`aarch64`. Relative to FP32, INT8 reduced the model by 73.39%, improved p50
latency by 1.07×, improved p95 latency by 1.10×, increased median throughput by
2.26×, and changed accuracy by -0.0075. These results use five latency trials
and nine full-test-set throughput trials per model, making the comparison less
sensitive to hosted-run noise. The committed JSON and Markdown reports preserve
the exact runner, package, and measurement-protocol evidence.

The workflow enforces those claims as a real CI policy: native Arm64, at least
60% size reduction, 1.5× median throughput, bounded latency regression, and no
more than 0.02 accuracy loss. It produces a readable gate report and fails the
pull request if any requirement is missed.

## Reproduce

1. Open the repository Actions page.
2. Run **Arm64 benchmark**, or push to `main`.
3. Download the `armbench-report` artifact.
4. Compare it with `results/arm64-report.json`.

## Evidence

- Repository: `https://github.com/ILoveBuns/armbench-ci`
- Successful native run: `https://github.com/ILoveBuns/armbench-ci/actions/runs/30758735011`
- Latest policy-enforced main run: `https://github.com/ILoveBuns/armbench-ci/actions/runs/30882077004`
- Demo video: `https://raw.githubusercontent.com/ILoveBuns/armbench-ci/main/assets/ArmBench-CI-demo.mp4`
- Workflow: `.github/workflows/arm64-benchmark.yml`
- Committed report: `results/arm64-report.md`
- Committed gate decision: `results/arm64-gate.md`
- Machine-readable policy: `armbench-policy.json`
- Policy validator and tests: `validate_report.py`, `tests/test_validate_report.py`

## Claims boundary

This is a small, deterministic benchmark designed to make an optimization
trade-off auditable. It does not claim that INT8 accelerates every model, and it
does not present the earlier x86_64 smoke run as Arm evidence.

## Devpost replacement copy

The current public Devpost page still describes an old digits/PyTorch prototype.
Replace that implementation description with the following text before judging:

### What it does

ArmBench CI trains a deterministic compact intent classifier, exports it to
ONNX, applies ONNX Runtime dynamic INT8 weight quantization, and benchmarks FP32
and INT8 on a native Arm64 GitHub Actions runner. It publishes machine-readable
and human-readable evidence for model size, accuracy, p50/p95 latency, repeated
full-test-set throughput, peak resident memory, architecture, and package
versions. A policy gate fails CI if the run is not native Arm64 or if the
optimization misses its declared size, throughput, latency, or accuracy limits.

### How we built it

The benchmark uses Python, scikit-learn, skl2onnx, ONNX Runtime, psutil, and
GitHub Actions. A seeded synthetic multiclass intent-style workload trains an
`MLPClassifier`; skl2onnx exports the FP32 graph, and ONNX Runtime dynamically
quantizes its weights to QInt8. GitHub's `ubuntu-24.04-arm` runner executes the
same benchmark and validator, then publishes JSON, Markdown, and a concise gate
decision as workflow artifacts.

### Evidence links to use

- Demo: `https://raw.githubusercontent.com/ILoveBuns/armbench-ci/main/assets/ArmBench-CI-demo.mp4`
- Latest successful policy-enforced run: `https://github.com/ILoveBuns/armbench-ci/actions/runs/30882077004`
- Committed report: `https://github.com/ILoveBuns/armbench-ci/blob/main/results/arm64-report.md`
- Committed gate: `https://github.com/ILoveBuns/armbench-ci/blob/main/results/arm64-gate.md`

Do not describe the current implementation as a digits image classifier,
PyTorch pipeline, static quantization, or calibration-based quantization.
