# Quick Verification Command

Run this after cloning or after any environment change to confirm all four languages work:

```bash
echo "=== Python ===" && uv run python languages/python/hello.py && \
echo "=== Node.js ===" && node languages/node/hello.mjs && \
echo "=== Rust ===" && cd languages/rust && cargo run && \
echo "=== Julia ===" && cd ../julia && julia --project=. -e 'println("Julia ready")'
```

Expected output:
```
=== Python ===
Python ready — AI Engineering from Scratch
=== Node.js ===
Node.js ready — AI Engineering from Scratch
=== Rust ===
   Compiling ai-engineering ...
    Finished `dev` profile ...
     Running `target/debug/ai-engineering`
Rust ready — AI Engineering from Scratch
=== Julia ===
Julia ready — AI Engineering from Scratch
```

If any step fails, the chain stops there. Fix that language's setup before moving on.
