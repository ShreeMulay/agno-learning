"""
Example #176: Citation Finder Agent
Category: research/science
DESCRIPTION: Finds relevant citations for research papers
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"topic": "neural networks for image recognition", "citation_type": "foundational", "count": 10}

class Citation(BaseModel):
    authors: str = Field(description="Authors")
    year: int = Field(description="Publication year")
    title: str = Field(description="Paper title")
    venue: str = Field(description="Journal/conference")
    relevance: str = Field(description="Why it's relevant")
    citation_context: str = Field(description="How to cite in your paper")

class CitationResults(BaseModel):
    topic: str = Field(description="Research topic")
    foundational: list[Citation] = Field(description="Foundational/classic papers")
    recent: list[Citation] = Field(description="Recent papers")
    methodology: list[Citation] = Field(description="Methodology papers")
    citation_tips: list[str] = Field(description="Citation best practices")
    gaps_identified: list[str] = Field(description="Citation gaps to fill")
    related_topics: list[str] = Field(description="Related topics to explore")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Citation Finder",
        instructions=[
            "You are an expert research citation specialist.",
            f"Find citations for {cfg['topic']}",
            f"Focus on {cfg['citation_type']} papers",
            "Include foundational and recent works",
            "Provide citation context suggestions",
            "Identify citation gaps",
        ],
        output_schema=CitationResults,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Citation Finder Agent - Demo")
    print("=" * 60)
    query = f"""Find citations for:
- Topic: {config['topic']}
- Type: {config['citation_type']}
- Count: {config['count']}

Identify key papers to cite."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CitationResults):
        print(f"\n📚 Citations for: {result.topic}")
        print(f"\n🏛️ Foundational Papers:")
        for c in result.foundational[:2]:
            print(f"  • {c.authors} ({c.year}) - {c.title}")
            print(f"    Context: {c.citation_context}")
        print(f"\n🆕 Recent Papers:")
        for c in result.recent[:2]:
            print(f"  • {c.authors} ({c.year}) - {c.title}")
        print(f"\n💡 Tips: {result.citation_tips[0]}")
        print(f"🔍 Related: {', '.join(result.related_topics[:3])}")

def main():
    parser = argparse.ArgumentParser(description="Citation Finder Agent")
    parser.add_argument("--topic", "-t", default=DEFAULT_CONFIG["topic"])
    parser.add_argument("--type", default=DEFAULT_CONFIG["citation_type"])
    parser.add_argument("--count", "-c", type=int, default=DEFAULT_CONFIG["count"])
    args = parser.parse_args()
    config = {"topic": args.topic, "citation_type": args.type, "count": args.count}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
