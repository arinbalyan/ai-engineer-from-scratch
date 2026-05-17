## Lesson 05: Jupyter Notebooks

### What I Learned

Jupyter notebooks are the standard scratch pad for AI engineering. The key insight is the cell-based architecture: a noteboook is a list of cells (code or markdown), all sharing a single kernel (a Python process that keeps variables in memory between cells).

The superpower is iteration speed -- run one cell, see the output, tweak, run again. The foot-gun is out-of-order execution: running cells in non-linear order creates hidden state that breaks when someone runs the notebook top-to-bottom.

### Key Distinctions

- Notebooks vs scripts: "explore in notebooks, ship in scripts." Notebooks for prototyping, visualization, and explanation. Scripts for reusable code, training pipelines, and production.
- JupyterLab vs Notebook vs VS Code: same `.ipynb` format, different interfaces. JupyterLab is the most common in AI work.
- `%timeit` vs `%%time`: `%timeit` runs many times and averages (microbenchmarks), `%%time` runs once (training runs).

### Tools & Commands

- Launch: `uv run jupyter lab --no-browser` (already configured as `pnpm dev`)
- Colab is also available at colab.research.google.com with free T4 GPU
- `.ipynb` files are JSON under the hood

### Common Traps

1. Out-of-order execution -- always do Kernel > Restart & Run All before sharing
2. Hidden state -- deleted cells can leave variables in memory
3. Memory leaks -- large datasets accumulate across cells; restart the kernel regularly

### Useful Commands from the Lesson

- `%timeit` -- microbenchmark (runs many times, averages)
- `%%time` -- wall clock for a cell
- `%matplotlib inline` -- renders plots inline
- `!pip install ...` -- install packages from within a notebook
- `%env VAR` -- check environment variables
- `Shift+Enter` -- run cell and move to next (the most-used shortcut)
