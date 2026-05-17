# GPU Setup Notes

## Current GPU

NVIDIA GTX 1650 Ti with 4GB VRAM. Driver 591.74, CUDA 13.1 on the system.

## PyTorch CUDA version

PyTorch was installed with cu124 wheels. It bundles its own CUDA runtime so it doesn't need the system CUDA toolkit. The driver is backward compatible so cu124 works fine on a CUDA 13.1 system.

## VRAM is the bottleneck

4GB is tight. Rule of thumb:

- Inference (fp16): models up to ~2B parameters fit
- Inference (fp32): models up to ~1B parameters fit
- Training with Adam: multiply model size by ~4 (params + grads + 2 momentum buffers). So training caps out around 200-300M parameters in fp16.

The `vram_estimate.py` script in this lesson's code folder calculates exact numbers at runtime.

## Google Colab fallback

For anything that doesn't fit locally, Colab free tier gives a T4 with 16GB VRAM. That's enough for models up to ~8B parameters in fp16 for inference, or ~2B for training.

## Benchmark script

The `gpu_benchmark.py` script runs a 5000x5000 matrix multiply on CPU and GPU and prints the speedup. On this machine the GPU should be roughly 10-30x faster for this operation.

## Device selection pattern

Every script that uses PyTorch should use this pattern:

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
```

Code should never hardcode "cuda" — it must fall back to CPU silently.
