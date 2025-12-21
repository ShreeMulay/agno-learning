"""
Example #200: Retirement Planner Agent
Category: personal/finance
DESCRIPTION: Projects retirement savings needs and creates contribution strategies
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"retirement_style": "comfortable"}

class RetirementMilestone(BaseModel):
    age: int = Field(description="Age at milestone")
    target_balance: float = Field(description="Target savings at this age")
    monthly_contribution: float = Field(description="Required monthly contribution")

class RetirementPlan(BaseModel):
    current_age: int = Field(description="Current age")
    retirement_age: int = Field(description="Target retirement age")
    years_to_retirement: int = Field(description="Years until retirement")
    retirement_income_needed: float = Field(description="Annual income needed in retirement")
    total_savings_needed: float = Field(description="Total nest egg required")
    current_savings: float = Field(description="Current retirement savings")
    savings_gap: float = Field(description="Additional savings needed")
    monthly_contribution_needed: float = Field(description="Required monthly savings")
    milestones: list[RetirementMilestone] = Field(description="Progress milestones")
    strategies: list[str] = Field(description="Retirement saving strategies")
    catch_up_options: list[str] = Field(description="Ways to accelerate if behind")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Retirement Planner",
        instructions=[
            f"You plan for a {cfg['retirement_style']} retirement lifestyle.",
            "Use 4% withdrawal rule for sustainability calculations.",
            "Account for inflation and investment growth.",
            "Consider Social Security and other income sources.",
            "Provide realistic projections and actionable steps.",
        ],
        output_schema=RetirementPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Retirement Planner - Demo")
    print("=" * 60)
    query = """Plan my retirement:
    Current age: 35
    Target retirement age: 65
    Current salary: $90,000
    Current retirement savings: $120,000
    Monthly contribution: $800
    Employer match: 4% of salary
    Expected Social Security: ~$2,000/month
    Desired retirement lifestyle: Comfortable, some travel"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, RetirementPlan):
        print(f"\n🎯 Retirement at Age {result.retirement_age} ({result.years_to_retirement} years)")
        print(f"\n💰 Savings Analysis:")
        print(f"  Current: ${result.current_savings:,.0f}")
        print(f"  Needed: ${result.total_savings_needed:,.0f}")
        print(f"  Gap: ${result.savings_gap:,.0f}")
        print(f"\n📈 Monthly Contribution Needed: ${result.monthly_contribution_needed:,.0f}")
        print(f"\n🎉 Milestones:")
        for m in result.milestones:
            print(f"  Age {m.age}: ${m.target_balance:,.0f}")
        print(f"\n💡 Strategies:")
        for s in result.strategies[:3]:
            print(f"  • {s}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--retirement-style", "-r", default=DEFAULT_CONFIG["retirement_style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"retirement_style": args.retirement_style}), {"retirement_style": args.retirement_style})

if __name__ == "__main__": main()
