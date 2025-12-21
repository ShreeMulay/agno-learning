"""
Example #142: Pricing Optimizer Agent
Category: industry/ecommerce
DESCRIPTION: Optimizes product pricing based on competition and demand
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"product": "Laptop Stand", "current_price": 49.99, "cost": 18.00}

class CompetitorPrice(BaseModel):
    competitor: str = Field(description="Competitor name")
    price: float = Field(description="Competitor price")
    notes: str = Field(description="Pricing notes")

class PricingRecommendation(BaseModel):
    recommended_price: float = Field(description="Recommended selling price")
    price_range_min: float = Field(description="Minimum viable price")
    price_range_max: float = Field(description="Maximum market price")
    margin_percentage: float = Field(description="Profit margin percentage")
    competitor_analysis: list[CompetitorPrice] = Field(description="Competitor pricing")
    pricing_strategy: str = Field(description="Recommended strategy")
    demand_assessment: str = Field(description="Demand level assessment")
    seasonal_factors: list[str] = Field(description="Seasonal considerations")
    action_items: list[str] = Field(description="Pricing action items")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Pricing Optimizer",
        instructions=[
            "You are an expert e-commerce pricing strategist.",
            f"Optimize pricing for products with cost around ${cfg['cost']:.2f}",
            "Analyze competitive landscape and demand signals",
            "Balance margin goals with market competitiveness",
            "Consider psychological pricing principles",
            "Provide actionable pricing recommendations",
        ],
        output_schema=PricingRecommendation,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Pricing Optimizer Agent - Demo")
    print("=" * 60)
    query = f"""Optimize pricing for this product:
- Product: {config['product']}
- Current Price: ${config['current_price']:.2f}
- Cost: ${config['cost']:.2f}

Analyze competition and recommend optimal pricing."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PricingRecommendation):
        print(f"\n💰 Recommended Price: ${result.recommended_price:.2f}")
        print(f"📊 Range: ${result.price_range_min:.2f} - ${result.price_range_max:.2f}")
        print(f"📈 Margin: {result.margin_percentage:.1f}%")
        print(f"\n🎯 Strategy: {result.pricing_strategy}")
        print(f"📉 Demand: {result.demand_assessment}")
        print(f"\n🏪 Competitors:")
        for c in result.competitor_analysis[:3]:
            print(f"  • {c.competitor}: ${c.price:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Pricing Optimizer Agent")
    parser.add_argument("--product", "-p", default=DEFAULT_CONFIG["product"])
    parser.add_argument("--price", type=float, default=DEFAULT_CONFIG["current_price"])
    parser.add_argument("--cost", "-c", type=float, default=DEFAULT_CONFIG["cost"])
    args = parser.parse_args()
    config = {"product": args.product, "current_price": args.price, "cost": args.cost}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
