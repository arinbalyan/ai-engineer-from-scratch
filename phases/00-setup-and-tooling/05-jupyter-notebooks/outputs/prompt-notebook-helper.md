## Prompt: Notebook Debugging Helper

Use this prompt when an AI assistant needs to help debug a Jupyter notebook issue. It provides essential context about notebook-specific failure modes.

```
I am working in a Jupyter notebook and running into issues. The notebook (.ipynb) 
is a JSON file with cells (code or markdown) that all share a single Python 
kernel process.

Before suggesting fixes, consider these notebook-specific failure modes:

1. **Out-of-order execution** -- Cells may have been run in non-linear order. 
   A variable may exist because of hidden execution history, not the order 
   cells appear. Ask me to run Kernel > Restart & Run All first.

2. **Hidden state** -- Deleting a cell does NOT delete the variables it created. 
   The kernel still holds them. Ask me to restart the kernel if I see stale 
   or unexpected values.

3. **Namespace pollution** -- Previous experiments may have left variables, 
   imports, or function definitions that conflict with current code. Restart 
   the kernel for a clean slate.

4. **Memory pressure** -- Large arrays and models accumulate across cells. 
   Python's garbage collector may not free memory promptly. Suggest 
   `del variable` and `gc.collect()` or a kernel restart.

5. **Matplotlib backend** -- If plots don't show inline, I may need 
   `%matplotlib inline` before plotting.

6. **Modified modules** -- If I import a .py file and then edit it, the 
   kernel still has the old version. I need `import importlib; importlib.reload(mod)` 
   or a kernel restart.

7. **`!pip install`** -- Packages installed via `!pip install` in a cell 
   affect the kernel's Python environment immediately, but a kernel restart 
   is still needed for some C-extensions to load properly.

Please start your debugging by asking me to run Kernel > Restart & Run All 
to eliminate hidden state, then walk through the cells in order.
