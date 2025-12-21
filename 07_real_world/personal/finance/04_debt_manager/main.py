"""
Example #194: Debt Manager Agent
Category: personal/finance
DESCRIPTION: Creates debt payoff strategies using avalanche, snowball, or hybrid methods
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"strategy": "avalanche"}

class DebtAccount(BaseModel):
    name: str = Field(description="Debt account name")
    balance: float = Field(description="Current balance")
    interest_rate: float = Field(description="APR")
    minimum_payment: float = Field(description="Minimum monthly payment")
    payoff_order: int = Field(description="Order to pay off")
    payoff_date: str = Field(description="Estimated payoff date")

class DebtPlan(BaseModel):
    total_debt: float = Field(description="Total debt amount")
    accounts: list[DebtAccount] = Field(description="Debts in payoff order")
    monthly_budget: float = Field(description="Total monthly debt payment")
    extra_payment_target: str = Field(description="Where extra payments go")
    total_interest_saved: float = Field(description="Interest saved vs minimum payments")
    debt_free_date: str = Field(description="Projected debt-free date")
    motivation_tips: list[str] = Field(description="Stay motivated suggestions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Debt Manager",
        instructions=[
            f"You create debt payoff plans using the {cfg['strategy']} method.",
            "Avalanche: highest interest first (saves most money).",
            "Snowball: smallest balance first (psychological wins).",
            "Calculate payoff timelines and interest savings.",
            "Provide motivation and practical tips.",
        ],
        output_schema=DebtPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Debt Manager - Demo")
    print("=" * 60)
    query = """Help me pay off my debts:
    1. Credit Card A: $5,000 balance, 22% APR, $150 minimum
    2. Credit Card B: $2,500 balance, 18% APR, $75 minimum
    3. Car Loan: $12,000 balance, 6% APR, $350 minimum
    4. Student Loan: $25,000 balance, 5% APR, $280 minimum
    I can afford $1,000/month total for debt payments."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DebtPlan):
        print(f"\n💳 Total Debt: ${result.total_debt:,.0f}")
        print(f"\n📋 Payoff Order ({config.get('strategy', 'avalanche').title()} Method):")
        for debt in result.accounts:
            print(f"  {debt.payoff_order}. {debt.name}: ${debt.balance:,.0f} @ {debt.interest_rate}%")
        print(f"\n🎯 Debt-Free Date: {result.debt_free_date}")
        print(f"💰 Interest Saved: ${result.total_interest_saved:,.0f}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", "-s", default=DEFAULT_CONFIG["strategy"])
    args = parser.parse_args()
    run_demo(get_agent(config={"strategy": args.strategy}), {"strategy": args.strategy})

if __name__ == "__main__": main()
