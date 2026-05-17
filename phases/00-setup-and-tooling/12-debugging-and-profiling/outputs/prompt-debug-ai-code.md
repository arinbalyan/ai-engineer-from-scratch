# AI Debugging Prompt Template

Use this prompt when an AI agent needs to debug AI/ML code.
Copy the relevant section(s) depending on the symptom.

---

## Symptom: NaN Loss or Exploding Gradients

```
The training loss goes to NaN. I need help debugging.

What I know:
- Framework: PyTorch
- Loss function: <cross_entropy / MSE / custom>
- Optimizer: <Adam / SGD> with lr=<value>
- Model type: <CNN / Transformer / MLP>
- When it happens: <immediately / after N steps / only on certain batches>

Please:
1. Suggest the most likely causes given the pattern above
2. Show me code to add conditional breakpoint at NaN step and check gradients per parameter
3. Recommend specific fixes (clip gradient norm, reduce LR, fix numerical stability in loss)
```

---

## Symptom: Training Slow / GPU Underutilized

```
My training loop is slow and GPU utilization is low (< 50%). Help me profile it.

Please:
1. Show me how to time data loading vs forward vs backward separately
2. Tell me what DataLoader settings to check (num_workers, prefetch_factor, pin_memory)
3. Suggest how to run cProfile or line_profiler on the training loop
4. Show GPU memory usage commands
```

---

## Symptom: Suspiciously High Accuracy

```
My model got <XX>% accuracy which seems too good to be true.

Please help me check for:
1. Data leakage: train/test overlap by ID column and by feature column
2. Temporal leakage: future data leaking into training samples
3. Target leakage: feature columns that correlate perfectly with labels
4. Show me a validation strategy that doesn't leak information
```

---

## Symptom: Shape Errors / Dimension Mismatch

```
I'm getting a shape mismatch error in my PyTorch model.

Error: <paste traceback here>

Please:
1. Trace the expected shape at each layer
2. Show me how to add forward hooks to print every shape transformation
3. Identify where the mismatch occurs
```

---

## General Debugging Workflow

```
Help me debug an AI training issue. I'll describe what I see, and you guide me step
by step through the three-level debugging hierarchy (Python -> Tensors -> Training).

Level 1 (Python): Check for actual errors, add logging with timestamps
Level 2 (Tensors): Check shapes, dtypes, devices, NaN/Inf values
Level 3 (Training): Check loss curves, gradient norms, weight distributions

Start at Level 1 and only escalate if needed.
```
