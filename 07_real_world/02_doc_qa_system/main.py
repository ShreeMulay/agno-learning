#!/usr/bin/env python3
"""Example 02: Document Q&A System - RAG with PDF documents.

A system for answering questions about uploaded documents.

Run with:
    python main.py --pdf path/to/document.pdf "What is the main topic?"
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


def create_doc_qa_agent(model, pdf_path: str = None):
    """Create a document Q&A agent with optional PDF knowledge."""
    
    # Set up vector database
    vector_db = LanceDb(
        uri="tmp/lancedb",
        table_name="documents",
    )
    
    knowledge = None
    if pdf_path and Path(pdf_path).exists():
        knowledge = Knowledge(
            name="document_qa",
            vector_db=vector_db,
        )
        knowledge.add_content(path=pdf_path)
    
    agent = Agent(
        name="DocQA",
        model=model,
        knowledge=knowledge,
        instructions=[
            "You answer questions based on the provided documents.",
            "Always cite the specific section or page when possible.",
            "If the answer is not in the documents, say so clearly.",
            "Provide relevant quotes when helpful.",
        ],
        search_knowledge=True,
        markdown=True,
    )
    
    return agent, knowledge






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
    if args.pdf:
        print(f"  Document: {args.pdf}")
        if not Path(args.pdf).exists():
            print(f"  ERROR: File not found: {args.pdf}")
            print("\n  Create a sample PDF or provide an existing one.")
            return
    else:
        print("  No document provided - running in demo mode")
        print("  Use --pdf <path> to load a document")
    
    agent, knowledge = create_doc_qa_agent(model, args.pdf)
    
    # Knowledge is already loaded when add_content is called
    if knowledge:
        print_section("Loading Document")
        print("  Document indexed successfully")
    
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
