"""
Example #148: Shipping Optimizer Agent
Category: industry/ecommerce
DESCRIPTION: Optimizes shipping methods and carrier selection
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"destination": "Los Angeles, CA", "weight_lbs": 5.2, "value": 150.00}

class ShippingOption(BaseModel):
    carrier: str = Field(description="Shipping carrier")
    service: str = Field(description="Service level")
    cost: float = Field(description="Shipping cost")
    transit_days: int = Field(description="Transit time in days")
    reliability_score: int = Field(description="Reliability 0-100")

class ShippingOptimization(BaseModel):
    recommended_option: ShippingOption = Field(description="Best shipping option")
    all_options: list[ShippingOption] = Field(description="All available options")
    optimization_factors: list[str] = Field(description="Factors considered")
    cost_vs_speed_analysis: str = Field(description="Cost vs speed tradeoff")
    packaging_recommendation: str = Field(description="Packaging suggestion")
    insurance_recommendation: str = Field(description="Insurance recommendation")
    delivery_estimate: str = Field(description="Estimated delivery date")
    tracking_importance: str = Field(description="Tracking recommendation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Shipping Optimizer",
        instructions=[
            "You are an expert e-commerce shipping and logistics specialist.",
            f"Optimize shipping to {cfg['destination']}",
            "Compare carriers on cost, speed, and reliability",
            "Consider package dimensions, weight, and value",
            "Balance customer expectations with shipping costs",
            "Provide practical packaging recommendations",
        ],
        output_schema=ShippingOptimization,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Shipping Optimizer Agent - Demo")
    print("=" * 60)
    query = f"""Optimize shipping for this order:
- Destination: {config['destination']}
- Package Weight: {config['weight_lbs']} lbs
- Order Value: ${config['value']:.2f}
- Dimensions: 12x8x6 inches
- Contents: Electronics

Compare carriers and recommend best option."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ShippingOptimization):
        rec = result.recommended_option
        print(f"\n⭐ Recommended: {rec.carrier} {rec.service}")
        print(f"   Cost: ${rec.cost:.2f} | Transit: {rec.transit_days} days | Reliability: {rec.reliability_score}%")
        print(f"\n📦 All Options:")
        for opt in result.all_options[:4]:
            print(f"  • {opt.carrier} {opt.service}: ${opt.cost:.2f} ({opt.transit_days} days)")
        print(f"\n📊 Analysis: {result.cost_vs_speed_analysis}")
        print(f"📦 Packaging: {result.packaging_recommendation}")
        print(f"🛡️ Insurance: {result.insurance_recommendation}")
        print(f"📅 Delivery: {result.delivery_estimate}")

def main():
    parser = argparse.ArgumentParser(description="Shipping Optimizer Agent")
    parser.add_argument("--dest", "-d", default=DEFAULT_CONFIG["destination"])
    parser.add_argument("--weight", "-w", type=float, default=DEFAULT_CONFIG["weight_lbs"])
    parser.add_argument("--value", "-v", type=float, default=DEFAULT_CONFIG["value"])
    args = parser.parse_args()
    config = {"destination": args.dest, "weight_lbs": args.weight, "value": args.value}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
