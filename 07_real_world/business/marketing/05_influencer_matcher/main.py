"""
Example #015: Influencer Matcher
Category: business/marketing

DESCRIPTION:
Finds and evaluates influencers for brand partnerships. Analyzes audience fit,
engagement authenticity, content alignment, and provides partnership
recommendations with estimated campaign ROI.

PATTERNS:
- Knowledge (influencer marketing best practices)
- Tools (web search for influencer research)
- Structured Output (InfluencerReport with matches)

ARGUMENTS:
- brand (str): Brand name. Default: "FitTech Pro"
- industry (str): Brand industry. Default: "fitness technology"
- budget (float): Campaign budget. Default: 25000
- goals (str): Campaign goals. Default: "awareness,engagement"
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "brand": "FitTech Pro",
    "industry": "fitness technology",
    "budget": 25000,
    "goals": "awareness,engagement",
    "target_audience": "health-conscious millennials and Gen Z",
}


# =============================================================================
# Output Schema
# =============================================================================

class InfluencerProfile(BaseModel):
    """Individual influencer evaluation."""
    
    name: str = Field(description="Influencer name or handle")
    platform: str = Field(description="Primary platform")
    follower_count: str = Field(description="Follower count range")
    engagement_rate: str = Field(description="Estimated engagement rate")
    content_style: str = Field(description="Content style description")
    audience_demographics: str = Field(description="Audience breakdown")
    brand_fit_score: int = Field(ge=0, le=100, description="Brand alignment 0-100")
    authenticity_score: int = Field(ge=0, le=100, description="Authenticity assessment 0-100")
    estimated_cpm: str = Field(description="Estimated cost per mille")
    past_brand_work: list[str] = Field(default_factory=list, description="Known brand partnerships")
    red_flags: list[str] = Field(default_factory=list, description="Potential concerns")


class PartnershipRecommendation(BaseModel):
    """Partnership structure recommendation."""
    
    influencer_name: str = Field(description="Influencer name")
    partnership_type: str = Field(description="Type (sponsored post, ambassador, etc.)")
    content_ideas: list[str] = Field(description="Suggested content concepts")
    estimated_cost: str = Field(description="Estimated partnership cost")
    expected_reach: str = Field(description="Expected reach")
    expected_engagement: str = Field(description="Expected engagement")
    roi_estimate: str = Field(description="Estimated ROI")


class InfluencerReport(BaseModel):
    """Complete influencer matching report."""
    
    campaign_summary: str = Field(description="Brief campaign overview")
    recommended_influencers: list[InfluencerProfile] = Field(description="Matched influencers")
    partnership_recommendations: list[PartnershipRecommendation] = Field(description="Partnership suggestions")
    budget_allocation: dict = Field(description="Suggested budget split")
    campaign_timeline: str = Field(description="Recommended timeline")
    success_metrics: list[str] = Field(description="KPIs to track")
    negotiation_tips: list[str] = Field(description="Tips for influencer negotiations")
    alternative_strategies: list[str] = Field(description="Alternative approaches if top picks unavailable")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Influencer Matcher agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for influencer matching
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Influencer Matcher",
        instructions=[
            "You are an expert influencer marketing strategist.",
            "Find and evaluate influencers for brand partnerships.",
            "",
            f"Brand: {cfg['brand']}",
            f"Industry: {cfg['industry']}",
            f"Budget: ${cfg['budget']:,.2f}",
            f"Goals: {cfg['goals']}",
            f"Target Audience: {cfg['target_audience']}",
            "",
            "Evaluation Criteria:",
            "- Audience Fit: Demographics match brand's target",
            "- Engagement Quality: Real engagement vs. bots",
            "- Content Alignment: Style fits brand voice",
            "- Past Performance: Track record with brand partnerships",
            "- Authenticity: Genuine connection with followers",
            "",
            "Influencer Tiers:",
            "- Nano (1K-10K): High engagement, niche, affordable",
            "- Micro (10K-100K): Strong engagement, focused audiences",
            "- Mid-Tier (100K-500K): Balance of reach and engagement",
            "- Macro (500K-1M): Wide reach, lower engagement rate",
            "- Mega (1M+): Celebrity status, brand awareness focus",
            "",
            "Research influencers in the brand's industry and provide detailed evaluations.",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=InfluencerReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of influencer matching."""
    print("\n" + "=" * 60)
    print("  Influencer Matcher - Demo")
    print("=" * 60)
    
    brand = config.get("brand", DEFAULT_CONFIG["brand"])
    industry = config.get("industry", DEFAULT_CONFIG["industry"])
    budget = config.get("budget", DEFAULT_CONFIG["budget"])
    goals = config.get("goals", DEFAULT_CONFIG["goals"])
    audience = config.get("target_audience", DEFAULT_CONFIG["target_audience"])
    
    query = f"""
    Find influencer partners for:
    
    Brand: {brand}
    Industry: {industry}
    Budget: ${budget:,.2f}
    Campaign Goals: {goals}
    Target Audience: {audience}
    
    1. Search for relevant influencers in the {industry} space
    2. Evaluate 3-5 potential matches
    3. Provide partnership recommendations
    4. Suggest budget allocation and timeline
    """
    
    print(f"\nBrand: {brand}")
    print(f"Industry: {industry}")
    print(f"Budget: ${budget:,.2f}")
    print("-" * 40)
    print("Searching for influencers...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, InfluencerReport):
        print(f"\n{'='*50}")
        print(f"INFLUENCER MATCHING REPORT")
        print(f"{'='*50}")
        
        print(f"\n📋 Campaign: {result.campaign_summary}")
        
        print(f"\n👤 Recommended Influencers:")
        for inf in result.recommended_influencers:
            print(f"\n  {inf.name} ({inf.platform})")
            print(f"    Followers: {inf.follower_count} | Engagement: {inf.engagement_rate}")
            print(f"    Brand Fit: {inf.brand_fit_score}/100 | Authenticity: {inf.authenticity_score}/100")
            print(f"    Style: {inf.content_style}")
            print(f"    CPM: {inf.estimated_cpm}")
            if inf.past_brand_work:
                print(f"    Past Brands: {', '.join(inf.past_brand_work[:3])}")
            if inf.red_flags:
                print(f"    ⚠️ Concerns: {', '.join(inf.red_flags)}")
        
        print(f"\n🤝 Partnership Recommendations:")
        for rec in result.partnership_recommendations:
            print(f"\n  {rec.influencer_name} - {rec.partnership_type}")
            print(f"    Cost: {rec.estimated_cost} | ROI: {rec.roi_estimate}")
            print(f"    Reach: {rec.expected_reach} | Engagement: {rec.expected_engagement}")
            print(f"    Content Ideas:")
            for idea in rec.content_ideas[:2]:
                print(f"      • {idea}")
        
        print(f"\n💰 Budget Allocation:")
        for channel, pct in result.budget_allocation.items():
            print(f"  {channel}: {pct}")
        
        print(f"\n📅 Timeline: {result.campaign_timeline}")
        
        print(f"\n📊 Success Metrics:")
        for metric in result.success_metrics[:4]:
            print(f"  • {metric}")
        
        print(f"\n💡 Negotiation Tips:")
        for tip in result.negotiation_tips[:3]:
            print(f"  • {tip}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Influencer Matcher - Find brand-aligned influencers"
    )
    
    parser.add_argument(
        "--brand", "-b",
        type=str,
        default=DEFAULT_CONFIG["brand"],
        help=f"Brand name (default: {DEFAULT_CONFIG['brand']})"
    )
    parser.add_argument(
        "--industry", "-i",
        type=str,
        default=DEFAULT_CONFIG["industry"],
        help=f"Industry (default: {DEFAULT_CONFIG['industry']})"
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=DEFAULT_CONFIG["budget"],
        help=f"Campaign budget (default: {DEFAULT_CONFIG['budget']})"
    )
    parser.add_argument(
        "--goals", "-g",
        type=str,
        default=DEFAULT_CONFIG["goals"],
        help=f"Campaign goals (default: {DEFAULT_CONFIG['goals']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "brand": args.brand,
        "industry": args.industry,
        "budget": args.budget,
        "goals": args.goals,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
