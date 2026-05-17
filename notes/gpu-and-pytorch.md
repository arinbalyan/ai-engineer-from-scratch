# GPU and PyTorch Notes

## GTX 1650 Ti limitations

4GB VRAM is the main bottleneck. Some things that won't fit:

- Training anything over ~100M parameters
- Running LLMs larger than 3B without heavy quantization
- Large batch sizes for image models

What works fine:

- Inference on small/medium models
- Training small CNNs and MLPs
- All the curriculum lessons up to Phase 10 or so

## CUDA version mismatch is normal

System has CUDA 13.1 but PyTorch was installed with cu124 wheels. This is fine because PyTorch ships its own CUDA runtime libraries. It doesn't use the system CUDA toolkit at all. The only thing that matters is the NVIDIA driver version, which is backward compatible.

## Checking GPU usage

```python
import torch
torch.cuda.is_available()       # True means GPU is working
torch.cuda.get_device_name(0)   # Shows which GPU
torch.cuda.memory_allocated()   # Current VRAM usage in bytes
```

If CUDA isn't available, PyTorch will silently fall back to CPU. Code still runs, just slower.

## MPS on Apple Silicon

If running on a Mac with M1/M2/M3, use `mps` instead of `cuda`:

```python
device = "mps" if torch.backends.mps.is_available() else "cpu"
```

Same pattern — PyTorch handles the device abstraction, code stays the same.
