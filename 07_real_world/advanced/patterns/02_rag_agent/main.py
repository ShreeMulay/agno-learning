"""
Example #222: RAG Agent (Retrieval-Augmented Generation)
Category: advanced/patterns
DESCRIPTION: Agent that retrieves relevant context before generating responses
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"knowledge_base": "product_docs"}

# Simulated knowledge base
KNOWLEDGE_BASE = {
    "product_docs": [
        {"id": 1, "content": "Our API rate limit is 1000 requests per minute per API key.", "topic": "api"},
        {"id": 2, "content": "Authentication requires a Bearer token in the Authorization header.", "topic": "auth"},
        {"id": 3, "content": "The webhook endpoint accepts POST requests with JSON payload.", "topic": "webhooks"},
        {"id": 4, "content": "Data is retained for 90 days in the standard plan.", "topic": "data"},
        {"id": 5, "content": "Enterprise plans include SSO integration and custom retention.", "topic": "enterprise"},
    ]
}

def retrieve_context(query: str, kb_name: str = "product_docs") -> list[str]:
    """Simple keyword-based retrieval (in production, use vector search)."""
    kb = KNOWLEDGE_BASE.get(kb_name, [])
    query_words = set(query.lower().split())
    results = []
    for doc in kb:
        doc_words = set(doc["content"].lower().split())
        if query_words & doc_words:
            results.append(doc["content"])
    return results[:3] if results else [kb[0]["content"]] if kb else []

class RAGResponse(BaseModel):
    query: str = Field(description="User question")
    retrieved_context: list[str] = Field(description="Retrieved documents")
    answer: str = Field(description="Generated answer")
    confidence: str = Field(description="Answer confidence: high, medium, low")
    sources_used: int = Field(description="Number of sources referenced")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="RAG Agent",
        instructions=[
            f"You answer questions using the {cfg['knowledge_base']} knowledge base.",
            "Base your answers on the retrieved context provided.",
            "If context doesn't contain the answer, say so clearly.",
            "Cite which sources informed your answer.",
        ],
        output_schema=RAGResponse,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  RAG Agent - Demo")
    print("=" * 60)
    
    query = "What is the API rate limit and how do I authenticate?"
    context = retrieve_context(query, config.get("knowledge_base", "product_docs"))
    
    print(f"\n❓ Query: {query}")
    print(f"📚 Retrieved {len(context)} documents")
    
    augmented_query = f"""
    User Question: {query}
    
    Retrieved Context:
    {chr(10).join(f'- {c}' for c in context)}
    
    Answer based on the context above."""
    
    response = agent.run(augmented_query)
    
    if isinstance(response.content, RAGResponse):
        r = response.content
        print(f"\n✅ Answer: {r.answer}")
        print(f"📊 Confidence: {r.confidence} | Sources: {r.sources_used}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--knowledge-base", "-k", default=DEFAULT_CONFIG["knowledge_base"])
    args = parser.parse_args()
    run_demo(get_agent(config={"knowledge_base": args.knowledge_base}), {"knowledge_base": args.knowledge_base})

if __name__ == "__main__": main()
