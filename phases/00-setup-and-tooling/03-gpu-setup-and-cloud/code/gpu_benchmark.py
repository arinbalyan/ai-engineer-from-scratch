"""GPU vs CPU benchmark — matrix multiplication speedup.

Compares a 5000x5000 matrix multiply on CPU vs GPU.
Run with: uv run phases/00-setup-and-tooling/03-gpu-setup-and-cloud/code/gpu_benchmark.py
"""

import torch
import time


def benchmark_matmul(size: int = 5000) -> None:
    a_cpu = torch.randn(size, size)
    b_cpu = torch.randn(size, size)

    # CPU
    torch.set_num_threads(torch.get_num_threads())
    start = time.time()
    c_cpu = a_cpu @ b_cpu
    cpu_time = time.time() - start
    print(f"CPU ({torch.get_num_threads()} threads): {cpu_time:.3f}s")

    if not torch.cuda.is_available():
        print("No GPU available. Skipping GPU benchmark.")
        return

    # GPU
    a_gpu = a_cpu.to("cuda")
    b_gpu = b_cpu.to("cuda")

    torch.cuda.synchronize()
    start = time.time()
    c_gpu = a_gpu @ b_gpu
    torch.cuda.synchronize()
    gpu_time = time.time() - start
    print(f"GPU ({torch.cuda.get_device_name(0)}): {gpu_time:.3f}s")
    print(f"Speedup: {cpu_time / gpu_time:.0f}x")


if __name__ == "__main__":
    benchmark_matmul()
