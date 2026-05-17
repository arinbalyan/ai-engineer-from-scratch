"""Linear Algebra Intuition — from scratch through NumPy to PyTorch.

Teaches: vectors as points, dot product as similarity, matrices as
transformations, linear independence, rank, projection, Gram-Schmidt.
"""

import math
import random


# ============================================================
# 1. VECTORS FROM SCRATCH
# ============================================================

class Vector:
    def __init__(self, components):
        self.components = list(components)
        self.dim = len(self.components)

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.components, other.components)])

    def dot(self, other):
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        return math.sqrt(sum(x ** 2 for x in self.components))

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            return Vector(self.components)
        return Vector([x / mag for x in self.components])

    def cosine_similarity(self, other):
        m = self.magnitude() * other.magnitude()
        return self.dot(other) / m if m != 0 else 0.0

    def angle_between(self, other):
        cs = self.cosine_similarity(other)
        cs = max(-1.0, min(1.0, cs))
        return math.degrees(math.acos(cs))

    def __repr__(self):
        return f"Vector({self.components})"


# ============================================================
# 2. MATRICES FROM SCRATCH
# ============================================================

class Matrix:
    def __init__(self, rows):
        self.rows = [list(r) for r in rows]
        self.shape = (len(self.rows), len(self.rows[0]))

    def __matmul__(self, other):
        if isinstance(other, Vector):
            return Vector([
                sum(self.rows[i][j] * other.components[j] for j in range(self.shape[1]))
                for i in range(self.shape[0])
            ])
        rows = []
        for i in range(self.shape[0]):
            row = []
            for j in range(other.shape[1]):
                row.append(sum(
                    self.rows[i][k] * other.rows[k][j]
                    for k in range(self.shape[1])
                ))
            rows.append(row)
        return Matrix(rows)

    def transpose(self):
        return Matrix([
            [self.rows[j][i] for j in range(self.shape[0])]
            for i in range(self.shape[1])
        ])

    def rank(self):
        rows = [row[:] for row in self.rows]
        num_rows, num_cols = self.shape
        rank = 0
        for col in range(num_cols):
            pivot = None
            for row in range(rank, num_rows):
                if abs(rows[row][col]) > 1e-10:
                    pivot = row
                    break
            if pivot is None:
                continue
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            scale = rows[rank][col]
            rows[rank] = [x / scale for x in rows[rank]]
            for row in range(num_rows):
                if row != rank and abs(rows[row][col]) > 1e-10:
                    factor = rows[row][col]
                    rows[row] = [
                        rows[row][j] - factor * rows[rank][j]
                        for j in range(num_cols)
                    ]
            rank += 1
        return rank

    def __repr__(self):
        return f"Matrix({self.rows})"


# ============================================================
# 3. LINEAR INDEPENDENCE, PROJECTION, GRAM-SCHMIDT
# ============================================================

def is_linearly_independent(vectors):
    n = len(vectors)
    mat = Matrix([v.components[:] for v in vectors])
    return mat.rank() == n


def project(a, b):
    scalar = a.dot(b) / b.dot(b)
    return Vector([scalar * x for x in b.components])


def gram_schmidt(vectors):
    orthonormal = []
    for v in vectors:
        w = v
        for u in orthonormal:
            w = w - project(w, u)
        if w.magnitude() < 1e-10:
            continue
        orthonormal.append(w.normalize())
    return orthonormal


# ============================================================
# 4. DEMONSTRATION
# ============================================================

print("=" * 60)
print("PART 1: VECTORS FROM SCRATCH")
print("=" * 60)

a = Vector([1, 2, 3])
b = Vector([4, 5, 6])

print(f"a = {a}")
print(f"b = {b}")
print(f"a + b  = {a + b}")
print(f"a - b  = {a - b}")
print(f"a . b  = {a.dot(b)}")
print(f"|a|    = {a.magnitude():.4f}")
print(f"cosine = {a.cosine_similarity(b):.4f}")
print(f"angle  = {a.angle_between(b):.2f} degrees")

print()
print("=" * 60)
print("PART 2: MATRICES FROM SCRATCH")
print("=" * 60)

