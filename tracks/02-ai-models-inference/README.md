# Track 02: AI Models, Serving & Inference Engineering

## Overview

Welcome to **Track 02: AI Models, Serving & Inference Engineering**. This track is dedicated to the systems engineering discipline required to deploy, optimize, and serve large language models (LLMs) and foundation models at scale with ultra-low latency and maximum token throughput.

Beyond high-level prompt engineering, this track focuses on the lower levels of the modern AI serving stack: GPU memory layout, kernel execution, continuous batching, quantization architectures, and distributed inference engines (vLLM, TensorRT-LLM, Triton).

---

## Pedagogical Philosophy

1. **Hardware & Memory Bound Reality:** Understanding GPU compute boundaries (FLOP/s) vs. memory bandwidth limits (TB/s) and how KV caching transforms inference economics.
2. **Serving Engine Visualizations:** Architectural diagrams dissecting token generation loops, prefill vs. decode phase splits, and distributed tensor parallelism.
3. **Executable Systems Code:** Python and CUDA/Triton kernels, serving configurations, and containerized deployment specs with health checks and GPU resource pinning.
4. **Latency vs. Accuracy Trade-offs:** Detailed comparative tables on quantization formats (FP16, INT8, INT4, AWQ, GPTQ) and speculative decoding verification budgets.

---

## Curriculum Roadmap

```
+--------------------------------------------------------------------------+
|                       AI SERVING CURRICULUM ROADMAP                      |
+--------------------------------------------------------------------------+
|  01. PagedAttention & KV-Cache Memory Management                         |
|      (Virtual Memory Paging, vLLM Engine, Block Allocations, Fragmentation)
|                                                                          |
|  02. Speculative Decoding & Draft Model Serving                          |
|      (Speculative Sampling, Tree Attention, Acceptance Thresholds)       |
|                                                                          |
|  03. Continuous Batching & In-Flight Request Scheduling                  |
|      (Static vs Dynamic Batching, Iteration-Level Scheduling, Starvation)|
|                                                                          |
|  04. Quantization Architectures & Kernel Acceleration                    |
|      (AWQ, GPTQ, SmoothQuant, FlashAttention-2/3, Triton Kernels)       |
|                                                                          |
|  05. Distributed Tensor & Pipeline Parallelism Serving                   |
|      (NCCL, Megatron-LM Spans, Inter-GPU Comm, Ray Serve Clustering)     |
+--------------------------------------------------------------------------+
```

---

## Active & Upcoming Modules

| Module Slug | Status | Focus Areas | Key Artifacts |
| :--- | :--- | :--- | :--- |
| `01-paged-attention-kv-cache` | *Planned* | Non-contiguous memory allocation, PagedAttention vLLM | Python vLLM config, cache benchmark suite |
| `02-speculative-decoding-serving` | *Planned* | Draft-verifier pipeline, speculative acceptance rates | Python verification loop, latency profiler |
| `03-continuous-batching-scheduling`| *Planned* | Dynamic iteration scheduling, TTFT vs TPOT optimization | Triton model repository, client benchmark |
| `04-quantization-awq-gptq` | *Planned* | Weight-only vs weight-activation quantization | vLLM quantization launch configs |
| `05-distributed-inference-ray` | *Planned* | Tensor parallelism over RoCE/InfiniBand | RayCluster manifest, multi-GPU deployment |

---

## Prerequisites & Tooling

- Solid foundation in Python 3.10+ and asynchronous programming (`asyncio`).
- Understanding of transformer architectures (self-attention mechanism, query-key-value projections).
- Familiarity with PyTorch tensors and CUDA runtime basics.
- Recommended lab setup: NVIDIA GPU environment (A10G, T4, L4, or local RTX) or cloud GPU instances (RunPod, Lambda, AWS EC2).
