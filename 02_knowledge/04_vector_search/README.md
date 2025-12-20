# Lesson 04: Vector Search Deep Dive

Understand how vector search powers RAG and learn to optimize it.

## Concepts Covered

- **Embeddings**: Converting text to vectors
- **Similarity search**: Finding related content
- **LanceDB**: Local vector database
- **Search parameters**: Tuning retrieval quality

## How Vector Search Works

1. **Embedding**: Text → 1536-dimensional vector
2. **Storage**: Vectors stored with metadata
3. **Query**: Question → vector → nearest neighbors
4. **Retrieval**: Top-k most similar chunks returned

```
Query: "How do I create an agent?"
  ↓
Embed query → [0.1, -0.3, 0.8, ...]
  ↓
Find nearest vectors in database
  ↓
Return top 5 matching chunks
  ↓
LLM generates answer using context
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `num_documents` | Documents to retrieve | 5 |
| `chunk_size` | Characters per chunk | ~500 |
| `chunk_overlap` | Overlap between chunks | ~50 |

## LanceDB Features

- **Local-first**: No server needed
- **Fast**: Built on Arrow/Lance format
- **Simple**: Just a directory on disk
- **Scalable**: Handles millions of vectors

## Run the Example

```bash
# Explore vector search
python main.py

# Adjust retrieval count
python main.py --num-docs 10

# See similarity scores
python main.py --show-scores

# Compare different queries
python main.py --query "agent creation" --compare "tool usage"
```

## Exercises

1. Index a large document and vary `num_documents`
2. Compare exact vs. approximate search
3. Experiment with different embedding models

## Module Complete!

Congratulations! You've completed Module 2: Knowledge.

**Next Module**: [03_memory](../../03_memory/) - Build agents that remember.
