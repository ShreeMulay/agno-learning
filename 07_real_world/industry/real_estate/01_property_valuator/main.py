"""
Example #131: Property Valuator Agent
Category: industry/real_estate
DESCRIPTION: Estimates property values using comparable sales and market data
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"property_type": "single_family", "square_feet": 2000, "bedrooms": 3, "location": "Austin, TX"}

class ComparableSale(BaseModel):
    address: str = Field(description="Address of comparable property")
    sale_price: int = Field(description="Sale price in dollars")
    sale_date: str = Field(description="Date of sale")
    adjustments: str = Field(description="Price adjustments for differences")

class PropertyValuation(BaseModel):
    estimated_value: int = Field(description="Estimated market value in dollars")
    value_range_low: int = Field(description="Low end of value range")
    value_range_high: int = Field(description="High end of value range")
    comparables: list[ComparableSale] = Field(description="Comparable sales used")
    valuation_method: str = Field(description="Method used for valuation")
    market_conditions: str = Field(description="Current market assessment")
    confidence_level: str = Field(description="Confidence in estimate: high/medium/low")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Property Valuator",
        instructions=[
            "You are an expert real estate appraiser and property valuation specialist.",
            f"Analyze properties of type: {cfg['property_type']}",
            "Use comparable sales approach as primary valuation method",
            "Consider location, condition, size, and amenities",
            "Provide realistic market-based valuations with supporting data",
            "Account for current market conditions and trends",
        ],
        output_schema=PropertyValuation,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Property Valuator Agent - Demo")
    print("=" * 60)
    query = f"""Provide a market valuation for this property:
- Type: {config['property_type']}
- Size: {config['square_feet']} sq ft
- Bedrooms: {config['bedrooms']}
- Location: {config['location']}

Include comparable sales and market analysis."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PropertyValuation):
        print(f"\n💰 Estimated Value: ${result.estimated_value:,}")
        print(f"📊 Value Range: ${result.value_range_low:,} - ${result.value_range_high:,}")
        print(f"📈 Method: {result.valuation_method}")
        print(f"🏠 Market: {result.market_conditions}")
        print(f"✅ Confidence: {result.confidence_level}")
        print(f"\n📋 Comparables ({len(result.comparables)}):")
        for comp in result.comparables[:3]:
            print(f"  • {comp.address}: ${comp.sale_price:,} ({comp.sale_date})")

def main():
    parser = argparse.ArgumentParser(description="Property Valuator Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["property_type"])
    parser.add_argument("--sqft", "-s", type=int, default=DEFAULT_CONFIG["square_feet"])
    parser.add_argument("--beds", "-b", type=int, default=DEFAULT_CONFIG["bedrooms"])
    parser.add_argument("--location", "-l", default=DEFAULT_CONFIG["location"])
    args = parser.parse_args()
    config = {"property_type": args.type, "square_feet": args.sqft, "bedrooms": args.beds, "location": args.location}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
