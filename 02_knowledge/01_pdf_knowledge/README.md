# Lesson 01: PDF Knowledge

Load PDF documents into your agent's knowledge base for RAG (Retrieval-Augmented Generation).

## Concepts Covered

- **PDFKnowledge**: Load and process PDF files
- **Vector database**: Store embeddings for semantic search
- **search_knowledge**: Enable automatic knowledge retrieval
- **Chunking**: How documents are split for embedding

## How It Works

```python
from agno.agent import Agent
from agno.knowledge.pdf import PDFKnowledge
from agno.vectordb.lancedb import LanceDb

# Create knowledge base from PDFs
knowledge = PDFKnowledge(
    path="./documents",  # Directory or single file
    vector_db=LanceDb(
        table_name="pdf_docs",
        uri="./lancedb",
    ),
)

# Load documents into vector DB (one time)
knowledge.load()

# Create agent with knowledge
agent = Agent(
    model=model,
    knowledge=knowledge,
    search_knowledge=True,  # Enable automatic RAG
)
```

## RAG Flow

1. **Indexing** (one time):
   - PDF text is extracted
   - Text is split into chunks
   - Chunks are embedded into vectors
   - Vectors stored in database

2. **Querying** (every query):
   - User question is embedded
   - Similar chunks are found
   - Retrieved context is added to prompt
   - LLM generates answer using context

## Run the Example

```bash
# Create a sample PDF first, then:
python main.py

# With a specific PDF file
python main.py --pdf ./my_document.pdf

# Ask questions about the document
python main.py --query "What is the main topic of this document?"
```

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `path` | Path to PDF file or directory |
| `vector_db` | Vector database instance |
| `num_documents` | Max documents to retrieve (default: 5) |
| `chunk_size` | Characters per chunk (default: varies) |

## Exercises

1. Load a multi-page PDF and ask questions
2. Compare answers with and without RAG
3. Adjust `num_documents` to see how it affects answers

## Next Lesson

[02_url_knowledge](../02_url_knowledge/) - Load content from websites.
