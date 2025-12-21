"""
Example #199: Financial Health Agent
Category: personal/finance
DESCRIPTION: Assesses overall financial health and provides personalized improvement plans
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"assessment_type": "comprehensive"}

class HealthMetric(BaseModel):
    metric: str = Field(description="Financial metric name")
    current_value: str = Field(description="Current status")
    target_value: str = Field(description="Healthy target")
    score: int = Field(description="Score out of 10")
    improvement_action: str = Field(description="How to improve")

class FinancialHealth(BaseModel):
    overall_score: int = Field(description="Overall health score 1-100")
    grade: str = Field(description="Letter grade A-F")
    metrics: list[HealthMetric] = Field(description="Individual metric scores")
    strengths: list[str] = Field(description="Financial strengths")
    weaknesses: list[str] = Field(description="Areas needing improvement")
    priority_actions: list[str] = Field(description="Top 3 actions to take")
    six_month_goals: list[str] = Field(description="Goals for next 6 months")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Financial Health Assessor",
        instructions=[
            f"You provide {cfg['assessment_type']} financial health assessments.",
            "Evaluate key metrics: emergency fund, debt-to-income, savings rate, etc.",
            "Identify strengths and weaknesses objectively.",
            "Provide actionable improvement recommendations.",
            "Set realistic short-term goals.",
        ],
        output_schema=FinancialHealth,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Financial Health Assessment - Demo")
    print("=" * 60)
    query = """Assess my financial health:
    Income: $6,000/month after tax
    Expenses: $4,800/month
    Emergency fund: $8,000 (goal is 3-6 months)
    Debt: $15,000 credit cards, $25,000 student loans
    Retirement savings: $45,000 (age 32)
    Savings rate: ~20% when no unexpected expenses
    Credit score: 720
    Life insurance: None
    Will/estate plan: None"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, FinancialHealth):
        print(f"\n📊 Financial Health Score: {result.overall_score}/100 (Grade: {result.grade})")
        print(f"\n✅ Strengths:")
        for s in result.strengths:
            print(f"  • {s}")
        print(f"\n⚠️ Needs Improvement:")
        for w in result.weaknesses:
            print(f"  • {w}")
        print(f"\n🎯 Priority Actions:")
        for i, action in enumerate(result.priority_actions, 1):
            print(f"  {i}. {action}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assessment-type", "-a", default=DEFAULT_CONFIG["assessment_type"])
    args = parser.parse_args()
    run_demo(get_agent(config={"assessment_type": args.assessment_type}), {"assessment_type": args.assessment_type})

if __name__ == "__main__": main()
