# Curriculum Structure Notes

## How lessons are organized

Each lesson follows the same layout:

```
phases/<NN>-<phase>/<NN>-<lesson>/
  code/       - actual implementations
  docs/       - lesson writeups
  outputs/    - prompts, skills, agents, MCP servers
```

This is consistent across all 20 phases. The idea is you build something from scratch first, then use the production library, then ship a reusable artifact.

## Build It / Use It pattern

Most lessons have two parts:

- **Build It** — implement the algorithm from raw math, no frameworks. This is where you actually understand what's happening.
- **Use It** — do the same thing with PyTorch, sklearn, or whatever the production tool is.

The curriculum is opinionated about this order. Don't skip the Build It part even if it's tempting.

## Phase 0 is setup only

Phase 0 has 12 lessons but they're all about environment preparation. No real AI content yet. The actual curriculum starts at Phase 1 (Math Foundations).

## Languages per phase

- Python dominates Phases 1-12 (ML, DL, NLP, Vision, Audio, LLMs)
- TypeScript takes over Phases 13-17 (tools, agents, infrastructure)
- Rust appears in performance-critical lessons throughout
- Julia is mostly Phase 1 (math foundations)

## Artifacts

Every lesson produces something reusable — a prompt, a skill definition, an agent loop, or an MCP server. These go in `outputs/` and are meant to be installed into actual tools, not just left as homework.
