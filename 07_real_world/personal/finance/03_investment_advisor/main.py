"""
Example #193: Investment Advisor Agent
Category: personal/finance
DESCRIPTION: Provides investment guidance based on goals, risk tolerance, and time horizon
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"risk_profile": "moderate"}

class AssetAllocation(BaseModel):
    asset_class: str = Field(description="Asset type")
    percentage: float = Field(description="Portfolio percentage")
    rationale: str = Field(description="Why this allocation")

class InvestmentPlan(BaseModel):
    risk_assessment: str = Field(description="Risk profile summary")
    recommended_allocation: list[AssetAllocation] = Field(description="Target portfolio")
    investment_vehicles: list[str] = Field(description="Suggested account types and funds")
    monthly_contribution: float = Field(description="Suggested monthly investment")
    rebalancing_frequency: str = Field(description="When to rebalance")
    key_principles: list[str] = Field(description="Investment strategy principles")
    warnings: list[str] = Field(description="Important considerations")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Investment Advisor",
        instructions=[
            f"You provide investment guidance for {cfg['risk_profile']} risk profiles.",
            "Consider time horizon, goals, and risk tolerance.",
            "Recommend diversified, low-cost investment strategies.",
            "Explain rationale for allocation decisions.",
            "Include appropriate disclaimers - this is educational, not financial advice.",
        ],
        output_schema=InvestmentPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Investment Advisor - Demo")
    print("=" * 60)
    query = """Help me plan my investments:
    Age: 35
    Goal: Retirement at 65 (30-year horizon)
    Current savings: $50,000 in savings account
    Can invest: $1,000/month
    Risk tolerance: Moderate - can handle some volatility
    Already have: 401k with employer match"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, InvestmentPlan):
        print(f"\n📊 Risk Assessment: {result.risk_assessment}")
        print(f"\n🎯 Recommended Allocation:")
        for alloc in result.recommended_allocation:
            print(f"  {alloc.asset_class}: {alloc.percentage}%")
        print(f"\n💰 Monthly Contribution: ${result.monthly_contribution:,.0f}")
        print(f"🔄 Rebalance: {result.rebalancing_frequency}")
        print(f"\n⚠️ Note: {result.warnings[0] if result.warnings else 'Consult a financial advisor'}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--risk-profile", "-r", default=DEFAULT_CONFIG["risk_profile"])
    args = parser.parse_args()
    run_demo(get_agent(config={"risk_profile": args.risk_profile}), {"risk_profile": args.risk_profile})

if __name__ == "__main__": main()
