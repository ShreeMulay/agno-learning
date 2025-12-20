"""
Example #039: Currency Risk Monitor
Category: business/finance

DESCRIPTION:
Monitors FX exposure, tracks currency movements, and recommends hedging strategies.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "exposure_data": """
    Currency Exposures:
    - EUR: $2.5M receivables (due Q1), Rate: 1.08
    - GBP: $1.2M payables (due Q1), Rate: 1.26
    - JPY: $800K receivables (due Q2), Rate: 0.0067
    
    Current Hedges:
    - EUR forward: $1M at 1.10 (expires Jan 15)
    
    Recent Volatility: EUR +2%, GBP -3%, JPY +1%
    """,
}

class CurrencyExposure(BaseModel):
    currency: str = Field(description="Currency code")
    amount_usd: float = Field(description="USD equivalent")
    direction: str = Field(description="receivable/payable")
    due_date: str = Field(description="When due")
    hedged_pct: float = Field(description="Percentage hedged")
    risk_level: str = Field(description="low/medium/high")

class FXReport(BaseModel):
    total_exposure: float = Field(description="Total FX exposure")
    net_exposure: float = Field(description="Net after hedges")
    exposures: list[CurrencyExposure] = Field(description="By currency")
    risk_assessment: str = Field(description="Overall FX risk")
    hedging_recommendations: list[str] = Field(description="Hedge suggestions")
    estimated_var: str = Field(description="Value at Risk estimate")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Currency Risk Monitor",
        instructions=[
            "You are an FX risk management specialist.",
            "Analyze currency exposures and recommend hedges.",
            "Consider both natural hedges and derivatives.",
        ],
        output_schema=FXReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Currency Risk Monitor - Demo")
    print("=" * 60)
    data = config.get("exposure_data", DEFAULT_CONFIG["exposure_data"])
    response = agent.run(f"Analyze FX risk:\n\n{data}")
    result = response.content
    if isinstance(result, FXReport):
        print(f"\n💱 FX Risk Report")
        print(f"Total Exposure: ${result.total_exposure:,.0f}")
        print(f"Net (after hedges): ${result.net_exposure:,.0f}")
        print(f"VaR: {result.estimated_var}")
        print(f"\n📊 By Currency:")
        for exp in result.exposures:
            print(f"  {exp.currency}: ${exp.amount_usd:,.0f} ({exp.direction})")
            print(f"    Hedged: {exp.hedged_pct}% | Risk: {exp.risk_level}")
        print(f"\n💡 Recommendations:")
        for rec in result.hedging_recommendations[:3]:
            print(f"  • {rec}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Currency Risk Monitor")
    parser.add_argument("--data", "-d", type=str, default=DEFAULT_CONFIG["exposure_data"])
    args = parser.parse_args()
    agent = get_agent()
    run_demo(agent, {"exposure_data": args.data})

if __name__ == "__main__":
    main()
