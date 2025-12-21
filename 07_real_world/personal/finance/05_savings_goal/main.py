"""
Example #195: Savings Goal Agent
Category: personal/finance
DESCRIPTION: Creates savings plans for specific goals with timelines and strategies
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"goal_type": "general"}

class SavingsMilestone(BaseModel):
    milestone: str = Field(description="Milestone description")
    target_amount: float = Field(description="Amount to reach")
    target_date: str = Field(description="When to reach it")
    celebration: str = Field(description="How to celebrate")

class SavingsPlan(BaseModel):
    goal_name: str = Field(description="Savings goal name")
    target_amount: float = Field(description="Total goal amount")
    current_savings: float = Field(description="Starting amount")
    monthly_contribution: float = Field(description="Required monthly savings")
    target_date: str = Field(description="Goal completion date")
    milestones: list[SavingsMilestone] = Field(description="Progress milestones")
    savings_strategies: list[str] = Field(description="How to find the money")
    where_to_save: str = Field(description="Recommended account type")
    automation_tips: list[str] = Field(description="How to automate savings")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Savings Goal Planner",
        instructions=[
            f"You create savings plans for {cfg['goal_type']} goals.",
            "Break large goals into achievable milestones.",
            "Suggest realistic monthly savings amounts.",
            "Recommend appropriate savings vehicles.",
            "Provide strategies to find extra money to save.",
        ],
        output_schema=SavingsPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Savings Goal Planner - Demo")
    print("=" * 60)
    query = """Help me save for a vacation:
    Goal: Trip to Japan
    Target amount: $6,000
    Current savings: $500
    Timeline: 12 months
    Monthly income: $4,500
    Current monthly expenses: ~$3,800"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SavingsPlan):
        print(f"\n🎯 Goal: {result.goal_name}")
        print(f"💰 Target: ${result.target_amount:,.0f}")
        print(f"📅 By: {result.target_date}")
        print(f"💵 Monthly Savings Needed: ${result.monthly_contribution:,.0f}")
        print(f"\n🏦 Save In: {result.where_to_save}")
        print(f"\n🎉 Milestones:")
        for m in result.milestones:
            print(f"  • ${m.target_amount:,.0f} by {m.target_date}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal-type", "-g", default=DEFAULT_CONFIG["goal_type"])
    args = parser.parse_args()
    run_demo(get_agent(config={"goal_type": args.goal_type}), {"goal_type": args.goal_type})

if __name__ == "__main__": main()
