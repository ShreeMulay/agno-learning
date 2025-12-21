"""
Example #146: Recommendation Engine Agent
Category: industry/ecommerce
DESCRIPTION: Generates personalized product recommendations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"customer_segment": "tech_enthusiast", "recent_purchase": "Laptop"}

class ProductRecommendation(BaseModel):
    product_name: str = Field(description="Recommended product")
    reason: str = Field(description="Why this recommendation")
    confidence: int = Field(description="Confidence score 0-100")
    recommendation_type: str = Field(description="cross_sell/upsell/complementary")
    price_range: str = Field(description="Price range")

class RecommendationResult(BaseModel):
    customer_profile: str = Field(description="Customer profile summary")
    recommendations: list[ProductRecommendation] = Field(description="Product recommendations")
    recommendation_strategy: str = Field(description="Strategy used")
    personalization_factors: list[str] = Field(description="Factors considered")
    bundle_suggestion: str = Field(description="Suggested product bundle")
    timing_note: str = Field(description="Best time to present offers")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Recommendation Engine",
        instructions=[
            "You are an expert e-commerce recommendation specialist.",
            f"Generate recommendations for {cfg['customer_segment']} customers",
            "Use collaborative filtering and content-based approaches",
            "Consider purchase history and browsing behavior",
            "Balance relevance with discovery and margin goals",
            "Provide explainable recommendations",
        ],
        output_schema=RecommendationResult,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Recommendation Engine Agent - Demo")
    print("=" * 60)
    query = f"""Generate personalized recommendations:
- Customer Segment: {config['customer_segment']}
- Recent Purchase: {config['recent_purchase']}
- Behavior: Browses electronics, reads reviews, price-conscious

Provide relevant product recommendations."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, RecommendationResult):
        print(f"\n👤 Profile: {result.customer_profile}")
        print(f"🎯 Strategy: {result.recommendation_strategy}")
        print(f"\n📦 Recommendations:")
        for r in result.recommendations[:4]:
            print(f"  • {r.product_name} ({r.confidence}% confidence)")
            print(f"    Type: {r.recommendation_type} | {r.price_range}")
            print(f"    Why: {r.reason}")
        print(f"\n🎁 Bundle: {result.bundle_suggestion}")
        print(f"⏰ Timing: {result.timing_note}")

def main():
    parser = argparse.ArgumentParser(description="Recommendation Engine Agent")
    parser.add_argument("--segment", "-s", default=DEFAULT_CONFIG["customer_segment"])
    parser.add_argument("--purchase", "-p", default=DEFAULT_CONFIG["recent_purchase"])
    args = parser.parse_args()
    config = {"customer_segment": args.segment, "recent_purchase": args.purchase}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
