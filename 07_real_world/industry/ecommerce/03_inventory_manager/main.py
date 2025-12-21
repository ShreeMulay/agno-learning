"""
Example #143: Inventory Manager Agent
Category: industry/ecommerce
DESCRIPTION: Manages inventory levels and generates reorder recommendations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"sku": "WH-1000XM5", "current_stock": 45, "daily_sales_avg": 8}

class ReorderRecommendation(BaseModel):
    sku: str = Field(description="Product SKU")
    reorder_quantity: int = Field(description="Recommended reorder quantity")
    reorder_urgency: str = Field(description="urgent/normal/low urgency")
    days_until_stockout: int = Field(description="Days until stock runs out")
    safety_stock_level: int = Field(description="Recommended safety stock")

class InventoryAnalysis(BaseModel):
    stock_status: str = Field(description="healthy/low/critical stock status")
    current_stock: int = Field(description="Current stock level")
    average_daily_sales: float = Field(description="Average daily sales")
    reorder_recommendations: list[ReorderRecommendation] = Field(description="Reorder recommendations")
    stockout_risk: str = Field(description="Stockout risk assessment")
    inventory_turnover: float = Field(description="Inventory turnover ratio")
    carrying_cost_note: str = Field(description="Carrying cost consideration")
    demand_forecast: str = Field(description="Short-term demand forecast")
    action_items: list[str] = Field(description="Recommended actions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Inventory Manager",
        instructions=[
            "You are an expert e-commerce inventory management specialist.",
            f"Analyze inventory for SKU: {cfg['sku']}",
            "Calculate optimal reorder points and quantities",
            "Balance stockout risk with carrying costs",
            "Consider lead times and demand variability",
            "Provide actionable inventory recommendations",
        ],
        output_schema=InventoryAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Inventory Manager Agent - Demo")
    print("=" * 60)
    query = f"""Analyze inventory and provide recommendations:
- SKU: {config['sku']}
- Current Stock: {config['current_stock']} units
- Average Daily Sales: {config['daily_sales_avg']} units

Provide reorder recommendations and risk assessment."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, InventoryAnalysis):
        print(f"\n📦 Stock Status: {result.stock_status.upper()}")
        print(f"📊 Current: {result.current_stock} units | Daily Sales: {result.average_daily_sales}")
        print(f"⚠️ Stockout Risk: {result.stockout_risk}")
        print(f"\n🔄 Reorder Recommendations:")
        for r in result.reorder_recommendations[:2]:
            print(f"  • {r.sku}: Order {r.reorder_quantity} units ({r.reorder_urgency})")
            print(f"    Days to stockout: {r.days_until_stockout}")
        print(f"\n📈 Forecast: {result.demand_forecast}")

def main():
    parser = argparse.ArgumentParser(description="Inventory Manager Agent")
    parser.add_argument("--sku", "-s", default=DEFAULT_CONFIG["sku"])
    parser.add_argument("--stock", type=int, default=DEFAULT_CONFIG["current_stock"])
    parser.add_argument("--sales", type=float, default=DEFAULT_CONFIG["daily_sales_avg"])
    args = parser.parse_args()
    config = {"sku": args.sku, "current_stock": args.stock, "daily_sales_avg": args.sales}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
