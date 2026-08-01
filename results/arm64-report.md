# ArmBench CI native Arm64 benchmark

Source: [GitHub Actions run 30688810539](https://github.com/ILoveBuns/armbench-ci/actions/runs/30688810539)

## Runner evidence

| Field | Value |
|---|---|
| Architecture | `aarch64` |
| Platform | `Linux-6.17.0-1020-azure-aarch64-with-glibc2.39` |
| Logical CPUs | 4 |
| Python | 3.12.13 |
| ONNX Runtime | 1.20.1 |

## Results

| Metric | FP32 | INT8 |
|---|---:|---:|
| Model size (KiB) | 271.0 | 72.1 |
| Accuracy | 0.4163 | 0.4088 |
| p50 latency (ms) | 0.0139 | 0.0130 |
| p95 latency (ms) | 0.0165 | 0.0137 |
| Throughput (samples/s) | 1,065,917.7 | 2,216,846.4 |

## Optimization summary

- Size reduction: **73.39%**
- p50 speedup: **1.07×**
- Accuracy delta: **-0.0075**
- Process RSS after benchmark: **210.7 MiB**

These measurements are from one reproducible hosted Arm64 run. They are not
claims about every workload or Arm system.