rotation_90 = Matrix([[0, -1], [1, 0]])
point = Vector([3, 1])
rotated = rotation_90 @ point
print(f"Rotation matrix: {rotation_90}")
print(f"Point: {point}")
print(f"Rotated 90 deg: {rotated}")

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])
print(f"\nA @ B = {(A @ B)}")
print(f"A.T   = {A.transpose()}")

print()
print("=" * 60)
print("PART 3: NEURAL NETWORK LAYER (matrix @ vector)")
print("=" * 60)

random.seed(42)
weights = Matrix([[random.gauss(0, 0.1) for _ in range(3)] for _ in range(2)])
input_vector = Vector([1.0, 0.5, -0.3])
output = weights @ input_vector
print(f"Input (3D):  {input_vector}")
print(f"Weight matrix shape: {weights.shape}")
print(f"Output (2D): {output}")

print()
print("=" * 60)
print("PART 4: LINEAR INDEPENDENCE")
print("=" * 60)

v1 = Vector([1, 0, 0])
v2 = Vector([0, 1, 0])
v3 = Vector([2, 1, 0])
print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v3 = 2*v1 + v2 = {v3}")
print(f"")
print(f"Independent {{v1, v2}}?     {is_linearly_independent([v1, v2])}")
print(f"Independent {{v1, v2, v3}}? {is_linearly_independent([v1, v2, v3])}")

A_dep = Matrix([[1, 2], [2, 4]])
print(f"\nRank of [[1,2],[2,4]]: {A_dep.rank()} (dependent)")

A_full = Matrix([[1, 2], [3, 4]])
print(f"Rank of [[1,2],[3,4]]: {A_full.rank()} (full rank)")

print()
print("=" * 60)
print("PART 5: PROJECTION")
print("=" * 60)

a_v = Vector([3, 4])
b_v = Vector([1, 0])
proj = project(a_v, b_v)
residual = a_v - proj
print(f"Project {a_v} onto {b_v}")
print(f"  projection: {proj}")
print(f"  residual:   {residual}")
print(f"  residual is perpendicular to b (dot=0): {residual.dot(b_v):.6f}")

print()
print("=" * 60)
print("PART 6: GRAM-SCHMIDT")
print("=" * 60)

v1 = Vector([1, 0, 0])
v2 = Vector([1, 1, 0])
v3 = Vector([1, 1, 1])
print(f"Input vectors: {v1}, {v2}, {v3}")
basis = gram_schmidt([v1, v2, v3])
for i, u in enumerate(basis):
    print(f"  u{i+1} = {u}  |u| = {u.magnitude():.6f}")
print(f"  u1 . u2 = {basis[0].dot(basis[1]):.6f}")
print(f"  u1 . u3 = {basis[0].dot(basis[2]):.6f}")
print(f"  u2 . u3 = {basis[1].dot(basis[2]):.6f}")

print()
print("=" * 60)
print("PART 7: NUMPY VERSION (what you'll actually use)")
print("=" * 60)

import numpy as np

a_np = np.array([1, 2, 3], dtype=float)
b_np = np.array([4, 5, 6], dtype=float)
print(f"a + b       = {a_np + b_np}")
print(f"a . b       = {np.dot(a_np, b_np)}")
print(f"|a|         = {np.linalg.norm(a_np):.4f}")
print(f"cosine      = {np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)):.4f}")

W = np.random.randn(2, 3) * 0.1
x = np.array([1.0, 0.5, -0.3])
print(f"Wx          = {W @ x}")

A_np = np.array([[1, 2], [2, 4]])
print(f"Rank        = {np.linalg.matrix_rank(A_np)}")

Q, R = np.linalg.qr(np.random.randn(3, 3))
print(f"Q orthog?   = {np.allclose(Q @ Q.T, np.eye(3))}")
print(f"R upper tri = {np.allclose(R, np.triu(R))}")

print()
print("=" * 60)
print("PART 8: PYTORCH — TENSORS WITH AUTODIFF")
print("=" * 60)

try:
    import torch
    x_t = torch.randn(3, requires_grad=True)
    y_t = torch.tensor([1.0, 0.0, 0.0])
    similarity = torch.dot(x_t, y_t)
    similarity.backward()
    print(f"x           = {x_t.data}")
    print(f"y           = {y_t.data}")
    print(f"dot product = {similarity.item():.4f}")
    print(f"d(dot)/dx   = {x_t.grad}")
except ImportError:
    print("PyTorch not installed. Skipping.")
