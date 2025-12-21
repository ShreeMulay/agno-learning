"""
Example #165: Audience Insights Agent
Category: industry/media
DESCRIPTION: Analyzes audience demographics and behavior patterns
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"platform": "instagram", "account_type": "brand", "niche": "fitness"}

class AudienceSegment(BaseModel):
    segment_name: str = Field(description="Segment name")
    percentage: float = Field(description="Percentage of audience")
    characteristics: list[str] = Field(description="Key characteristics")
    content_preferences: list[str] = Field(description="Preferred content types")
    engagement_pattern: str = Field(description="When they engage")

class AudienceInsights(BaseModel):
    platform: str = Field(description="Platform analyzed")
    total_audience_size: str = Field(description="Estimated audience size")
    segments: list[AudienceSegment] = Field(description="Audience segments")
    peak_activity_times: list[str] = Field(description="Peak activity times")
    top_interests: list[str] = Field(description="Top audience interests")
    content_recommendations: list[str] = Field(description="Content to create")
    growth_opportunities: list[str] = Field(description="Growth opportunities")
    competitor_comparison: str = Field(description="Competitor audience notes")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Audience Insights",
        instructions=[
            "You are an expert audience analytics specialist.",
            f"Analyze {cfg['platform']} audiences for {cfg['account_type']} accounts",
            f"Focus on the {cfg['niche']} niche",
            "Identify distinct audience segments",
            "Provide actionable content recommendations",
            "Consider engagement patterns and preferences",
        ],
        output_schema=AudienceInsights,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Audience Insights Agent - Demo")
    print("=" * 60)
    query = f"""Analyze audience for:
- Platform: {config['platform']}
- Account Type: {config['account_type']}
- Niche: {config['niche']}

Provide detailed audience insights and recommendations."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, AudienceInsights):
        print(f"\n📱 {result.platform} Audience ({result.total_audience_size})")
        print(f"\n👥 Segments:")
        for seg in result.segments[:3]:
            print(f"  • {seg.segment_name} ({seg.percentage}%)")
            print(f"    Traits: {', '.join(seg.characteristics[:2])}")
            print(f"    Prefers: {', '.join(seg.content_preferences[:2])}")
        print(f"\n⏰ Peak Times: {', '.join(result.peak_activity_times[:3])}")
        print(f"❤️ Interests: {', '.join(result.top_interests[:4])}")
        print(f"\n📈 Growth:")
        for opp in result.growth_opportunities[:2]:
            print(f"  • {opp}")

def main():
    parser = argparse.ArgumentParser(description="Audience Insights Agent")
    parser.add_argument("--platform", "-p", default=DEFAULT_CONFIG["platform"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["account_type"])
    parser.add_argument("--niche", "-n", default=DEFAULT_CONFIG["niche"])
    args = parser.parse_args()
    config = {"platform": args.platform, "account_type": args.type, "niche": args.niche}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
