"""
Example #164: Trend Analyzer Agent
Category: industry/media
DESCRIPTION: Analyzes trending topics and predicts content opportunities
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"industry": "technology", "timeframe": "this week", "region": "US"}

class TrendingTopic(BaseModel):
    topic: str = Field(description="Trending topic")
    momentum: str = Field(description="rising/stable/declining")
    volume: str = Field(description="Search/mention volume")
    relevance_score: int = Field(description="Relevance to industry 0-100")
    content_angle: str = Field(description="Suggested content angle")

class TrendAnalysis(BaseModel):
    industry: str = Field(description="Industry analyzed")
    timeframe: str = Field(description="Analysis timeframe")
    top_trends: list[TrendingTopic] = Field(description="Top trending topics")
    emerging_trends: list[str] = Field(description="Early-stage emerging trends")
    declining_trends: list[str] = Field(description="Fading trends to avoid")
    content_opportunities: list[str] = Field(description="Content opportunities")
    hashtags_to_use: list[str] = Field(description="Trending hashtags")
    timing_recommendation: str = Field(description="When to publish")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Trend Analyzer",
        instructions=[
            "You are an expert trend analyst and content strategist.",
            f"Analyze trends in the {cfg['industry']} industry",
            f"Focus on {cfg['region']} region trends",
            "Identify content opportunities from trends",
            "Distinguish between lasting trends and fads",
            "Provide actionable content recommendations",
        ],
        output_schema=TrendAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Trend Analyzer Agent - Demo")
    print("=" * 60)
    query = f"""Analyze current trends:
- Industry: {config['industry']}
- Timeframe: {config['timeframe']}
- Region: {config['region']}

Identify trends and content opportunities."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, TrendAnalysis):
        print(f"\n📊 {result.industry} Trends ({result.timeframe})")
        print(f"\n🔥 Top Trends:")
        for t in result.top_trends[:4]:
            print(f"  • {t.topic} ({t.momentum}) - {t.relevance_score}% relevant")
            print(f"    Angle: {t.content_angle}")
        print(f"\n🌱 Emerging: {', '.join(result.emerging_trends[:3])}")
        print(f"📉 Declining: {', '.join(result.declining_trends[:3])}")
        print(f"\n#️⃣ Hashtags: {' '.join(result.hashtags_to_use[:5])}")
        print(f"⏰ Timing: {result.timing_recommendation}")

def main():
    parser = argparse.ArgumentParser(description="Trend Analyzer Agent")
    parser.add_argument("--industry", "-i", default=DEFAULT_CONFIG["industry"])
    parser.add_argument("--timeframe", "-t", default=DEFAULT_CONFIG["timeframe"])
    parser.add_argument("--region", "-r", default=DEFAULT_CONFIG["region"])
    args = parser.parse_args()
    config = {"industry": args.industry, "timeframe": args.timeframe, "region": args.region}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
