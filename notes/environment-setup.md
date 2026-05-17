# Environment Setup Notes

## uv is fast but the lock file matters

uv resolves and installs way faster than pip, which is nice. But the first sync with PyTorch + CUDA takes a while because the NVIDIA wheels are huge — over 1.5 GB combined. After that everything is cached and subsequent syncs are instant.

The `uv.lock` file should be committed. It pins exact versions so the environment is reproducible across machines.

## Python version pinning

The `.python-version` file tells uv which Python to use. Pinned to 3.12 because it's the most stable for the AI/ML ecosystem right now. 3.13 works for most things but some libraries still lag behind.

## GPU setup

NVIDIA driver 591.74, CUDA 13.1 on this machine. GTX 1650 Ti with 4GB VRAM. Not a lot of memory for training but fine for learning and running inference on smaller models.

PyTorch was installed with the cu124 index URL. It works fine even though the system has CUDA 13.1 — PyTorch bundles its own CUDA runtime so it doesn't need the system CUDA toolkit.

## Julia installation

Juliaup is the recommended installer. It manages Julia versions similar to how rustup manages Rust. The binary goes in `~/.juliaup/bin/` and needs to be on PATH. Symlinked to `~/.local/bin/julia` so it works without modifying shell config files.

## pnpm via corepack

corepack ships with Node 20+ and manages package manager versions. Enabled pnpm through it instead of installing globally. The `packageManager` field in `package.json` pins the exact version so everyone on the project uses the same one.

## Isolation is the priority

Nothing was installed globally. Python stays in `.venv/`, Node uses workspace-level `node_modules/`, Rust and Julia have their own project directories. This means the system Python and system packages are untouched.
