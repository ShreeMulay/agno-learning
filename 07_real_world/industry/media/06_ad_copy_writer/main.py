"""
Example #166: Ad Copy Writer Agent
Category: industry/media
DESCRIPTION: Writes compelling ad copy for various platforms
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"product": "productivity app", "platform": "facebook", "objective": "conversions"}

class AdVariation(BaseModel):
    headline: str = Field(description="Ad headline")
    primary_text: str = Field(description="Primary ad text")
    cta: str = Field(description="Call to action")
    hook_type: str = Field(description="Type of hook used")
    character_count: int = Field(description="Total character count")

class AdCopyResult(BaseModel):
    product: str = Field(description="Product/service")
    platform: str = Field(description="Ad platform")
    variations: list[AdVariation] = Field(description="Ad copy variations")
    best_performer_prediction: str = Field(description="Predicted best performer")
    targeting_suggestions: list[str] = Field(description="Audience targeting tips")
    a_b_testing_plan: str = Field(description="A/B testing recommendation")
    compliance_notes: list[str] = Field(description="Platform compliance notes")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Ad Copy Writer",
        instructions=[
            "You are an expert advertising copywriter.",
            f"Write ads for {cfg['platform']} platform",
            f"Optimize for {cfg['objective']} objective",
            "Use proven copywriting formulas (AIDA, PAS, etc.)",
            "Create multiple variations for testing",
            "Follow platform-specific guidelines",
        ],
        output_schema=AdCopyResult,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Ad Copy Writer Agent - Demo")
    print("=" * 60)
    query = f"""Write ad copy for:
- Product: {config['product']}
- Platform: {config['platform']}
- Objective: {config['objective']}

Create multiple high-converting ad variations."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, AdCopyResult):
        print(f"\n📢 {result.product} Ads for {result.platform}")
        print(f"\n📝 Variations:")
        for i, ad in enumerate(result.variations[:3], 1):
            print(f"\n  --- Variation {i} ({ad.hook_type}) ---")
            print(f"  Headline: {ad.headline}")
            print(f"  Text: {ad.primary_text[:80]}...")
            print(f"  CTA: {ad.cta}")
        print(f"\n🏆 Best Performer: {result.best_performer_prediction}")
        print(f"\n🔬 A/B Plan: {result.a_b_testing_plan}")

def main():
    parser = argparse.ArgumentParser(description="Ad Copy Writer Agent")
    parser.add_argument("--product", "-p", default=DEFAULT_CONFIG["product"])
    parser.add_argument("--platform", default=DEFAULT_CONFIG["platform"])
    parser.add_argument("--objective", "-o", default=DEFAULT_CONFIG["objective"])
    args = parser.parse_args()
    config = {"product": args.product, "platform": args.platform, "objective": args.objective}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
