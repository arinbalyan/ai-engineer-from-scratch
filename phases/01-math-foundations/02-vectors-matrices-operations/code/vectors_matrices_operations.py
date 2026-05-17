"""Vectors, Matrices & Operations — from scratch to NumPy.

Covers: element-wise vs matrix multiply, transpose, determinant,
inverse, broadcasting, and a dense neural network layer.
"""

import random
import math


class Vector:
    def __init__(self, data):
        self.data = list(data)
        self.size = len(self.data)

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __sub__(self, other):
        return Vector([a - b for a, b in zip(self.data, other.data)])

    def __mul__(self, scalar):
        return Vector([x * scalar for x in self.data])

    def dot(self, other):
        return sum(a * b for a, b in zip(self.data, other.data))

    def magnitude(self):
        return math.sqrt(sum(x ** 2 for x in self.data))

    def __repr__(self):
        return f"Vector({self.data})"


class Matrix:
    def __init__(self, data):
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.shape = (self.rows, self.cols)

    def __add__(self, other):
        return Matrix([
            [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def __sub__(self, other):
        return Matrix([
            [self.data[i][j] - other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def scalar_multiply(self, scalar):
        return Matrix([
            [self.data[i][j] * scalar for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def element_wise_multiply(self, other):
        return Matrix([
            [self.data[i][j] * other.data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ])

    def matmul(self, other):
        return Matrix([
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                for j in range(other.cols)
            ]
            for i in range(self.rows)
        ])

    def transpose(self):
        return Matrix([
            [self.data[j][i] for j in range(self.rows)]
            for i in range(self.cols)
        ])

    def determinant(self):
        if self.shape == (1, 1):
            return self.data[0][0]
        if self.shape == (2, 2):
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        det = 0
        for j in range(self.cols):
            minor = Matrix([
                [self.data[i][k] for k in range(self.cols) if k != j]
                for i in range(1, self.rows)
            ])
            det += ((-1) ** j) * self.data[0][j] * minor.determinant()
        return det

    def inverse_2x2(self):
        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular, no inverse exists")
        return Matrix([
            [self.data[1][1] / det, -self.data[0][1] / det],
            [-self.data[1][0] / det, self.data[0][0] / det]
        ])

    @staticmethod
    def identity(n):
        return Matrix([
            [1 if i == j else 0 for j in range(n)]
            for i in range(n)
        ])

    def __repr__(self):
        rows = "\n  ".join(str(row) for row in self.data)
        return f"Matrix({self.shape}):\n  {rows}"


def relu_matrix(m):
    return Matrix([[max(0, val) for val in row] for row in m.data])


print("=" * 60)
print("PART 1: ELEMENT-WISE vs MATRIX MULTIPLY")
print("=" * 60)

A = Matrix([[1, 2], [3, 4]])
B = Matrix([[5, 6], [7, 8]])
print(f"A = {A}")
print(f"B = {B}")
print(f"\nA + B =\n{A + B}")
print(f"\nA * B (element-wise) =\n{A.element_wise_multiply(B)}")
print(f"\nA @ B (matrix multiply) =\n{A.matmul(B)}")

print()
print("=" * 60)
print("PART 2: TRANSPOSE, DETERMINANT, INVERSE")
print("=" * 60)

print(f"A^T =\n{A.transpose()}")
print(f"\ndet(A) = {A.determinant()}")

A_inv = A.inverse_2x2()
print(f"\nA^-1 =\n{A_inv}")
print(f"\nA @ A^-1 =\n{A.matmul(A_inv)}")
print(f"(should be identity)\n{Matrix.identity(2)}")

print()
print("=" * 60)
print("PART 3: DENSE NEURAL NETWORK LAYER")
print("=" * 60)

random.seed(42)
inputs = Matrix([[0.5], [0.8], [0.2]])
weights_data = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(2)]
weights = Matrix(weights_data)
bias = Matrix([[0.1], [0.1]])

pre_activation = weights.matmul(inputs) + bias
output = relu_matrix(pre_activation)

print(f"Input shape:  {inputs.shape}")
print(f"Weight shape: {weights.shape}")
print(f"Bias shape:   {bias.shape}")
print(f"Output shape: {output.shape}")
print(f"\nPre-activation:\n{pre_activation}")
print(f"\nAfter ReLU:\n{output}")

print()
print("=" * 60)
print("PART 4: NUMPY EQUIVALENTS")
print("=" * 60)

import numpy as np

A_np = np.array([[1, 2], [3, 4]])
B_np = np.array([[5, 6], [7, 8]])
print(f"A + B =\n{A_np + B_np}")
print(f"\nA * B (element-wise) =\n{A_np * B_np}")
print(f"\nA @ B (matrix multiply) =\n{A_np @ B_np}")
print(f"\nA^T =\n{A_np.T}")
print(f"\ndet(A) = {np.linalg.det(A_np)}")
print(f"\nA^-1 =\n{np.linalg.inv(A_np)}")
print(f"\nI =\n{np.eye(2)}")

inputs_np = np.random.randn(3, 1)
weights_np = np.random.randn(2, 3)
bias_np = np.array([[0.1], [0.1]])
output_np = np.maximum(0, weights_np @ inputs_np + bias_np)
print(f"\nNeural network layer: {weights_np.shape} @ {inputs_np.shape} = {output_np.shape}")

print()
print("=" * 60)
print("PART 5: BROADCASTING")
print("=" * 60)

matrix_np = np.array([[1, 2, 3], [4, 5, 6]])
bias_np = np.array([10, 20, 30])
print(f"Matrix: {matrix_np.shape}")
print(f"Bias:   {bias_np.shape}")
print(f"Result:\n{matrix_np + bias_np}")
