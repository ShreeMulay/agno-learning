#!/usr/bin/env python3
"""
Lesson 02: URL Knowledge

Concepts covered:
- Loading web content into knowledge base
- URLKnowledge for web scraping
- Indexing multiple URLs
- Building agents with web-sourced knowledge

Run: python main.py
     python main.py --urls "https://example.com/page1"
     python main.py --query "What is Agno?"
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# Default URLs to index (Agno documentation)
DEFAULT_URLS = [
    "https://docs.agno.com/introduction",
]



def create_url_agent(model, knowledge):
    """Create a RAG agent with URL knowledge."""
    return Agent(
        model=model,
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "You are a helpful assistant with access to web content.",
            "Use the knowledge base to answer questions accurately.",
            "Cite the source URL when providing information.",
            "If information isn't available, say so.",
        ],
        markdown=True,
    )


def main():
    """Demonstrate URL knowledge base."""
    parser = argparse.ArgumentParser(
        description="URL Knowledge demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--urls",
        nargs="+",
        default=DEFAULT_URLS,
        help="URLs to index (space-separated)",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What is Agno and what are its key features?",
        help="Question to ask about the web content",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild the knowledge base",
    )
    args = parser.parse_args()

    print_header("Lesson 02: URL Knowledge")

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

    print_section("URLs to Index")
    for url in args.urls:
        print(f"  - {url}")

    print_section("Building Knowledge Base")
    print(f"Vector DB: {lancedb_path}")
    
    try:
        # Create knowledge base with URL content
        print("  [1/4] Initializing vector database...")
        knowledge = Knowledge(
            name="url_knowledge",
            vector_db=LanceDb(
                table_name="url_knowledge",
                uri=str(lancedb_path),
            ),
        )
        print("  [1/4] Vector database ready ✓")
        
        # Load and index content from URLs
        print(f"\n  [2/4] Fetching {len(args.urls)} URL(s)...")
        for i, url in enumerate(args.urls, 1):
            print(f"        [{i}/{len(args.urls)}] Fetching: {url}")
        
        print("\n  [3/4] Chunking and embedding content...")
        print("        (This may take 10-60 seconds depending on content size)")
        
        import time
        start_time = time.time()
        
        for i, url in enumerate(args.urls, 1):
            url_start = time.time()
            print(f"        [{i}/{len(args.urls)}] Processing: {url}...", end=" ", flush=True)
            knowledge.add_content(url=url)
            elapsed = time.time() - url_start
            print(f"done ({elapsed:.1f}s)")
        
        total_time = time.time() - start_time
        print(f"\n  [4/4] Knowledge base ready ✓ (total: {total_time:.1f}s)")
        
    except Exception as e:
        print(f"\n  ✗ Error building knowledge base: {e}")
        print("\nTip: Make sure you have the required dependencies:")
        print("  pip install beautifulsoup4 lxml httpx lancedb")
        print("\nAlso ensure the URLs are accessible.")
        sys.exit(1)

    print_section("Creating RAG Agent")
    
    agent = create_url_agent(model, knowledge)

    print_section("Query")
    print(f"Question: {args.query}\n")
    
    print("Answer:")
    print("-" * 60)
    agent.print_response(args.query)
    print("-" * 60)

    print_section("Key Points")
    print("""
    URL Knowledge enables:
    
    1. Live Web Content
       - Scrape any accessible URL
       - Extract text from HTML
       - Handle JavaScript-rendered pages (with additional setup)
    
    2. Multiple Sources
       - Index many URLs at once
       - Build comprehensive knowledge bases
       - Aggregate information from various sites
    
    3. RAG Pattern
       - Semantic search finds relevant content
       - LLM generates answers with context
       - Cites sources for verification
    
    Use Cases:
       - Documentation assistants
       - News aggregators
       - Company knowledge bases
       - Research tools
    """)


if __name__ == "__main__":
    main()
