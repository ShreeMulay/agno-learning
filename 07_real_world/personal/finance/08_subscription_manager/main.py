"""
Example #198: Subscription Manager Agent
Category: personal/finance
DESCRIPTION: Tracks recurring subscriptions and identifies unused or redundant services
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"audit_depth": "standard"}

class Subscription(BaseModel):
    service: str = Field(description="Service name")
    monthly_cost: float = Field(description="Monthly cost")
    annual_cost: float = Field(description="Annual cost")
    category: str = Field(description="entertainment, productivity, health, etc")
    usage_level: str = Field(description="high, medium, low, unused")
    recommendation: str = Field(description="keep, downgrade, cancel, review")

class SubscriptionAudit(BaseModel):
    subscriptions: list[Subscription] = Field(description="All tracked subscriptions")
    monthly_total: float = Field(description="Total monthly spending")
    annual_total: float = Field(description="Total annual spending")
    potential_savings: float = Field(description="Savings if recommendations followed")
    cancel_suggestions: list[str] = Field(description="Services to consider canceling")
    downgrade_suggestions: list[str] = Field(description="Services to downgrade")
    optimization_tips: list[str] = Field(description="General subscription advice")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Subscription Manager",
        instructions=[
            f"You audit subscriptions with {cfg['audit_depth']} depth.",
            "Identify unused or underutilized subscriptions.",
            "Find redundant services with overlapping features.",
            "Calculate potential savings from optimization.",
            "Suggest alternatives or bundle options.",
        ],
        output_schema=SubscriptionAudit,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Subscription Manager - Demo")
    print("=" * 60)
    query = """Audit my subscriptions:
    - Netflix: $15.99/month (watch weekly)
    - Hulu: $12.99/month (rarely use)
    - Disney+: $10.99/month (kids use sometimes)
    - HBO Max: $15.99/month (watched 1 show last month)
    - Spotify: $10.99/month (use daily)
    - Apple Music: $10.99/month (forgot I had this)
    - Amazon Prime: $14.99/month (use for shipping)
    - Gym membership: $49.99/month (went twice last month)
    - Headspace: $12.99/month (used once)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SubscriptionAudit):
        print(f"\n💸 Monthly Total: ${result.monthly_total:,.2f}")
        print(f"📅 Annual Total: ${result.annual_total:,.2f}")
        print(f"💰 Potential Savings: ${result.potential_savings:,.2f}/year")
        print(f"\n❌ Consider Canceling:")
        for sub in result.cancel_suggestions:
            print(f"  • {sub}")
        print(f"\n⬇️ Consider Downgrading:")
        for sub in result.downgrade_suggestions:
            print(f"  • {sub}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-depth", "-a", default=DEFAULT_CONFIG["audit_depth"])
    args = parser.parse_args()
    run_demo(get_agent(config={"audit_depth": args.audit_depth}), {"audit_depth": args.audit_depth})

if __name__ == "__main__": main()
