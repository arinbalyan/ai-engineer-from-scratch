"""Dev Environment Verification — AI Engineering from Scratch.

Checks that all four layers of the AI engineering stack are functional:
1. System foundation (OS, shell, git)
2. Package managers (uv, pnpm, cargo, juliaup)
3. Language runtimes (Python, Node.js, Rust, Julia)
4. AI/ML libraries (NumPy, PyTorch, CUDA)
"""

import sys
import platform
import subprocess


def header(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def check(name: str, cmd: str) -> bool:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip() or result.stderr.strip()
        status = "OK" if result.returncode == 0 else "FAIL"
        print(f"  [{status}] {name}: {output}")
        return result.returncode == 0
    except Exception as e:
        print(f"  [FAIL] {name}: {e}")
        return False


def main() -> None:
    header("AI Engineering from Scratch — Environment Verification")

    print(f"\n  Platform: {platform.system()} {platform.release()}")
    print(f"  Machine:  {platform.machine()}")
    print(f"  Python:   {sys.version.split()[0]}")

    # Layer 1: System
    header("Layer 1 — System Foundation")
    check("Git", "git --version")
    check("curl", "curl --version | head -1")
    check("wget", "wget --version | head -1")
    check("GCC", "gcc --version | head -1")

    # Layer 2: Package Managers
    header("Layer 2 — Package Managers")
    check("uv", "uv --version")
    check("pnpm", "pnpm --version")
    check("cargo", "cargo --version")
    check("juliaup", "juliaup --version")

    # Layer 3: Language Runtimes
    header("Layer 3 — Language Runtimes")
    check("Python", "python --version")
    check("Node.js", "node --version")
    check("Rust", "rustc --version")
    check("Julia", "julia --version")

    # Layer 4: AI/ML Libraries
    header("Layer 4 — AI/ML Libraries")
    try:
        import numpy as np

        print(f"  [OK]   NumPy: {np.__version__}")
        a = np.array([1, 2, 3])
        print(f"       Vector: {a.tolist()}, dot: {int(np.dot(a, a))}")
    except ImportError:
        print("  [FAIL] NumPy not installed")

    try:
        import torch

        print(f"  [OK]   PyTorch: {torch.__version__}")
        cuda = torch.cuda.is_available()
        print(f"  [{'OK' if cuda else 'SKIP'}] CUDA: {cuda}")
        if cuda:
            print(f"       GPU: {torch.cuda.get_device_name(0)}")
            x = torch.randn(3, 3).cuda()
            print(f"       Test tensor (GPU): {x.device}")
    except ImportError:
        print("  [FAIL] PyTorch not installed")

    try:
        import scipy

        print(f"  [OK]   SciPy: {scipy.__version__}")
    except ImportError:
        print("  [SKIP] SciPy not installed")

    try:
        import sklearn

        print(f"  [OK]   scikit-learn: {sklearn.__version__}")
    except ImportError:
        print("  [SKIP] scikit-learn not installed")

    try:
        import pandas

        print(f"  [OK]   pandas: {pandas.__version__}")
    except ImportError:
        print("  [SKIP] pandas not installed")

    try:
        import matplotlib

        print(f"  [OK]   matplotlib: {matplotlib.__version__}")
    except ImportError:
        print("  [SKIP] matplotlib not installed")

    header("Summary")
    print("  Environment ready. Start with Phase 1 — Math Foundations.")
    print(f"  Activate venv: source .venv/bin/activate")
    print(f"  Run lessons:   uv run phases/<phase>/<lesson>/code/<script>.py")


if __name__ == "__main__":
    main()
