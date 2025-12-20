#!/usr/bin/env python3
"""
Lesson 01: PDF Knowledge

Concepts covered:
- Loading PDFs into a knowledge base
- Using LanceDB for vector storage
- Enabling search_knowledge for RAG
- Querying documents with natural language

Run: python main.py
     python main.py --pdf ./document.pdf
     python main.py --query "What is this about?"
"""

import argparse
import sys
import tempfile
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_sample_pdf(output_path: Path) -> None:
    """
    Create a simple sample PDF for demonstration.
    
    Note: This creates a text file that simulates PDF content.
    For real PDFs, use actual PDF files.
    """
    # Create a simple text file (PDFKnowledge can handle various formats)
    content = """
    AGNO FRAMEWORK OVERVIEW
    =======================
    
    Introduction
    ------------
    Agno is a high-performance Python framework for building AI agents.
    It was formerly known as phiData and was rebranded in January 2025.
    
    Key Features
    ------------
    1. Blazing Fast: Agents instantiate in ~3 microseconds
    2. Low Memory: ~6.6KB per agent
    3. Privacy First: Runs entirely in your cloud
    4. 100+ Tools: Pre-built integrations
    5. Multi-Model: Supports OpenAI, Anthropic, Google, and more
    
    Core Concepts
    -------------
    Agents: AI programs where an LLM controls execution flow
    Tools: Functions that agents can call
    Knowledge: Domain-specific information via RAG
    Memory: Persistent user preferences
    Teams: Multi-agent collaboration
    Workflows: Orchestrated pipelines
    
    Getting Started
    ---------------
    Install agno: pip install agno
    Create an agent: Agent(model=model, instructions="...")
    Run it: agent.print_response("Hello!")
    
    For more information, visit docs.agno.com
    """
    
    output_path.write_text(content)
    print(f"Created sample document: {output_path}")



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    
    project_root = Path(__file__).parent.parent.parent
    lancedb_path = project_root / ".lancedb"
    
    knowledge = Knowledge(
        name="pdf_knowledge",
        vector_db=LanceDb(
            table_name="pdf_knowledge",
            uri=str(lancedb_path),
        ),
    )
    return create_rag_agent(model, knowledge)


def create_rag_agent(model, knowledge):
    """Create a RAG agent with the given knowledge base."""
    return Agent(
        model=model,
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "You are a helpful assistant with access to document knowledge.",
            "Use the knowledge base to answer questions accurately.",
            "If the answer isn't in the documents, say so.",
            "Cite relevant sections when possible.",
        ],
        markdown=True,
    )


def main():
    """Demonstrate PDF knowledge base."""
    parser = argparse.ArgumentParser(
        description="PDF Knowledge demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--pdf",
        type=str,
        help="Path to PDF file (uses sample if not provided)",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What are the key features of Agno?",
        help="Question to ask about the document",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild the knowledge base",
    )
    args = parser.parse_args()

    print_header("Lesson 01: PDF Knowledge")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Provider: {args.provider}")
    print(f"Model: {args.model or 'default'}")

    # Set up paths
    project_root = Path(__file__).parent.parent.parent
    lancedb_path = project_root / ".lancedb"
    
    # Handle PDF path
    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"Error: PDF not found: {pdf_path}")
            sys.exit(1)
    else:
        # Create sample document
        sample_dir = project_root / "sample_data"
        sample_dir.mkdir(exist_ok=True)
        pdf_path = sample_dir / "sample_agno_overview.txt"
        
        if not pdf_path.exists() or args.rebuild:
            print_section("Creating Sample Document")
            create_sample_pdf(pdf_path)

    print_section("Building Knowledge Base")
    print(f"Document: {pdf_path}")
    print(f"Vector DB: {lancedb_path}")
    
    # Create knowledge base using the new Knowledge API
    try:
        knowledge = Knowledge(
            name="pdf_knowledge",
            vector_db=LanceDb(
                table_name="pdf_knowledge",
                uri=str(lancedb_path),
            ),
        )
        
        # Load documents (index them) - must use path= keyword argument
        print("Indexing document...")
        knowledge.add_content(path=str(pdf_path))
        print("Knowledge base ready!")
        
    except Exception as e:
        print(f"Error building knowledge base: {e}")
        print("\nTip: Make sure you have the required dependencies:")
        print("  pip install pypdf lancedb")
        sys.exit(1)

    print_section("Creating RAG Agent")
    
    agent = create_rag_agent(model, knowledge)

    print_section("Query")
    print(f"Question: {args.query}\n")
    
    print("Answer:")
    print("-" * 60)
    agent.print_response(args.query)
    print("-" * 60)

    # Try a few more example questions
    print_section("Try More Questions")
    example_questions = [
        "What is Agno?",
        "How do I install Agno?",
        "What are the core concepts?",
    ]
    
    for q in example_questions:
        print(f"  - {q}")
    
    print("\nRun again with: python main.py --query \"Your question here\"")


if __name__ == "__main__":
    main()
