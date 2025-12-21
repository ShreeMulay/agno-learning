"""
Example #133: Buyer Matcher Agent
Category: industry/real_estate
DESCRIPTION: Matches buyer preferences with available properties
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"budget": 500000, "bedrooms_min": 3, "location": "suburban", "priorities": "good schools, quiet neighborhood"}

class PropertyMatch(BaseModel):
    property_id: str = Field(description="Property identifier")
    address: str = Field(description="Property address")
    price: int = Field(description="Listing price")
    match_score: int = Field(description="Match score 0-100")
    matching_features: list[str] = Field(description="Features matching buyer needs")
    tradeoffs: list[str] = Field(description="Potential compromises")

class BuyerMatchResult(BaseModel):
    buyer_profile_summary: str = Field(description="Summary of buyer preferences")
    top_matches: list[PropertyMatch] = Field(description="Best matching properties")
    market_insights: str = Field(description="Market conditions for this search")
    recommendation: str = Field(description="Agent recommendation")
    search_tips: list[str] = Field(description="Tips to improve search")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Buyer Matcher",
        instructions=[
            "You are an expert buyer's agent specializing in matching clients with properties.",
            f"Work within budget constraints around ${cfg['budget']:,}",
            "Prioritize buyer's stated preferences while suggesting alternatives",
            "Consider lifestyle needs, not just property features",
            "Provide honest assessments including potential tradeoffs",
            "Generate realistic property matches based on market knowledge",
        ],
        output_schema=BuyerMatchResult,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Buyer Matcher Agent - Demo")
    print("=" * 60)
    query = f"""Find property matches for this buyer:
- Budget: ${config['budget']:,}
- Minimum Bedrooms: {config['bedrooms_min']}
- Preferred Location: {config['location']}
- Priorities: {config['priorities']}

Provide top matches with analysis."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, BuyerMatchResult):
        print(f"\n👤 Profile: {result.buyer_profile_summary}")
        print(f"\n🏠 Top Matches ({len(result.top_matches)}):")
        for m in result.top_matches[:3]:
            print(f"  • {m.address} - ${m.price:,} (Score: {m.match_score}/100)")
            print(f"    ✓ {', '.join(m.matching_features[:2])}")
        print(f"\n📊 Market: {result.market_insights}")
        print(f"\n💡 Recommendation: {result.recommendation}")

def main():
    parser = argparse.ArgumentParser(description="Buyer Matcher Agent")
    parser.add_argument("--budget", "-b", type=int, default=DEFAULT_CONFIG["budget"])
    parser.add_argument("--beds", type=int, default=DEFAULT_CONFIG["bedrooms_min"])
    parser.add_argument("--location", "-l", default=DEFAULT_CONFIG["location"])
    parser.add_argument("--priorities", "-p", default=DEFAULT_CONFIG["priorities"])
    args = parser.parse_args()
    config = {"budget": args.budget, "bedrooms_min": args.beds, "location": args.location, "priorities": args.priorities}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
