#!/usr/bin/env python3
"""Example 02: Document Q&A System - RAG with PDF documents.

A system for answering questions about uploaded documents.

Run with:
    python main.py                           # Demo mode with sample content
    python main.py --pdf path/to/doc.pdf     # Interactive with your PDF
    python main.py --pdf doc.pdf "Question?" # Single question mode
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# Sample document content for demo mode
SAMPLE_DOCUMENT = """
# Agno Framework Overview

## What is Agno?

Agno is a lightweight, high-performance framework for building AI agents. It was
formerly known as phiData and was renamed to Agno in version 2.0.

## Key Features

1. **Multi-Provider Support**: Works with OpenAI, Anthropic, Google, and 100+ other
   model providers through a unified interface.

2. **Tool Integration**: Agents can use tools to interact with external systems,
   APIs, databases, and more.

3. **Knowledge Bases**: Built-in support for RAG (Retrieval Augmented Generation)
   with vector databases like LanceDB, Pinecone, and Qdrant.

4. **Teams**: Coordinate multiple agents to work together on complex tasks using
   different modes: coordinate, route, and collaborate.

5. **Memory**: Session state, user memories, and agentic memory for persistent
   context across conversations.

## Performance

Agno is designed for speed:
- Agent instantiation: ~3μs (microseconds)
- Memory efficient: ~6KB per agent
- No heavy dependencies

## Getting Started

Install Agno with pip:
```
pip install agno
```

Create your first agent:
```python
from agno.agent import Agent

agent = Agent(model="openai:gpt-4o")
agent.print_response("Hello!")
```

## Best Practices

1. Use structured outputs with `output_schema` for reliable parsing
2. Add `session_id` when using session state across multiple calls
3. Use SqliteDb for persistence when state needs to survive restarts
4. Test with multiple providers to ensure compatibility
"""


def create_doc_qa_agent(model, pdf_path: str = None, use_demo_content: bool = False):
    """Create a document Q&A agent with optional PDF knowledge."""
    
    # Set up vector database
    project_root = Path(__file__).parent.parent.parent
    vector_db = LanceDb(
        uri=str(project_root / "tmp" / "lancedb"),
        table_name="doc_qa",
    )
    
    knowledge = None
    
    # Load PDF if provided
    if pdf_path and Path(pdf_path).exists():
        knowledge = Knowledge(
            name="document_qa",
            vector_db=vector_db,
        )
        knowledge.add_content(path=pdf_path)
    
    # Load demo content if no PDF
    elif use_demo_content:
        knowledge = Knowledge(
            name="document_qa",
            vector_db=vector_db,
        )
        # Add sample content as text
        knowledge.add_content(text_content=SAMPLE_DOCUMENT)
    
    agent = Agent(
        name="DocQA",
        model=model,
        knowledge=knowledge,
        instructions=[
            "You answer questions based on the provided documents.",
            "Always cite the specific section when possible.",
            "If the answer is not in the documents, say so clearly.",
            "Provide relevant quotes when helpful.",
        ],
        search_knowledge=True,
        markdown=True,
    )
    
    return agent, knowledge






def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    agent, _ = create_doc_qa_agent(model, use_demo_content=True)
    return agent


def main():
    parser = argparse.ArgumentParser(description="Document Q&A System")
    add_model_args(parser)
    parser.add_argument(
        "--pdf", type=str, default=None,
        help="Path to PDF document"
    )
    parser.add_argument(
        "query", type=str, nargs="?", default=None,
        help="Question to ask"
    )
    args = parser.parse_args()

    print_header("Document Q&A System")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    
    print_section("Setup")
    use_demo = False
    if args.pdf:
        print(f"  Document: {args.pdf}")
        if not Path(args.pdf).exists():
            print(f"  ERROR: File not found: {args.pdf}")
            print("\n  Create a sample PDF or provide an existing one.")
            return
    else:
        print("  No document provided - running in demo mode")
        print("  Loading sample Agno documentation...")
        print("  (Use --pdf <path> to load your own document)")
        use_demo = True
    
    agent, knowledge = create_doc_qa_agent(model, args.pdf, use_demo_content=use_demo)
    
    # Knowledge is already loaded when add_content is called
    if knowledge:
        print_section("Document Indexed")
        print("  Ready to answer questions!")
    
    # Single query or interactive mode
    if args.query:
        print_section("Question")
        print(f"  {args.query}")
        print()
        
        print_section("Answer")
        response = agent.run(args.query)
        print(response.content)
    else:
        # Interactive mode
        print_section("Interactive Mode")
        print("  Type your questions. Enter 'quit' to exit.\n")
        
        while True:
            try:
                query = input("Q: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            
            if not query:
                continue
            if query.lower() == 'quit':
                break
            
            response = agent.run(query)
            print(f"\nA: {response.content}\n")


if __name__ == "__main__":
    main()
