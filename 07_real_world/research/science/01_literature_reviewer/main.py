"""
Example #171: Literature Reviewer Agent
Category: research/science
DESCRIPTION: Reviews and synthesizes scientific literature on a topic
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"topic": "machine learning in drug discovery", "years": 5, "focus": "methodology"}

class PaperSummary(BaseModel):
    title: str = Field(description="Paper title")
    authors: str = Field(description="Key authors")
    year: int = Field(description="Publication year")
    key_finding: str = Field(description="Main finding")
    methodology: str = Field(description="Research methodology")
    relevance: int = Field(description="Relevance score 0-100")

class LiteratureReview(BaseModel):
    topic: str = Field(description="Research topic")
    review_scope: str = Field(description="Scope of review")
    key_papers: list[PaperSummary] = Field(description="Key papers reviewed")
    major_themes: list[str] = Field(description="Major research themes")
    methodology_trends: list[str] = Field(description="Methodology trends")
    research_gaps: list[str] = Field(description="Identified gaps")
    future_directions: list[str] = Field(description="Suggested future research")
    synthesis: str = Field(description="Overall synthesis")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Literature Reviewer",
        instructions=[
            "You are an expert scientific literature reviewer.",
            f"Review literature on {cfg['topic']} from the past {cfg['years']} years",
            f"Focus on {cfg['focus']} aspects",
            "Identify key themes and research gaps",
            "Synthesize findings across papers",
            "Suggest future research directions",
        ],
        output_schema=LiteratureReview,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Literature Reviewer Agent - Demo")
    print("=" * 60)
    query = f"""Review scientific literature on:
- Topic: {config['topic']}
- Timeframe: Past {config['years']} years
- Focus: {config['focus']}

Synthesize key findings and identify gaps."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, LiteratureReview):
        print(f"\n📚 {result.topic}")
        print(f"🔍 Scope: {result.review_scope}")
        print(f"\n📄 Key Papers:")
        for p in result.key_papers[:3]:
            print(f"  • {p.title} ({p.year})")
            print(f"    Finding: {p.key_finding[:60]}...")
        print(f"\n🎯 Themes: {', '.join(result.major_themes[:3])}")
        print(f"\n⚠️ Gaps:")
        for gap in result.research_gaps[:2]:
            print(f"  • {gap}")
        print(f"\n🔮 Future: {', '.join(result.future_directions[:2])}")

def main():
    parser = argparse.ArgumentParser(description="Literature Reviewer Agent")
    parser.add_argument("--topic", "-t", default=DEFAULT_CONFIG["topic"])
    parser.add_argument("--years", "-y", type=int, default=DEFAULT_CONFIG["years"])
    parser.add_argument("--focus", "-f", default=DEFAULT_CONFIG["focus"])
    args = parser.parse_args()
    config = {"topic": args.topic, "years": args.years, "focus": args.focus}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
