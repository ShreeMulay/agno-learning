"""
Example #138: Investment Analyzer Agent
Category: industry/real_estate
DESCRIPTION: Analyzes real estate investment opportunities and ROI
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"purchase_price": 300000, "monthly_rent": 2200, "property_type": "rental"}

class InvestmentMetrics(BaseModel):
    cap_rate: float = Field(description="Capitalization rate percentage")
    cash_on_cash_return: float = Field(description="Cash on cash return percentage")
    gross_rent_multiplier: float = Field(description="Gross rent multiplier")
    monthly_cash_flow: int = Field(description="Net monthly cash flow")
    annual_roi: float = Field(description="Annual return on investment")
    break_even_occupancy: float = Field(description="Break-even occupancy rate")

class InvestmentAnalysis(BaseModel):
    property_summary: str = Field(description="Property investment summary")
    metrics: InvestmentMetrics = Field(description="Key investment metrics")
    expense_breakdown: dict = Field(description="Monthly expense breakdown")
    five_year_projection: str = Field(description="5-year investment projection")
    risks: list[str] = Field(description="Investment risks")
    opportunities: list[str] = Field(description="Value-add opportunities")
    investment_grade: str = Field(description="A/B/C/D investment grade")
    recommendation: str = Field(description="Buy/pass recommendation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Investment Analyzer",
        instructions=[
            "You are an expert real estate investment analyst.",
            f"Analyze {cfg['property_type']} investment properties",
            "Calculate comprehensive ROI metrics",
            "Consider all expenses including vacancy, repairs, management",
            "Project long-term appreciation and equity building",
            "Provide honest assessment of risks and opportunities",
        ],
        output_schema=InvestmentAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Investment Analyzer Agent - Demo")
    print("=" * 60)
    query = f"""Analyze this investment property:
- Purchase Price: ${config['purchase_price']:,}
- Expected Monthly Rent: ${config['monthly_rent']:,}
- Property Type: {config['property_type']}

Provide comprehensive investment analysis."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, InvestmentAnalysis):
        print(f"\n📊 {result.property_summary}")
        m = result.metrics
        print(f"\n💰 Key Metrics:")
        print(f"  • Cap Rate: {m.cap_rate:.1f}%")
        print(f"  • Cash-on-Cash: {m.cash_on_cash_return:.1f}%")
        print(f"  • Monthly Cash Flow: ${m.monthly_cash_flow:,}")
        print(f"  • Annual ROI: {m.annual_roi:.1f}%")
        print(f"\n📈 5-Year Projection: {result.five_year_projection}")
        print(f"\n⭐ Grade: {result.investment_grade}")
        print(f"💡 Recommendation: {result.recommendation}")

def main():
    parser = argparse.ArgumentParser(description="Investment Analyzer Agent")
    parser.add_argument("--price", "-p", type=int, default=DEFAULT_CONFIG["purchase_price"])
    parser.add_argument("--rent", "-r", type=int, default=DEFAULT_CONFIG["monthly_rent"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["property_type"])
    args = parser.parse_args()
    config = {"purchase_price": args.price, "monthly_rent": args.rent, "property_type": args.type}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
