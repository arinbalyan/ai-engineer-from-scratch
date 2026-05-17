# Lesson 12: Debugging and Profiling

**Type:** Build | **Language:** Python | **Time:** ~60 min

## What I Learned

AI bugs are different from web-app bugs. A misconfigured training loop runs for hours
producing a beautiful loss curve on garbage. No crash, no stack trace.

Three levels of AI debugging:
1. Standard Python -- breakpoints, logging, profiling, memory
2. Tensor Operations -- shapes, dtypes, devices, NaN/Inf
3. Training Dynamics -- loss curves, gradient norms, activations

80% of AI bugs live at levels 1 and 2.

## Techniques Covered

| Technique | Tool | When to Use |
|-----------|------|-------------|
| Print debugging | `debug_print()` | Quick shape/dtype/value checks |
| Conditional breakpoint | `breakpoint()` | Stop only when loss spikes or NaN |
| Logging | `logging` module | Persistent records with timestamps |
| Timing | `Timer` context manager | Find slow sections (data loading is #1) |
| Function profiling | `cProfile` | Find slowest function calls |
| Line profiling | `line_profiler` / `kernprof` | Line-by-line time breakdown |
| CPU memory | `tracemalloc` / `memory_profiler` | Find memory hogs in data pipeline |
| GPU memory | `torch.cuda.memory_*` | Diagnose OOM, reduce batch size |
| Shape checks | Forward hooks | Verify every layer's in/out dims |
| NaN detection | `torch.isnan()` + grad check | Find exploding gradients |
| Device check | Compare `.device` | Catch silent CPU fallback |
| TensorBoard | `SummaryWriter` | Visualize loss, weights, gradients |

## Common AI Bug Checklist

- [x] Shape mismatch? Run `check_shapes` with a sample batch.
- [x] NaN loss? Check LR, log(0), division by zero, exploding grads.
- [x] 99% test accuracy? Check data leakage -- train/test overlap.
- [x] Training slow? Profile; data loading is likely the bottleneck.
- [x] OOM? Reduce batch size first. Then try AMP or gradient checkpointing.

## Arch / Environment Notes

- All commands run via `uv run python3 ...` (not bare `python3`)
- TensorBoard: `uv run tensorboard --logdir=<path>`
- cProfile: `uv run python3 -m cProfile -s cumtime <script>`
- line_profiler: `uv run kernprof -l -v <script>`
- GPU: GTX 1650 Ti, 4 GB VRAM, CUDA 13.0
- LSP errors on torch/tensorboard imports are false positives (uv venv not indexed)
