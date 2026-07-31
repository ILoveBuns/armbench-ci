#!/usr/bin/env python3
import json
import sys
from pathlib import Path

source, destination = map(Path, sys.argv[1:3])
r = json.loads(source.read_text(encoding="utf-8"))
text = f"""# ArmBench CI native benchmark

## Runner evidence

| Field | Value |
|---|---|
| Architecture | `{r['system']['architecture']}` |
| Platform | `{r['system']['platform']}` |
| Logical CPUs | {r['system']['cpu_count']} |
| Python | {r['system']['python']} |
| ONNX Runtime | {r['system']['onnxruntime']} |

## Results

| Metric | FP32 | INT8 |
|---|---:|---:|
| Model size (KiB) | {r['fp32']['bytes']/1024:.1f} | {r['int8']['bytes']/1024:.1f} |
| Accuracy | {r['fp32']['accuracy']:.4f} | {r['int8']['accuracy']:.4f} |
| p50 latency (ms) | {r['fp32']['latency_ms_p50']:.4f} | {r['int8']['latency_ms_p50']:.4f} |
| p95 latency (ms) | {r['fp32']['latency_ms_p95']:.4f} | {r['int8']['latency_ms_p95']:.4f} |
| Throughput (samples/s) | {r['fp32']['throughput_samples_per_sec']:.1f} | {r['int8']['throughput_samples_per_sec']:.1f} |

## Optimization summary

- Size reduction: **{r['comparison']['size_reduction_percent']:.2f}%**
- p50 speedup: **{r['comparison']['p50_speedup']:.2f}×**
- Accuracy delta: **{r['comparison']['accuracy_delta']:+.4f}**
- Process RSS after benchmark: **{r['peak_rss_bytes']/1024/1024:.1f} MiB**
"""
destination.write_text(text, encoding="utf-8")
print(text)
