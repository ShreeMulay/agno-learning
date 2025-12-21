"""
Example #162: Headline Generator Agent
Category: industry/media
DESCRIPTION: Generates compelling headlines for articles and content
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"topic": "AI in healthcare", "tone": "informative", "platform": "blog"}

class HeadlineOption(BaseModel):
    headline: str = Field(description="The headline")
    style: str = Field(description="Headline style used")
    word_count: int = Field(description="Word count")
    power_words: list[str] = Field(description="Power words used")
    click_potential: int = Field(description="Click potential 0-100")

class HeadlineGeneration(BaseModel):
    topic: str = Field(description="Content topic")
    headlines: list[HeadlineOption] = Field(description="Generated headlines")
    top_pick: str = Field(description="Recommended headline")
    a_b_test_pair: list[str] = Field(description="Two headlines for A/B testing")
    seo_keywords: list[str] = Field(description="SEO keywords included")
    emotional_triggers: list[str] = Field(description="Emotional triggers used")
    tips: list[str] = Field(description="Headline writing tips")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Headline Generator",
        instructions=[
            "You are an expert headline copywriter.",
            f"Generate headlines with {cfg['tone']} tone",
            f"Optimize for {cfg['platform']} platform",
            "Use proven headline formulas",
            "Include power words and emotional triggers",
            "Balance clickability with accuracy",
        ],
        output_schema=HeadlineGeneration,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Headline Generator Agent - Demo")
    print("=" * 60)
    query = f"""Generate headlines for:
- Topic: {config['topic']}
- Tone: {config['tone']}
- Platform: {config['platform']}

Create compelling, click-worthy headlines."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, HeadlineGeneration):
        print(f"\n📝 Topic: {result.topic}")
        print(f"\n⭐ Top Pick: {result.top_pick}")
        print(f"\n📰 All Headlines:")
        for h in result.headlines[:5]:
            print(f"  • {h.headline}")
            print(f"    Style: {h.style} | Click: {h.click_potential}%")
        print(f"\n🔬 A/B Test:")
        for ab in result.a_b_test_pair:
            print(f"  • {ab}")

def main():
    parser = argparse.ArgumentParser(description="Headline Generator Agent")
    parser.add_argument("--topic", "-t", default=DEFAULT_CONFIG["topic"])
    parser.add_argument("--tone", default=DEFAULT_CONFIG["tone"])
    parser.add_argument("--platform", "-p", default=DEFAULT_CONFIG["platform"])
    args = parser.parse_args()
    config = {"topic": args.topic, "tone": args.tone, "platform": args.platform}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
