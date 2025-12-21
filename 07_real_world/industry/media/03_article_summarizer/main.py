"""
Example #163: Article Summarizer Agent
Category: industry/media
DESCRIPTION: Summarizes articles into different formats and lengths
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"length": "medium", "format": "bullet_points", "audience": "general"}

class ArticleSummary(BaseModel):
    title: str = Field(description="Article title")
    one_liner: str = Field(description="One sentence summary")
    key_points: list[str] = Field(description="Key takeaways")
    detailed_summary: str = Field(description="Detailed summary paragraph")
    twitter_thread: list[str] = Field(description="Twitter thread format")
    linkedin_post: str = Field(description="LinkedIn post format")
    keywords: list[str] = Field(description="Main keywords")
    reading_time_saved: str = Field(description="Time saved vs reading full article")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Article Summarizer",
        instructions=[
            "You are an expert content summarizer.",
            f"Create {cfg['length']} length summaries",
            f"Format as {cfg['format']} for {cfg['audience']} audience",
            "Preserve key insights and data points",
            "Maintain accuracy while condensing",
            "Create platform-specific versions",
        ],
        output_schema=ArticleSummary,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Article Summarizer Agent - Demo")
    print("=" * 60)
    sample_article = """Tech giants are investing billions in AI research, with breakthroughs
in natural language processing leading the way. Recent developments show AI can now
write code, create art, and engage in complex reasoning. Experts predict AI will
transform industries from healthcare to finance within the next decade. However,
concerns about job displacement and ethical use remain significant challenges."""
    query = f"""Summarize this article:
{sample_article}

Create {config['length']} summary in {config['format']} format for {config['audience']} audience."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ArticleSummary):
        print(f"\n📰 {result.title}")
        print(f"\n💡 TL;DR: {result.one_liner}")
        print(f"\n📋 Key Points:")
        for pt in result.key_points[:4]:
            print(f"  • {pt}")
        print(f"\n🐦 Twitter Thread (first 2):")
        for tweet in result.twitter_thread[:2]:
            print(f"  {tweet}")
        print(f"\n⏱️ {result.reading_time_saved}")

def main():
    parser = argparse.ArgumentParser(description="Article Summarizer Agent")
    parser.add_argument("--length", "-l", default=DEFAULT_CONFIG["length"], choices=["short", "medium", "long"])
    parser.add_argument("--format", "-f", default=DEFAULT_CONFIG["format"])
    parser.add_argument("--audience", "-a", default=DEFAULT_CONFIG["audience"])
    args = parser.parse_args()
    config = {"length": args.length, "format": args.format, "audience": args.audience}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
