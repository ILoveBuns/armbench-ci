#!/usr/bin/env python3
import argparse
import json
import os
import platform
import statistics
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
import psutil
from onnxruntime.quantization import QuantType, quantize_dynamic
from sklearn.datasets import make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


def percentile(values, q):
    return float(np.percentile(np.asarray(values, dtype=np.float64), q))


def train_and_export(workdir: Path):
    x, y = make_classification(
        n_samples=4000,
        n_features=256,
        n_informative=64,
        n_redundant=24,
        n_classes=12,
        random_state=42,
    )
    x_train, x_test, y_train, y_test = train_test_split(
        x.astype(np.float32), y, test_size=0.2, random_state=42, stratify=y
    )
    model = MLPClassifier(
        hidden_layer_sizes=(192, 96),
        activation="relu",
        max_iter=45,
        batch_size=128,
        early_stopping=True,
        random_state=42,
    )
    model.fit(x_train, y_train)
    fp32 = workdir / "intent-fp32.onnx"
    int8 = workdir / "intent-int8.onnx"
    graph = convert_sklearn(
        model,
        initial_types=[("input", FloatTensorType([None, x_train.shape[1]]))],
        options={id(model): {"zipmap": False}},
        target_opset=17,
    )
    fp32.write_bytes(graph.SerializeToString())
    quantize_dynamic(str(fp32), str(int8), weight_type=QuantType.QInt8)
    return x_test, y_test, fp32, int8


def benchmark_model(
    path: Path,
    x_test,
    y_test,
    latency_rounds=300,
    latency_trials=5,
    throughput_trials=9,
):
    session = ort.InferenceSession(
        str(path), providers=["CPUExecutionProvider"],
        sess_options=ort.SessionOptions(),
    )
    input_name = session.get_inputs()[0].name
    sample = x_test[:1]
    for _ in range(30):
        session.run(None, {input_name: sample})
    latencies = []
    for trial in range(latency_trials):
        for i in range(latency_rounds):
            row_index = (trial * latency_rounds + i) % len(x_test)
            row = x_test[row_index : row_index + 1]
            start = time.perf_counter_ns()
            session.run(None, {input_name: row})
            latencies.append((time.perf_counter_ns() - start) / 1_000_000)

    throughput_samples = []
    outputs = None
    for _ in range(throughput_trials):
        start = time.perf_counter_ns()
        outputs = session.run(None, {input_name: x_test})
        elapsed_seconds = (time.perf_counter_ns() - start) / 1_000_000_000
        throughput_samples.append(len(x_test) / elapsed_seconds)

    assert outputs is not None
    predictions = np.asarray(outputs[0]).reshape(-1)
    return {
        "bytes": path.stat().st_size,
        "accuracy": float(accuracy_score(y_test, predictions)),
        "latency_ms_p50": percentile(latencies, 50),
        "latency_ms_p95": percentile(latencies, 95),
        "latency_ms_mean": float(statistics.mean(latencies)),
        "throughput_samples_per_sec": float(statistics.median(throughput_samples)),
        "throughput_samples_per_sec_min": float(min(throughput_samples)),
        "throughput_samples_per_sec_max": float(max(throughput_samples)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/report.json")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    model_dir = output.parent / "models"
    model_dir.mkdir(exist_ok=True)
    x_test, y_test, fp32_path, int8_path = train_and_export(model_dir)
    process = psutil.Process(os.getpid())
    report = {
        "system": {
            "architecture": platform.machine(),
            "platform": platform.platform(),
            "python": platform.python_version(),
            "onnxruntime": ort.__version__,
            "cpu_count": psutil.cpu_count(logical=True),
        },
        "measurement": {
            "warmup_runs": 30,
            "latency_rounds_per_trial": 300,
            "latency_trials": 5,
            "throughput_trials": 9,
            "throughput_statistic": "median",
        },
        "fp32": benchmark_model(fp32_path, x_test, y_test),
        "int8": benchmark_model(int8_path, x_test, y_test),
    }
    report["peak_rss_bytes"] = process.memory_info().rss
    report["comparison"] = {
        "size_reduction_percent": 100 * (1 - report["int8"]["bytes"] / report["fp32"]["bytes"]),
        "p50_speedup": report["fp32"]["latency_ms_p50"] / report["int8"]["latency_ms_p50"],
        "p95_speedup": report["fp32"]["latency_ms_p95"] / report["int8"]["latency_ms_p95"],
        "throughput_speedup": report["int8"]["throughput_samples_per_sec"] / report["fp32"]["throughput_samples_per_sec"],
        "accuracy_delta": report["int8"]["accuracy"] - report["fp32"]["accuracy"],
    }
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
