"""
Example #134: Market Analyzer Agent
Category: industry/real_estate
DESCRIPTION: Analyzes real estate market trends and conditions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"location": "Denver, CO", "property_type": "single_family", "timeframe": "6 months"}

class MarketMetrics(BaseModel):
    median_price: int = Field(description="Median sale price")
    price_change_pct: float = Field(description="Price change percentage")
    days_on_market: int = Field(description="Average days on market")
    inventory_months: float = Field(description="Months of inventory")
    list_to_sale_ratio: float = Field(description="List price to sale price ratio")

class MarketAnalysis(BaseModel):
    market_type: str = Field(description="Buyer's, seller's, or balanced market")
    metrics: MarketMetrics = Field(description="Key market metrics")
    trends: list[str] = Field(description="Current market trends")
    forecast: str = Field(description="Short-term market forecast")
    opportunities: list[str] = Field(description="Investment opportunities")
    risks: list[str] = Field(description="Market risks to consider")
    recommendation: str = Field(description="Buy/sell/hold recommendation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Market Analyzer",
        instructions=[
            "You are an expert real estate market analyst.",
            f"Analyze the {cfg['location']} market for {cfg['property_type']} properties",
            f"Focus on trends over the past {cfg['timeframe']}",
            "Provide data-driven insights with realistic metrics",
            "Consider economic factors, interest rates, and local conditions",
            "Give actionable recommendations for buyers and sellers",
        ],
        output_schema=MarketAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Market Analyzer Agent - Demo")
    print("=" * 60)
    query = f"""Analyze the real estate market:
- Location: {config['location']}
- Property Type: {config['property_type']}
- Timeframe: {config['timeframe']}

Provide comprehensive market analysis with metrics and recommendations."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, MarketAnalysis):
        print(f"\n📊 Market Type: {result.market_type}")
        m = result.metrics
        print(f"\n📈 Key Metrics:")
        print(f"  • Median Price: ${m.median_price:,}")
        print(f"  • Price Change: {m.price_change_pct:+.1f}%")
        print(f"  • Days on Market: {m.days_on_market}")
        print(f"  • Inventory: {m.inventory_months:.1f} months")
        print(f"\n🔮 Forecast: {result.forecast}")
        print(f"\n💡 Recommendation: {result.recommendation}")

def main():
    parser = argparse.ArgumentParser(description="Market Analyzer Agent")
    parser.add_argument("--location", "-l", default=DEFAULT_CONFIG["location"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["property_type"])
    parser.add_argument("--timeframe", "-tf", default=DEFAULT_CONFIG["timeframe"])
    args = parser.parse_args()
    config = {"location": args.location, "property_type": args.type, "timeframe": args.timeframe}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
