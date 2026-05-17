# Linear Algebra Intuition

> "Every AI model is just matrix math wearing a fancy hat."

## What I Built

From-scratch Vector and Matrix classes covering the full pipeline:

| Step | What | Library |
|------|------|---------|
| 1-3 | Vector ops (add, dot, norm, cosine, angle) | Pure Python |
| 4-6 | Matrix ops (matmul, transpose, rank) | Pure Python |
| 7 | Linear independence detection | Pure Python (row reduction) |
| 8 | Projection onto a vector | Pure Python |
| 9 | Gram-Schmidt orthogonalization | Pure Python |
| 10 | NumPy equivalents (linalg.norm, matrix_rank, QR) | NumPy |
| 11 | PyTorch tensors with autodiff | PyTorch |

## Key Intuitions

- **Dot product** = similarity measure (positive = same direction, zero = unrelated, negative = opposite)
- **Matrix multiply** = transformation (every neural network layer is Wx + b)
- **Rank** = number of independent dimensions (rank deficiency = redundant features)
- **Projection** = the component of one vector in another's direction (foundation of least squares)
- **Gram-Schmidt** = converting a basis into an orthonormal one (QR decomposition)

## How This Connects to AI

| Concept | Real usage |
|---------|-----------|
| Dot product | Attention scores in transformers, cosine similarity in RAG |
| Matrix multiply | Every neural network layer |
| Rank | LoRA (low-rank adaptation of LLMs) |
| Projection | Linear regression, PCA |
| Orthonormal basis | Stable numerics, whitening transforms |

## To Run

```bash
uv run phases/01-math-foundations/01-linear-algebra-intuition/code/linear_algebra_intuition.py
```
