## Lesson 09: Data Management

### What I Learned

The Hugging Face `datasets` library is the standard way to load, cache, convert, and split data for AI work. It uses Apache Arrow under the hood for fast in-memory processing.

Key workflow: load or stream from HF Hub -> cache locally -> convert format (CSV/JSON/Parquet/Arrow) -> split into train/val/test -> pass to training pipeline.

### Key Distinctions

- **Loading vs streaming**: `load_dataset()` downloads the full dataset to cache; `load_dataset(streaming=True)` fetches rows on demand as an `IterableDataset`. Streaming keeps memory constant regardless of dataset size.
- **File formats**: Parquet is the best storage format (columnar, compressed, fast reads). Arrow is best for in-memory (zero-copy). CSV and JSON are for human readability and interchange.
- **Git for large files**: `.gitignore` (simple, re-downloadable data), Git LFS (team model sharing), DVC (reproducible experiments across machines).
- **Splits**: Train (learns), Validation (tune during training), Test (final unbiased evaluation). Always use a fixed seed for reproducibility.

### Dependencies Added

- `datasets>=3.0` -- load/stream/cache/split datasets from Hugging Face Hub
- `huggingface-hub>=0.26` -- download individual model files and snapshots

### Data Pipeline Tools

- `datasets.load_dataset()` -- load or stream datasets
- `Dataset.to_csv/to_json/to_parquet()` -- format conversion
- `Dataset.train_test_split(seed=N)` -- reproducible splits with seeding
- `hf_hub_download()` -- download individual model files
- `hf_hub_snapshot()` -- download full model repos
- Cache is at `~/.cache/huggingface/{datasets,hub}/`

### Common Traps

1. Forgetting to set a seed on splits -> irreproducible results
2. Streaming mode disables `.len()` and random access (no index)
3. Parquet/Arrow require `pyarrow` (comes with `datasets`)
4. Model weights and large datasets should never go into git
