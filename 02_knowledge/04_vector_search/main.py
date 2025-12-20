#!/usr/bin/env python3
"""
Lesson 04: Vector Search Deep Dive

Concepts covered:
- How embeddings work
- LanceDB vector storage
- Similarity search mechanics
- Tuning retrieval parameters

Run: python main.py
     python main.py --num-docs 10
     python main.py --query "How do agents work?"
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.knowledge.text import TextKnowledge
from agno.vectordb.lancedb import LanceDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# Sample knowledge chunks to demonstrate vector search
KNOWLEDGE_CHUNKS = [
    """
    Agents in Agno are AI programs where a language model controls execution flow.
    The model decides whether to reason, use tools, or respond to the user.
    Agents are created using the Agent class with a model and optional instructions.
    """,
    """
    Tools extend agent capabilities by allowing them to interact with external systems.
    Tools are Python functions that agents can call to fetch data or perform actions.
    Agno includes 100+ pre-built tools and supports custom tool creation.
    """,
    """
    Knowledge bases enable RAG (Retrieval-Augmented Generation) patterns.
    Documents are chunked, embedded into vectors, and stored in a vector database.
    When a query is made, relevant chunks are retrieved and added to the LLM context.
    """,
    """
    Memory allows agents to remember information across sessions.
    User memories persist preferences, facts, and context about the user.
    Session state provides temporary storage within a single conversation.
    """,
    """
    Teams enable multi-agent collaboration for complex tasks.
    A team has a leader agent that coordinates work among member agents.
    Teams can operate in coordinate, route, or collaborate modes.
    """,
    """
    Workflows provide structured orchestration of agent tasks.
    Each workflow step can involve different agents or operations.
    Workflows support sequential, parallel, and conditional execution.
    """,
    """
    Vector search finds similar content using mathematical distance metrics.
    Common metrics include cosine similarity and Euclidean distance.
    The embedding model converts text to high-dimensional vectors.
    """,
    """
    LanceDB is a local vector database that requires no server setup.
    It stores vectors in the Lance format for fast similarity search.
    LanceDB supports both exact and approximate nearest neighbor search.
    """,
]


def create_text_knowledge(lancedb_path: Path, rebuild: bool = False):
    """Create a knowledge base from text chunks."""
    # Combine chunks into a single text for demonstration
    combined_text = "\n\n".join(KNOWLEDGE_CHUNKS)
    
    # Create a temporary file
    temp_file = lancedb_path.parent / "sample_data" / "knowledge_chunks.txt"
    temp_file.parent.mkdir(exist_ok=True)
    temp_file.write_text(combined_text)
    
    knowledge = TextKnowledge(
        path=str(temp_file),
        vector_db=LanceDb(
            table_name="vector_search_demo",
            uri=str(lancedb_path),
        ),
    )
    
    knowledge.load(recreate=rebuild)
    return knowledge



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        model=model,
knowledge=knowledge,
search_knowledge=True,
num_documents=args.num_docs,  # Control retrieval count
instructions=[
"You are a helpful assistant explaining Agno concepts.",
"Use the retrieved context to answer accurately.",
"If information isn't available, say so.",
],
show_tool_calls=True,
markdown=True,
    )


def main():
    """Demonstrate vector search concepts."""
    parser = argparse.ArgumentParser(
        description="Vector Search Deep Dive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--query",
        type=str,
        default="How do vector databases work?",
        help="Search query",
    )
    parser.add_argument(
        "--num-docs",
        type=int,
        default=3,
        help="Number of documents to retrieve (default: 3)",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force rebuild the knowledge base",
    )
    parser.add_argument(
        "--show-chunks",
        action="store_true",
        help="Show the indexed chunks",
    )
    args = parser.parse_args()

    print_header("Lesson 04: Vector Search Deep Dive")

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

    if args.show_chunks:
        print_section("Knowledge Chunks")
        for i, chunk in enumerate(KNOWLEDGE_CHUNKS, 1):
            print(f"Chunk {i}:")
            print(f"  {chunk.strip()[:100]}...")
            print()

    print_section("Building Vector Index")
    print(f"Chunks: {len(KNOWLEDGE_CHUNKS)}")
    print(f"Vector DB: {lancedb_path}")
    
    try:
        knowledge = create_text_knowledge(lancedb_path, args.rebuild)
        print("Vector index ready!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print_section("How Vector Search Works")
    print(f"""
    1. EMBEDDING
       Your query: "{args.query}"
       → Converted to a 1536-dimensional vector
       
    2. SIMILARITY SEARCH
       → Compare query vector to all stored vectors
       → Find {args.num_docs} most similar chunks
       
    3. RETRIEVAL
       → Return top {args.num_docs} chunks as context
       → LLM uses context to generate answer
    """)

    print_section("Creating RAG Agent")
    
    agent = get_agent(model)

    print_section(f"Query (retrieving {args.num_docs} chunks)")
    print(f"Question: {args.query}\n")
    
    print("Answer:")
    print("-" * 60)
    agent.print_response(args.query)
    print("-" * 60)

    print_section("Vector Search Concepts")
    print("""
    EMBEDDINGS
    ----------
    Text → Vector (1536 dimensions for OpenAI embeddings)
    
    "cat" → [0.1, -0.3, 0.8, 0.2, ...]
    "dog" → [0.15, -0.28, 0.75, 0.18, ...]  (similar!)
    "car" → [-0.5, 0.9, -0.1, 0.3, ...]     (different!)
    
    SIMILARITY METRICS
    ------------------
    Cosine Similarity: angle between vectors (0 to 1)
    Euclidean Distance: straight-line distance
    
    CHUNKING STRATEGIES
    -------------------
    - Fixed size (500 chars)
    - Sentence-based
    - Paragraph-based
    - Semantic (by topic)
    
    TUNING TIPS
    -----------
    - More chunks = more context but more noise
    - Smaller chunks = precise but may miss context
    - Overlap helps with context continuity
    """)

    print("\nTry: python main.py --num-docs 5 --query \"Your question\"")


if __name__ == "__main__":
    main()
