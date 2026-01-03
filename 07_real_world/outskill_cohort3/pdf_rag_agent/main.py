#!/usr/bin/env python3
"""Example: PDF RAG Agent
Category: outskill_cohort3/rag

RAG with PDF documents using LanceDB for vector storage.
Downloads a sample PDF and creates a searchable knowledge base.
"""

import argparse
import sys
from pathlib import Path
import httpx

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section

DEFAULT_CONFIG = {
    "pdf_url": "https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
    "query": "How do I make chicken and galangal in coconut milk soup?",
}


def download_pdf(url: str, output_path: Path) -> bool:
    """Download PDF from URL to local path."""
    try:
        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()
        output_path.write_bytes(response.content)
        return True
    except Exception as e:
        print(f"  Failed to download: {e}")
        return False


def create_knowledge_base(pdf_path: Path, db_path: str = "tmp/pdf_rag_lancedb"):
    """Create knowledge base from PDF file."""
    return Knowledge(
        name="pdf_documents",
        vector_db=LanceDb(
            table_name="pdf_documents",
            uri=db_path,
        ),
    )


def create_agent(model, knowledge):
    """Create RAG agent with PDF knowledge base."""
    return Agent(
        name="PDFRagAgent",
        model=model,
        knowledge=knowledge,
        search_knowledge=True,
        instructions=[
            "Answer questions based on the provided PDF knowledge base",
            "If the answer isn't in the knowledge base, say so",
            "Cite specific sections or recipes when applicable",
        ],
        markdown=True,
    )


def get_agent(model=None):
    """Get agent for GUI integration."""
    if model is None:
        model = get_model()
    
    project_root = Path(__file__).parent.parent.parent.parent
    db_path = project_root / "tmp" / "pdf_rag_lancedb"
    
    knowledge = Knowledge(
        name="pdf_documents",
        vector_db=LanceDb(
            table_name="pdf_documents",
            uri=str(db_path),
        ),
    )
    
    return create_agent(model, knowledge)


def main():
    parser = argparse.ArgumentParser(
        description="RAG with PDF documents"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--pdf-url",
        type=str,
        default=DEFAULT_CONFIG["pdf_url"],
        help="URL of PDF to download and index"
    )
    parser.add_argument(
        "--pdf-path",
        type=str,
        default="",
        help="Local PDF path (skips download if provided)"
    )
    parser.add_argument(
        "--query",
        type=str,
        default=DEFAULT_CONFIG["query"],
        help="Question to ask about the PDF"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Force reload the PDF into the knowledge base"
    )
    
    args = parser.parse_args()
    
    print_header("PDF RAG Agent")
    
    project_root = Path(__file__).parent.parent.parent.parent
    cache_dir = project_root / "tmp" / "pdf_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = project_root / "tmp" / "pdf_rag_lancedb"
    
    if args.pdf_path:
        pdf_path = Path(args.pdf_path)
        if not pdf_path.exists():
            print(f"Error: PDF not found: {pdf_path}")
            sys.exit(1)
    else:
        pdf_name = args.pdf_url.split("/")[-1]
        pdf_path = cache_dir / pdf_name
        
        if not pdf_path.exists() or args.reload:
            print_section("Downloading PDF")
            print(f"  URL: {args.pdf_url[:60]}...")
            if not download_pdf(args.pdf_url, pdf_path):
                sys.exit(1)
            print(f"  Saved: {pdf_path}")
    
    print_section("Configuration")
    print(f"  PDF: {pdf_path.name}")
    print(f"  Vector DB: LanceDB (local)")
    print()
    
    print_section("Building Knowledge Base...")
    
    try:
        knowledge = Knowledge(
            name="pdf_documents",
            vector_db=LanceDb(
                table_name="pdf_documents",
                uri=str(db_path),
            ),
        )
        
        table_path = db_path / "pdf_documents.lance"
        if args.reload or not table_path.exists():
            print("  Indexing PDF (first run or reload)...")
            knowledge.add_content(path=str(pdf_path))
        else:
            print("  Using cached index (use --reload to refresh)")
        
        print("  Knowledge base ready!")
        
    except Exception as e:
        print(f"  Error: {e}")
        print("\n  Tip: Make sure you have: pip install pypdf lancedb")
        sys.exit(1)
    
    print()
    print_section("Query")
    print(f"  {args.query}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model, knowledge)
    
    print_section("Searching knowledge base...")
    
    try:
        response = agent.run(args.query)
        
        print_section("Answer")
        print(response.content)
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
