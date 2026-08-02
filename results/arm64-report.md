# ArmBench CI native benchmark

Source: [GitHub Actions run 30758735011](https://github.com/ILoveBuns/armbench-ci/actions/runs/30758735011)

## Runner evidence

| Field | Value |
|---|---|
| Architecture | `aarch64` |
| Platform | `Linux-6.17.0-1020-azure-aarch64-with-glibc2.39` |
| Logical CPUs | 4 |
| Python | 3.12.13 |
| ONNX Runtime | 1.20.1 |

## Measurement protocol

- 30 warm-up inferences per model.
- 5 latency trials × 300 single-sample inferences.
- 9 full-test-set trials; the table reports the median.

## Results

| Metric | FP32 | INT8 |
|---|---:|---:|
| Model size (KiB) | 271.0 | 72.1 |
| Accuracy | 0.4163 | 0.4088 |
| p50 latency (ms) | 0.0138 | 0.0130 |
| p95 latency (ms) | 0.0147 | 0.0134 |
| Throughput (samples/s) | 1189746.8 | 2689066.6 |

## Optimization summary

- Size reduction: **73.39%**
- p50 speedup: **1.07×**
- p95 speedup: **1.10×**
- Median throughput speedup: **2.26×**
- Accuracy delta: **-0.0075**
- Process RSS after benchmark: **210.8 MiB**
