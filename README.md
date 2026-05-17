# AI Engineering from Scratch

Local workspace for the [AI Engineering from Scratch](https://aiengineeringfromscratch.com) curriculum. 20 phases, 4 languages, fully isolated environment.

## Setup

### Prerequisites

- Linux, macOS, or WSL2
- Git installed

### Install

```bash
git clone https://github.com/YOUR_USERNAME/ai-engineering.git
cd ai-engineering
```

### Python

Uses `uv` for fast, isolated package management. Nothing installs globally.

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and populate the virtual environment
uv sync
```

All Python dependencies stay inside `.venv/`.

### Node.js

Uses `corepack` (ships with Node) and `pnpm`. No global installs.

```bash
corepack enable
pnpm install
```

### Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

The Rust project lives in `languages/rust/`.

### Julia

```bash
curl -fsSL https://install.julialang.org | sh
```

The Julia project lives in `languages/julia/`.

## Quick Start

```bash
# Verify all four languages are working
echo "=== Python ===" && uv run python languages/python/hello.py && \
echo "=== Node.js ===" && node languages/node/hello.mjs && \
echo "=== Rust ===" && cd languages/rust && cargo run && \
echo "=== Julia ===" && cd ../julia && julia --project=. -e 'println("Julia ready")'

# Run the environment verification script
uv run phases/00-setup-and-tooling/01-dev-environment/code/verify.py

# Run any Python lesson
uv run phases/<phase>/<lesson>/code/<script>.py

# Run a Node.js lesson
pnpm exec node languages/node/<script>.mjs

# Run a Rust lesson
cd languages/rust && cargo run

# Run a Julia lesson
cd languages/julia && julia --project=. <script>.jl
```

## Directory Structure

```
phases/
  <NN>-<phase-name>/
    <NN>-<lesson-name>/
      code/       - runnable implementations
      docs/       - lesson notes
      outputs/    - artifacts (prompts, skills, agents)
languages/
  python/         - standalone Python scripts
  node/           - Node.js / TypeScript code
  rust/           - Cargo project
  julia/          - Julia project
notes/            - personal findings and observations
```

## API Keys and Secrets

Secrets live in `~/.config/ai-eng/secrets.json` — never in the repo.

```json
{
  "huggingface": "hf_...",
  "openrouter": "sk-or-..."
}
```

A helper module at `languages/python/utils/secrets.py` reads them:

```python
import sys; sys.path.insert(0, "languages/python")
from utils.secrets import get_huggingface_key, get_openrouter_key

hf_token = get_huggingface_key()
or_token = get_openrouter_key()
```

Add your keys once, all lessons use them. To add a new key, edit `~/.config/ai-eng/secrets.json` and add a getter to `secrets.py`.

### Default Model

We use OpenRouter's free tier with `openai/gpt-oss-120b:free`. Change the model in `~/.config/ai-eng/secrets.json`:

```json
{
  "default_model": "openai/gpt-oss-120b:free"
}
```

## Notes

See the `notes/` directory for findings, gotchas, and observations from working through the curriculum.

## License

MIT
