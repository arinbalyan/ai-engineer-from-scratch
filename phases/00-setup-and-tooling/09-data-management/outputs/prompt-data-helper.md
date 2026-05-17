## Prompt: Dataset Finder and Loader

Use this prompt when an AI assistant needs to help you find, load, or manage datasets for an AI/ML project.

```
I need to find and load a dataset for my AI project. Help me identify the 
right dataset and load it properly.

Context about my task:
- [Describe what you are building: e.g., text classification, image generation, 
  question answering, etc.]
- [Domain: e.g., medical, finance, general]
- [Size constraints: e.g., must fit in 4GB VRAM, need streaming for large data]
- [Format needed: e.g., text pairs, image-label, question-answer]

Please:

1. **Find the dataset** -- Search the Hugging Face Hub for datasets matching 
   my task. Recommend 2-3 options with tradeoffs (size, quality, license).

2. **Provide a loader snippet** -- Give me the exact code to load it using 
   the Hugging Face `datasets` library. Include streaming=True if the dataset 
   is large.

3. **Format conversion** -- If I need to convert formats, provide the 
   conversion code. Parquet is preferred for storage.

4. **Split strategy** -- Show me how to create train/val/test splits with 
   a fixed seed for reproducibility.

5. **Cache info** -- Tell me where the dataset will be cached and how to 
   clear or inspect the cache if needed.

6. **Avoid these traps** -- Warn me about dataset-specific issues:
   - Is the license compatible with my use case?
   - Does it need preprocessing (tokenization, normalization)?
   - Is there label imbalance?
   - Can it fit in memory or should I stream it?

Use the `datasets` library with these conventions:
- `load_dataset("name", split="train")` for direct loading
- `load_dataset("name", split="train", streaming=True)` for large datasets
- `dataset.train_test_split(test_size=0.2, seed=42)` for reproducible splits
