"""
Example #197: Net Worth Tracker Agent
Category: personal/finance
DESCRIPTION: Calculates and tracks net worth with assets, liabilities, and growth analysis
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"tracking_period": "monthly"}

class Asset(BaseModel):
    name: str = Field(description="Asset name")
    category: str = Field(description="cash, investments, property, other")
    value: float = Field(description="Current value")
    liquidity: str = Field(description="high, medium, low")

class Liability(BaseModel):
    name: str = Field(description="Liability name")
    balance: float = Field(description="Amount owed")
    interest_rate: float = Field(description="Interest rate if applicable")

class NetWorthAnalysis(BaseModel):
    total_assets: float = Field(description="Sum of all assets")
    total_liabilities: float = Field(description="Sum of all debts")
    net_worth: float = Field(description="Assets minus liabilities")
    assets: list[Asset] = Field(description="Asset breakdown")
    liabilities: list[Liability] = Field(description="Liability breakdown")
    liquid_net_worth: float = Field(description="Easily accessible net worth")
    growth_rate: str = Field(description="Net worth change vs last period")
    wealth_building_tips: list[str] = Field(description="How to grow net worth")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Net Worth Tracker",
        instructions=[
            f"You track net worth on a {cfg['tracking_period']} basis.",
            "Categorize assets by type and liquidity.",
            "Track all liabilities accurately.",
            "Calculate liquid vs total net worth.",
            "Provide actionable wealth-building advice.",
        ],
        output_schema=NetWorthAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Net Worth Tracker - Demo")
    print("=" * 60)
    query = """Calculate my net worth:
    Assets:
    - Checking account: $5,000
    - Savings account: $15,000
    - 401k: $85,000
    - Roth IRA: $25,000
    - Car value: $18,000
    - Home value: $350,000
    
    Liabilities:
    - Mortgage: $280,000 @ 4%
    - Car loan: $12,000 @ 5%
    - Credit card: $2,500 @ 20%"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, NetWorthAnalysis):
        print(f"\n📈 Net Worth Summary")
        print(f"  Assets: ${result.total_assets:,.0f}")
        print(f"  Liabilities: ${result.total_liabilities:,.0f}")
        print(f"  ─────────────────")
        print(f"  Net Worth: ${result.net_worth:,.0f}")
        print(f"\n💧 Liquid Net Worth: ${result.liquid_net_worth:,.0f}")
        print(f"📊 Growth: {result.growth_rate}")
        print(f"\n💡 Wealth Building Tips:")
        for tip in result.wealth_building_tips[:3]:
            print(f"  • {tip}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracking-period", "-t", default=DEFAULT_CONFIG["tracking_period"])
    args = parser.parse_args()
    run_demo(get_agent(config={"tracking_period": args.tracking_period}), {"tracking_period": args.tracking_period})

if __name__ == "__main__": main()
