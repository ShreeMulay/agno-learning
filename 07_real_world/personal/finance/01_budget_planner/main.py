"""
Example #191: Budget Planner Agent
Category: personal/finance
DESCRIPTION: Creates and manages personal budgets with spending categories and savings goals
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"income_frequency": "monthly"}

class BudgetCategory(BaseModel):
    category: str = Field(description="Spending category")
    allocated_amount: float = Field(description="Budgeted amount")
    percentage_of_income: float = Field(description="Percent of total income")
    priority: str = Field(description="essential, important, discretionary")

class BudgetPlan(BaseModel):
    total_income: float = Field(description="Total income for period")
    categories: list[BudgetCategory] = Field(description="Budget categories")
    savings_target: float = Field(description="Recommended savings amount")
    emergency_fund_contribution: float = Field(description="Emergency fund allocation")
    budget_rules: list[str] = Field(description="Key budget principles applied")
    adjustments_needed: list[str] = Field(description="Areas to optimize")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Budget Planner",
        instructions=[
            f"You create {cfg['income_frequency']} budget plans.",
            "Apply 50/30/20 or zero-based budgeting principles.",
            "Prioritize essential expenses and savings.",
            "Identify areas for potential savings.",
            "Create realistic, sustainable budgets.",
        ],
        output_schema=BudgetPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Budget Planner - Demo")
    print("=" * 60)
    query = """Create a budget for me:
    Monthly income: $5,000 after tax
    Fixed expenses: Rent $1,500, Car payment $350, Insurance $200
    Current spending: Groceries ~$600, Dining out ~$400, Entertainment ~$300
    Goals: Build emergency fund, save for vacation"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, BudgetPlan):
        print(f"\n💰 Monthly Budget Plan (Income: ${result.total_income:,.0f})")
        print(f"\n📊 Categories:")
        for cat in result.categories:
            print(f"  {cat.category}: ${cat.allocated_amount:,.0f} ({cat.percentage_of_income:.0f}%)")
        print(f"\n💵 Savings Target: ${result.savings_target:,.0f}")
        print(f"🏦 Emergency Fund: ${result.emergency_fund_contribution:,.0f}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--income-frequency", "-f", default=DEFAULT_CONFIG["income_frequency"])
    args = parser.parse_args()
    run_demo(get_agent(config={"income_frequency": args.income_frequency}), {"income_frequency": args.income_frequency})

if __name__ == "__main__": main()
