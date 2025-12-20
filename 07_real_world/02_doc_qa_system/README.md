# Example 02: Document Q&A System

A RAG-based system for answering questions about PDF documents.

## Features

- PDF document ingestion
- Vector search with LanceDB
- Context-aware answers
- Source citations

## Architecture

```
PDF → Text Extraction → Embeddings → Vector DB
User Query → Vector Search → Context → LLM → Answer
```

## Key Concepts

- **Knowledge**: PDFKnowledgeBase for document ingestion
- **Vector DB**: LanceDB for semantic search
- **RAG**: Retrieval-Augmented Generation

## Run the Example

```bash
# With a sample PDF
python main.py --pdf sample.pdf "What is the main topic?"

# Interactive mode
python main.py --pdf sample.pdf
```

## Customization Ideas

1. Support multiple document formats
2. Add document summarization
3. Implement multi-document Q&A
4. Add conversation memory
