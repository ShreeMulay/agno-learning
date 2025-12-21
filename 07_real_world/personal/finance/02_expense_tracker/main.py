"""
Example #192: Expense Tracker Agent
Category: personal/finance
DESCRIPTION: Categorizes and analyzes spending patterns to identify savings opportunities
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"period": "monthly"}

class ExpenseCategory(BaseModel):
    category: str = Field(description="Expense category")
    total_spent: float = Field(description="Total amount spent")
    transaction_count: int = Field(description="Number of transactions")
    average_transaction: float = Field(description="Average per transaction")
    trend: str = Field(description="up, down, stable vs last period")

class ExpenseAnalysis(BaseModel):
    total_spending: float = Field(description="Total spent in period")
    categories: list[ExpenseCategory] = Field(description="Spending by category")
    top_merchants: list[str] = Field(description="Top spending locations")
    unusual_expenses: list[str] = Field(description="One-time or unusual charges")
    savings_opportunities: list[str] = Field(description="Where to cut back")
    spending_insights: list[str] = Field(description="Key patterns identified")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Expense Tracker",
        instructions=[
            f"You analyze {cfg['period']} expenses and spending patterns.",
            "Categorize transactions accurately.",
            "Identify trends and unusual spending.",
            "Find actionable savings opportunities.",
            "Provide non-judgmental insights.",
        ],
        output_schema=ExpenseAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Expense Tracker - Demo")
    print("=" * 60)
    query = """Analyze my recent expenses:
    - Amazon: $450 (various purchases)
    - Grocery Store: $580 (weekly shopping)
    - Gas Station: $180
    - Netflix/Spotify/HBO: $45
    - Coffee shops: $120
    - Restaurant: $320
    - Uber: $85
    - Pharmacy: $60
    - Online courses: $200 (annual subscription renewed)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ExpenseAnalysis):
        print(f"\n💸 Total Spending: ${result.total_spending:,.0f}")
        print(f"\n📊 By Category:")
        for cat in result.categories[:5]:
            trend_emoji = "📈" if cat.trend == "up" else "📉" if cat.trend == "down" else "➡️"
            print(f"  {cat.category}: ${cat.total_spent:,.0f} {trend_emoji}")
        print(f"\n💡 Savings Opportunities:")
        for opp in result.savings_opportunities:
            print(f"  • {opp}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--period", "-p", default=DEFAULT_CONFIG["period"])
    args = parser.parse_args()
    run_demo(get_agent(config={"period": args.period}), {"period": args.period})

if __name__ == "__main__": main()
