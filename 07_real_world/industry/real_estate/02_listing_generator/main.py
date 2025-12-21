"""
Example #132: Listing Generator Agent
Category: industry/real_estate
DESCRIPTION: Creates compelling property listings for MLS and marketing
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"property_type": "single_family", "bedrooms": 4, "bathrooms": 2.5, "features": "updated kitchen, pool, large backyard"}

class PropertyListing(BaseModel):
    headline: str = Field(description="Attention-grabbing headline")
    description: str = Field(description="Full property description")
    highlights: list[str] = Field(description="Key selling points")
    mls_description: str = Field(description="Concise MLS-formatted description")
    social_media_post: str = Field(description="Short social media caption")
    seo_keywords: list[str] = Field(description="Keywords for online visibility")
    call_to_action: str = Field(description="Compelling CTA for buyers")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Listing Generator",
        instructions=[
            "You are an expert real estate copywriter specializing in property listings.",
            f"Create listings for {cfg['property_type']} properties",
            "Write compelling, accurate descriptions that sell",
            "Highlight unique features and lifestyle benefits",
            "Use power words that create urgency without being pushy",
            "Optimize for both MLS requirements and online search",
        ],
        output_schema=PropertyListing,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Listing Generator Agent - Demo")
    print("=" * 60)
    query = f"""Create a compelling listing for:
- Type: {config['property_type']}
- Bedrooms: {config['bedrooms']} | Bathrooms: {config['bathrooms']}
- Features: {config['features']}

Generate headline, description, and marketing content."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PropertyListing):
        print(f"\n📝 Headline: {result.headline}")
        print(f"\n📖 Description:\n{result.description[:300]}...")
        print(f"\n⭐ Highlights:")
        for h in result.highlights[:4]:
            print(f"  • {h}")
        print(f"\n📱 Social: {result.social_media_post[:100]}...")
        print(f"\n🎯 CTA: {result.call_to_action}")

def main():
    parser = argparse.ArgumentParser(description="Listing Generator Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["property_type"])
    parser.add_argument("--beds", "-b", type=float, default=DEFAULT_CONFIG["bedrooms"])
    parser.add_argument("--baths", type=float, default=DEFAULT_CONFIG["bathrooms"])
    parser.add_argument("--features", "-f", default=DEFAULT_CONFIG["features"])
    args = parser.parse_args()
    config = {"property_type": args.type, "bedrooms": args.beds, "bathrooms": args.baths, "features": args.features}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
