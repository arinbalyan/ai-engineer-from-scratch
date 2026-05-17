"""Vectors, Matrices & Operations — Julia version.

Covers: element-wise vs matrix multiply, transpose, determinant,
inverse, broadcasting, and a dense neural network layer.

Run: julia --project=languages/julia phases/01-math-foundations/02-vectors-matrices-operations/code/vectors_matrices_operations.jl
"""

using LinearAlgebra
using Random

println("=" ^ 60)
println("PART 1: ELEMENT-WISE vs MATRIX MULTIPLY")
println("=" ^ 60)

A = [1 2; 3 4]
B = [5 6; 7 8]
println("A = $A")
println("\nB = $B")
println("\nA + B = $(A + B)")
println("\nA .* B (element-wise) = $(A .* B)")
println("\nA * B (matrix multiply) = $(A * B)")

println()
println("=" ^ 60)
println("PART 2: TRANSPOSE, DETERMINANT, INVERSE")
println("=" ^ 60)

println("A' (transpose) = $(A')")
println("\ndet(A) = $(det(A))")
A_inv = inv(A)
println("\ninv(A) = $A_inv")
println("\nA * inv(A) = $(round.(A * A_inv, digits=10))")
println("I = $(I(2))")

println()
println("=" ^ 60)
println("PART 3: DENSE NEURAL NETWORK LAYER")
println("=" ^ 60)

Random.seed!(42)
inputs = [0.5, 0.8, 0.2]
weights = rand(2, 3) .* 2 .- 1
bias = [0.1, 0.1]

pre_activation = weights * inputs + bias
output = max.(0, pre_activation)

println("Input dim:  $(length(inputs))")
println("Weight shape: $(size(weights))")
println("Bias dim:   $(length(bias))")
println("Output dim: $(length(output))")
println("\nPre-activation: $pre_activation")
println("After ReLU:     $output")

println()
println("=" ^ 60)
println("PART 4: BROADCASTING")
println("=" ^ 60)

M = [1 2 3; 4 5 6]
b_row = [10 20 30]
println("Matrix: $(size(M))")
println("Bias row: $(size(b_row))")
println("Result: $(M .+ b_row)")

println()
println("=" ^ 60)
println("JULIA ADVANTAGES")
println("=" ^ 60)
println("  - Vectors/matrices are native (no custom classes)")
println("  - .* for element-wise, * for matrix multiply")
println("  - Built-in: det, inv, I, transpose")
println("  - Broadcasting with dot syntax: .+, .*, max.")
println("  - Same LinearAlgebra that powers Flux.jl")
