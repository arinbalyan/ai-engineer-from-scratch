"""VRAM estimation — how big a model fits in your GPU.

Rule of thumb: 2 bytes per parameter for fp16, 4 bytes for fp32.
Accounts for optimizer state (Adam uses ~3x model size in additional memory).

Run with: uv run phases/00-setup-and-tooling/03-gpu-setup-and-cloud/code/vram_estimate.py
"""

import torch


def estimate_vram() -> None:
    if not torch.cuda.is_available():
        print("No GPU available.")
        return

    props = torch.cuda.get_device_properties(0)
    total_bytes = props.total_memory
    total_gb = total_bytes / (1024**3)
    name = props.name

    print(f"GPU: {name}")
    print(f"Total VRAM: {total_gb:.2f} GB")
    print()

    # PyTorch reserves some VRAM at startup
    reserved = torch.cuda.memory_reserved()
    usable_gb = (total_bytes - reserved) / (1024**3)
    print(f"Usable VRAM (after PyTorch init): {usable_gb:.2f} GB")
    print()

    # Model size estimates
    print("Maximum model size that fits in VRAM:")
    print("-" * 50)

    for dtype, bytes_per_param in [("fp32", 4), ("fp16/bf16", 2), ("int8", 1), ("int4", 0.5)]:
        params = (usable_gb * 1024**3) / bytes_per_param
        if params >= 1e9:
            print(f"  {dtype:>10}: {params / 1e9:.1f}B parameters")
        else:
            print(f"  {dtype:>10}: {params / 1e6:.0f}M parameters")

    print()

    # Adam optimizer requires extra memory (grads + 2 momentum buffers)
    # Roughly 3x model size for training
    print("For training (Adam optimizer, ~3x overhead):")
    print("-" * 50)
    for dtype, bytes_per_param in [("fp32", 4), ("fp16/bf16", 2)]:
        effective = bytes_per_param * 4  # params + grads + 2 momentum buffers
        params = (usable_gb * 1024**3) / effective
        if params >= 1e9:
            print(f"  {dtype:>10}: {params / 1e9:.1f}B parameters")
        else:
            print(f"  {dtype:>10}: {params / 1e6:.0f}M parameters")


if __name__ == "__main__":
    estimate_vram()
