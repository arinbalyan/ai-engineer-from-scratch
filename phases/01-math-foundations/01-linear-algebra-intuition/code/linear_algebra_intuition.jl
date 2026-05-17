"""Linear Algebra Intuition — Julia version.

Teaches: vectors as points, dot product as similarity, matrices as
transformations, linear independence, rank, projection, Gram-Schmidt.

Run: julia --project=languages/julia phases/01-math-foundations/01-linear-algebra-intuition/code/linear_algebra_intuition.jl
"""

using LinearAlgebra
using Random

# ============================================================
# 1. VECTORS
# ============================================================

a = [1.0, 2.0, 3.0]
b = [4.0, 5.0, 6.0]

println("=" ^ 60)
println("PART 1: VECTOR OPERATIONS")
println("=" ^ 60)
println("a = $a")
println("b = $b")
println("a + b  = $(a + b)")
println("a - b  = $(a - b)")
println("a . b  = $(a ⋅ b)")
println("|a|    = $(round(norm(a), digits=4))")
println("cosine = $(round((a ⋅ b) / (norm(a) * norm(b)), digits=4))")

function angle_between(v, w)
    cs = (v ⋅ w) / (norm(v) * norm(w))
    cs = max(-1.0, min(1.0, cs))
    return rad2deg(acos(cs))
end
println("angle  = $(round(angle_between(a, b), digits=2)) degrees")

# ============================================================
# 2. MATRIX OPERATIONS
# ============================================================

println()
println("=" ^ 60)
println("PART 2: MATRIX OPERATIONS")
println("=" ^ 60)

rotation_90 = [0 -1; 1 0]
point = [3.0, 1.0]
rotated = rotation_90 * point
println("Rotation matrix: $rotation_90")
println("Point: $point")
println("Rotated 90 deg: $rotated")

A = [1 2; 3 4]
B = [5 6; 7 8]
println("\nA * B = $(A * B)")
println("A'    = $(A')")

# ============================================================
# 3. NEURAL NETWORK LAYER
# ============================================================

println()
println("=" ^ 60)
println("PART 3: NEURAL NETWORK LAYER")
println("=" ^ 60)

Random.seed!(42)
W = randn(2, 3) * 0.1
x = [1.0, 0.5, -0.3]
output = W * x
println("Input (3D):  $x")
println("Weight matrix shape: $(size(W))")
println("Output (2D): $output")

# ============================================================
# 4. LINEAR INDEPENDENCE
# ============================================================

println()
println("=" ^ 60)
println("PART 4: LINEAR INDEPENDENCE")
println("=" ^ 60)

v1 = [1, 0, 0]
v2 = [0, 1, 0]
v3 = [2, 1, 0]
println("v1 = $v1")
println("v2 = $v2")
println("v3 = 2*v1 + v2 = $v3")

M_dep = [1 2; 2 4]
M_full = [1 2; 3 4]
println("\nRank of [1 2; 2 4]: $(rank(M_dep)) (dependent)")
println("Rank of [1 2; 3 4]: $(rank(M_full)) (full rank)")

function is_independent(vectors)
    mat = reduce(hcat, vectors)'
    return rank(mat) == length(vectors)
end
println("\nIndependent {v1, v2}?     $(is_independent([v1, v2]))")
println("Independent {v1, v2, v3}? $(is_independent([v1, v2, v3]))")

# ============================================================
# 5. PROJECTION
# ============================================================

println()
println("=" ^ 60)
println("PART 5: PROJECTION")
println("=" ^ 60)

a_v = [3.0, 4.0]
b_v = [1.0, 0.0]
proj = (a_v ⋅ b_v) / (b_v ⋅ b_v) * b_v
residual = a_v - proj
println("Project $a_v onto $b_v")
println("  projection: $proj")
println("  residual:   $residual")
println("  residual ⋅ b = $(round(residual ⋅ b_v, digits=6))")

# ============================================================
# 6. GRAM-SCHMIDT
# ============================================================

println()
println("=" ^ 60)
println("PART 6: GRAM-SCHMIDT")
println("=" ^ 60)

function gram_schmidt(vectors)
    orthonormal = Vector{Float64}[]
    for v in vectors
        w = copy(v)
        for u in orthonormal
            proj = (w ⋅ u) / (u ⋅ u) * u
            w = w - proj
        end
        if norm(w) < 1e-10
            continue
        end
        push!(orthonormal, w / norm(w))
    end
    return orthonormal
end

v1 = [1.0, 0.0, 0.0]
v2 = [1.0, 1.0, 0.0]
v3 = [1.0, 1.0, 1.0]
println("Input vectors: $v1, $v2, $v3")
basis = gram_schmidt([v1, v2, v3])
for (i, u) in enumerate(basis)
    println("  u$i = $(round.(u, digits=6))  |u| = $(round(norm(u), digits=6))")
end
println("  u1 ⋅ u2 = $(round(basis[1] ⋅ basis[2], digits=6))")
println("  u1 ⋅ u3 = $(round(basis[1] ⋅ basis[3], digits=6))")
println("  u2 ⋅ u3 = $(round(basis[2] ⋅ basis[3], digits=6))")

# ============================================================
# 7. QR DECOMPOSITION (built-in)
# ============================================================

println()
println("=" ^ 60)
println("PART 7: QR DECOMPOSITION (built-in)")
println("=" ^ 60)

M3 = randn(3, 3)
F = qr(M3)
Q = Matrix(F.Q)
R = F.R
println("Q is orthogonal: $(isapprox(Q * Q', I, atol=1e-10))")
println("R is upper tri:  $(istriu(R))")
