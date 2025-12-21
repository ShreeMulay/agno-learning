"""
Example #168: Influencer Matcher Agent
Category: industry/media
DESCRIPTION: Matches brands with suitable influencers for partnerships
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"brand_niche": "sustainable fashion", "budget": 5000, "platform": "instagram"}

class InfluencerMatch(BaseModel):
    name: str = Field(description="Influencer name/handle")
    followers: str = Field(description="Follower count")
    engagement_rate: float = Field(description="Engagement rate percentage")
    niche_alignment: int = Field(description="Niche alignment score 0-100")
    estimated_cost: str = Field(description="Estimated partnership cost")
    content_style: str = Field(description="Content style description")
    audience_match: str = Field(description="Audience match assessment")

class InfluencerMatching(BaseModel):
    brand_niche: str = Field(description="Brand niche")
    budget: int = Field(description="Campaign budget")
    matches: list[InfluencerMatch] = Field(description="Matched influencers")
    tier_breakdown: dict = Field(description="Breakdown by influencer tier")
    outreach_strategy: str = Field(description="Recommended outreach approach")
    campaign_ideas: list[str] = Field(description="Campaign collaboration ideas")
    red_flags_to_watch: list[str] = Field(description="Warning signs to avoid")
    roi_expectations: str = Field(description="Expected ROI")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Influencer Matcher",
        instructions=[
            "You are an expert influencer marketing strategist.",
            f"Find influencers for {cfg['brand_niche']} brands",
            f"Work within ${cfg['budget']} budget on {cfg['platform']}",
            "Prioritize engagement over follower count",
            "Consider audience authenticity and brand safety",
            "Provide outreach and collaboration strategies",
        ],
        output_schema=InfluencerMatching,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Influencer Matcher Agent - Demo")
    print("=" * 60)
    query = f"""Find influencer matches:
- Brand Niche: {config['brand_niche']}
- Budget: ${config['budget']}
- Platform: {config['platform']}

Identify suitable influencers for partnership."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, InfluencerMatching):
        print(f"\n🎯 {result.brand_niche} Influencer Search (${result.budget} budget)")
        print(f"\n👥 Top Matches:")
        for inf in result.matches[:4]:
            print(f"  • {inf.name} ({inf.followers})")
            print(f"    Engagement: {inf.engagement_rate}% | Alignment: {inf.niche_alignment}%")
            print(f"    Cost: {inf.estimated_cost}")
        print(f"\n📧 Outreach: {result.outreach_strategy}")
        print(f"\n💡 Campaign Ideas:")
        for idea in result.campaign_ideas[:2]:
            print(f"  • {idea}")
        print(f"\n📈 ROI: {result.roi_expectations}")

def main():
    parser = argparse.ArgumentParser(description="Influencer Matcher Agent")
    parser.add_argument("--niche", "-n", default=DEFAULT_CONFIG["brand_niche"])
    parser.add_argument("--budget", "-b", type=int, default=DEFAULT_CONFIG["budget"])
    parser.add_argument("--platform", "-p", default=DEFAULT_CONFIG["platform"])
    args = parser.parse_args()
    config = {"brand_niche": args.niche, "budget": args.budget, "platform": args.platform}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
