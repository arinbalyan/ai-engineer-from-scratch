#!/usr/bin/env python3
"""Debugging and Profiling Toolkit for AI Workloads.

Covers all techniques from the lesson:
  1. debug_print helper
  2. Timer context manager
  3. tracemalloc memory profiling
  4. GPU memory queries
  5. Shape-check hooks
  6. NaN/Inf detection
  7. Device mismatch detection
  8. TensorBoard logging
  9. cProfile (run via: uv run python3 -m cProfile -s cumtime debug_tools.py)
 10. line_profiler (run via: uv run kernprof -l -v debug_tools.py)

Run: uv run python3 phases/00-setup-and-tooling/12-debugging-and-profiling/code/debug_tools.py
"""

import logging
import time
import tracemalloc
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F

# ---------------------------------------------------------------------------
# Part 1: debug_print -- one-liner for tensor inspection
# ---------------------------------------------------------------------------

def debug_print(name, tensor):
    print(
        f"[DEBUG] {name}: shape={tuple(tensor.shape)}, "
        f"dtype={tensor.dtype}, device={tensor.device}, "
        f"min={tensor.min().item():.4f}, max={tensor.max().item():.4f}, "
        f"mean={tensor.mean().item():.4f}, "
        f"has_nan={tensor.isnan().any().item()}"
    )

# ---------------------------------------------------------------------------
# Part 4: Timer context manager
# ---------------------------------------------------------------------------

class Timer:
    def __init__(self, name=""):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        elapsed = time.perf_counter() - self.start
        print(f"[TIMER] {self.name}: {elapsed:.4f}s")

# ---------------------------------------------------------------------------
# Part 3: Logging setup  (also used by the timed-training demo)
# ---------------------------------------------------------------------------

def setup_logger(log_path: Path):
    logger = logging.getLogger("debug_tools")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)

    logger.handlers.clear()
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

# ---------------------------------------------------------------------------
# A tiny model for the demonstrations
# ---------------------------------------------------------------------------

class DummyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(64, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# ---------------------------------------------------------------------------
# Part 7: Shape-check hooks
# ---------------------------------------------------------------------------

def check_shapes(model, sample_input):
    print("\n=== Shape-Check Hooks ===")
    print(f"Input: {tuple(sample_input.shape)}")
    hooks = []

    def make_hook(name):
        def hook(module, inp, out):
            in_shape = tuple(inp[0].shape) if isinstance(inp, tuple) else tuple(inp.shape)
            out_shape = tuple(out.shape) if hasattr(out, "shape") else type(out).__name__
            print(f"  {name}: {in_shape} -> {out_shape}")
        return hook

    for name, module in model.named_modules():
        if name:
            hooks.append(module.register_forward_hook(make_hook(name)))

    with torch.no_grad():
        model(sample_input)

    for h in hooks:
        h.remove()

# ---------------------------------------------------------------------------
# Part 7: NaN / Inf gradient detection
# ---------------------------------------------------------------------------

def detect_nan(model, loss, step):
    if torch.isnan(loss) or torch.isinf(loss):
        print(f"\n  [!] NaN/Inf loss at step {step}")
        for name, param in model.named_parameters():
            if param.grad is not None:
                if torch.isnan(param.grad).any():
                    print(f"      NaN gradient in {name}")
                if torch.isinf(param.grad).any():
                    print(f"      Inf gradient in {name}")
        return True
    return False

# ---------------------------------------------------------------------------
# Part 7: Device mismatch detection
# ---------------------------------------------------------------------------

def check_devices(model, *tensors):
    print("\n=== Device Check ===")
    model_device = next(model.parameters()).device
    print(f"  Model device: {model_device}")
    for i, t in enumerate(tensors):
        dev = t.device
        status = "OK" if dev == model_device else "WARNING: MISMATCH"
        print(f"  tensor {i}: {dev}  [{status}]")

# ---------------------------------------------------------------------------
# Part 8: TensorBoard writer
# ---------------------------------------------------------------------------

def tensorboard_demo(log_dir: Path, num_steps: int = 50):
    from torch.utils.tensorboard import SummaryWriter

    print(f"\n=== TensorBoard Demo ===")
    print(f"  Logs -> {log_dir}")
    print(f"  View: uv run tensorboard --logdir={log_dir}")

    model = DummyModel()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    writer = SummaryWriter(str(log_dir))

    for step in range(num_steps):
        x = torch.randn(16, 64)
        y = torch.randint(0, 10, (16,))
        out = model(x)
        loss = F.cross_entropy(out, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        writer.add_scalar("loss/train", loss.item(), step)
        writer.add_scalar("lr", optimizer.param_groups[0]["lr"], step)

        if step % 10 == 0:
            for name, param in model.named_parameters():
                writer.add_histogram(f"weights/{name}", param, step)
                if param.grad is not None:
                    writer.add_histogram(f"grads/{name}", param.grad, step)

    writer.close()
    print("  Done. Run tensorboard --logdir=<path> to view.")

# ===================================================================
# Main
# ===================================================================

def main():
    lesson_dir = Path(__file__).parent.parent
    outputs_dir = lesson_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 56)
    print("  Debugging & Profiling Toolkit")
    print("=" * 56)

    # ------------------------------------------------------------------
    # Part 1: debug_print
    # ------------------------------------------------------------------
    print("\n--- Part 1: debug_print ---")
    x = torch.randn(8, 3, 64, 64)
    w = torch.randn(16, 3, 3, 3)
    out = F.conv2d(x, w)
    debug_print("conv2d output", out)

    # ------------------------------------------------------------------
    # Part 4: Timer
    # ------------------------------------------------------------------
    print("\n--- Part 4: Timer ---")
    big = torch.randn(2000, 2000)
    with Timer("matmul"):
        for _ in range(50):
            big = big @ big

    # ------------------------------------------------------------------
    # Part 6a: tracemalloc
    # ------------------------------------------------------------------
    print("\n--- Part 6: tracemalloc ---")
    tracemalloc.start()
    big_list = [torch.randn(100, 100) for _ in range(100)]
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")
    print("  Top 3 allocation lines:")
    for stat in top_stats[:3]:
        print(f"    {stat}")
    del big_list

    # ------------------------------------------------------------------
    # Part 6b: GPU memory
    # ------------------------------------------------------------------
    print("\n--- Part 6b: GPU Memory ---")
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"  Device: {torch.cuda.get_device_name(0)}")
        print(f"  Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
        print(f"  Reserved:  {torch.cuda.memory_reserved() / 1e9:.2f} GB")

        a = torch.randn(1000, 1000, device=device)
        b = torch.randn(1000, 1000, device=device)
        c = a @ b
        print(f"  After alloc:  {torch.cuda.memory_allocated() / 1e9:.2f} GB")

        del a, b, c
        torch.cuda.empty_cache()
        print(f"  After empty_cache: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
    else:
        print("  No CUDA device available (skipping GPU memory demo)")

    # ------------------------------------------------------------------
    # Part 7a: Shape-check hooks
    # ------------------------------------------------------------------
    model = DummyModel()
    sample = torch.randn(4, 64)
    check_shapes(model, sample)

    # ------------------------------------------------------------------
    # Part 7b: NaN detection
    # ------------------------------------------------------------------
    print("\n=== NaN Detection Demo ===")
    normal_loss = torch.tensor(2.5)
    print(f"  Normal loss: {normal_loss.item():.4f} -> no alarm")

    nan_loss = torch.tensor(float("nan"))
    detect_nan(model, nan_loss, step=42)

    inf_loss = torch.tensor(float("inf"))
    detect_nan(model, inf_loss, step=99)

    # ------------------------------------------------------------------
    # Part 7c: Device check
    # ------------------------------------------------------------------
    cpu_tensor = torch.randn(4, 64)
    gpu_tensor = torch.randn(4, 64).cuda() if torch.cuda.is_available() else cpu_tensor
    check_devices(model, cpu_tensor, gpu_tensor)

    # ------------------------------------------------------------------
    # Part 3 + mini training loop with logging
    # ------------------------------------------------------------------
    print("\n--- Part 3: Logged Training Loop ---")
    log_path = outputs_dir / "training.log"
    logger = setup_logger(log_path)
    logger.info("Starting demo training (5 steps)")

    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    for step in range(5):
        x = torch.randn(16, 64)
        y = torch.randint(0, 10, (16,))
        out = model(x)
        loss = F.cross_entropy(out, y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        logger.info(f"step={step:2d}  loss={loss.item():.4f}")

    print(f"  Log written to: {log_path}")

    # ------------------------------------------------------------------
    # Part 8: TensorBoard
    # ------------------------------------------------------------------
    tb_dir = outputs_dir / "runs" / "demo"
    tensorboard_demo(tb_dir, num_steps=30)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 56)
    print("  All debugging tools demonstrated successfully.")
    print("=" * 56)
    print("\n  To view TensorBoard:")
    print(f"    uv run tensorboard --logdir={outputs_dir / 'runs'}")
    print("\n  To run cProfile:")
    print("    uv run python3 -m cProfile -s cumtime \\")
    print(f"      {Path(__file__).name} 2>&1 | head -30")
    print("\n  To run line_profiler:")
    print("    uv run kernprof -l -v \\")
    print(f"      {Path(__file__).name}")
    print("    (then: uv run python3 -m line_profiler debug_tools.py.lprof)")


if __name__ == "__main__":
    main()
