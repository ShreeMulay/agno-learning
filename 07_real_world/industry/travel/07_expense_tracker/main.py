"""
Example #157: Expense Tracker Agent
Category: industry/travel
DESCRIPTION: Tracks and analyzes travel expenses
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"trip_name": "Europe Summer 2024", "budget": 5000, "currency": "USD"}

class ExpenseCategory(BaseModel):
    category: str = Field(description="Expense category")
    amount: float = Field(description="Total amount")
    percentage: float = Field(description="Percentage of total")
    top_expenses: list[str] = Field(description="Largest expenses")

class ExpenseAnalysis(BaseModel):
    trip_name: str = Field(description="Trip name")
    total_spent: float = Field(description="Total spent")
    budget: float = Field(description="Budget")
    remaining: float = Field(description="Remaining budget")
    daily_average: float = Field(description="Daily average spend")
    by_category: list[ExpenseCategory] = Field(description="Breakdown by category")
    overspending_alerts: list[str] = Field(description="Categories over budget")
    savings_opportunities: list[str] = Field(description="Where to save")
    forecast: str = Field(description="Budget forecast")
    currency_notes: str = Field(description="Currency exchange notes")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Expense Tracker",
        instructions=[
            "You are an expert travel expense analyst.",
            f"Track expenses for {cfg['trip_name']} with ${cfg['budget']} budget",
            "Categorize and analyze spending patterns",
            "Identify overspending and savings opportunities",
            "Project budget consumption",
            "Handle multi-currency considerations",
        ],
        output_schema=ExpenseAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Expense Tracker Agent - Demo")
    print("=" * 60)
    sample_expenses = """Expenses so far:
- Flights: $1200
- Hotels (5 nights): $800
- Food: $350
- Activities: $200
- Transport: $150
- Shopping: $180"""
    query = f"""Analyze travel expenses:
- Trip: {config['trip_name']}
- Budget: ${config['budget']}
- Days Elapsed: 7 of 14

{sample_expenses}

Provide analysis and budget forecast."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ExpenseAnalysis):
        print(f"\n📊 {result.trip_name}")
        print(f"💰 Spent: ${result.total_spent:.2f} of ${result.budget:.2f}")
        print(f"📈 Remaining: ${result.remaining:.2f} | Daily Avg: ${result.daily_average:.2f}")
        print(f"\n📋 By Category:")
        for cat in result.by_category[:4]:
            print(f"  • {cat.category}: ${cat.amount:.2f} ({cat.percentage:.1f}%)")
        if result.overspending_alerts:
            print(f"\n⚠️ Alerts: {', '.join(result.overspending_alerts)}")
        print(f"\n🔮 Forecast: {result.forecast}")

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker Agent")
    parser.add_argument("--trip", "-t", default=DEFAULT_CONFIG["trip_name"])
    parser.add_argument("--budget", "-b", type=float, default=DEFAULT_CONFIG["budget"])
    parser.add_argument("--currency", "-c", default=DEFAULT_CONFIG["currency"])
    args = parser.parse_args()
    config = {"trip_name": args.trip, "budget": args.budget, "currency": args.currency}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
