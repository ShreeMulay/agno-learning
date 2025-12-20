"""
Example #034: Financial Report Generator
Category: business/finance

DESCRIPTION:
Transforms raw financial data into narrative insights and executive summaries.
Generates board-ready reports with key metrics and trend analysis.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "financial_data": """
    FY2024 Annual Results:
    Revenue: $12.5M (up 23% YoY)
    Gross Margin: 68% (up from 62%)
    Operating Expenses: $7.2M
    EBITDA: $2.8M (22% margin)
    Net Income: $1.9M
    Cash: $4.2M
    ARR: $14.1M
    Customer Count: 342 (up from 280)
    Churn: 5.2% annually
    NRR: 118%
    """,
}

class FinancialReport(BaseModel):
    period: str = Field(description="Reporting period")
    headline: str = Field(description="One-line headline")
    key_metrics: dict = Field(description="Key metrics with values")
    performance_summary: str = Field(description="Performance narrative")
    highlights: list[str] = Field(description="Top achievements")
    concerns: list[str] = Field(description="Areas of concern")
    yoy_comparison: dict = Field(description="Year-over-year changes")
    outlook: str = Field(description="Forward-looking statement")
    board_talking_points: list[str] = Field(description="Key points for board")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Financial Report Generator",
        instructions=[
            "You are a CFO-level financial analyst.",
            "Transform data into compelling narratives.",
            "Focus on insights, not just numbers.",
            "Highlight trends and their implications.",
        ],
        output_schema=FinancialReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Financial Report Generator - Demo")
    print("=" * 60)
    data = config.get("financial_data", DEFAULT_CONFIG["financial_data"])
    response = agent.run(f"Generate executive report:\n\n{data}")
    result = response.content
    if isinstance(result, FinancialReport):
        print(f"\n📊 {result.period}")
        print(f"📰 {result.headline}")
        print(f"\n{result.performance_summary}")
        print(f"\n✅ Highlights:")
        for h in result.highlights[:3]:
            print(f"  • {h}")
        if result.concerns:
            print(f"\n⚠️ Concerns:")
            for c in result.concerns[:2]:
                print(f"  • {c}")
        print(f"\n🔮 Outlook: {result.outlook}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Financial Report Generator")
    parser.add_argument("--data", "-d", type=str, default=DEFAULT_CONFIG["financial_data"])
    args = parser.parse_args()
    agent = get_agent()
    run_demo(agent, {"financial_data": args.data})

if __name__ == "__main__":
    main()
