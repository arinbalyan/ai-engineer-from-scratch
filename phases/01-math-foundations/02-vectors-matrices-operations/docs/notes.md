# Vectors, Matrices & Operations

> Every neural network is just matrix multiplication with extra steps.

## What I Built

| Step | What | Library |
|------|------|---------|
| 1 | Element-wise vs matrix multiply | Pure Python |
| 2 | Transpose, determinant, inverse | Pure Python |
| 3 | Dense neural network layer (relu(Wx + b)) | Pure Python |
| 4 | NumPy equivalents (linalg, broadcasting) | NumPy |
| 5 | Native Julia versions (no custom classes) | Julia |

## To Run

```bash
uv run phases/01-math-foundations/02-vectors-matrices-operations/code/vectors_matrices_operations.py

julia --project=languages/julia phases/01-math-foundations/02-vectors-matrices-operations/code/vectors_matrices_operations.jl
```
