"""
Example #040: Financial Modeling Assistant
Category: business/finance

DESCRIPTION:
Helps build financial models with scenario analysis and sensitivity testing.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "model_inputs": """
    3-Year Revenue Projection Model:
    Base Year Revenue: $10M
    Growth Rate: 20% (base case)
    Gross Margin: 65%
    OpEx as % Revenue: 45%
    
    Scenarios to model:
    - Bear: 10% growth
    - Base: 20% growth
    - Bull: 35% growth
    
    Sensitivity: How does 5% margin change impact profitability?
    """,
}

class Scenario(BaseModel):
    name: str = Field(description="Scenario name")
    year1_revenue: float = Field(description="Year 1 revenue")
    year2_revenue: float = Field(description="Year 2 revenue")
    year3_revenue: float = Field(description="Year 3 revenue")
    year3_profit: float = Field(description="Year 3 net income")
    irr: Optional[float] = Field(default=None, description="IRR if applicable")

class SensitivityResult(BaseModel):
    variable: str = Field(description="Variable tested")
    base_value: str = Field(description="Base assumption")
    test_value: str = Field(description="Test value")
    impact: str = Field(description="Impact on outcome")

class FinancialModel(BaseModel):
    model_name: str = Field(description="Model description")
    assumptions: dict = Field(description="Key assumptions")
    scenarios: list[Scenario] = Field(description="Scenario outputs")
    sensitivities: list[SensitivityResult] = Field(description="Sensitivity tests")
    key_insights: list[str] = Field(description="Model insights")
    risks: list[str] = Field(description="Key risks")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Financial Modeling Assistant",
        instructions=[
            "You are a financial modeling expert.",
            "Build scenario-based projections.",
            "Perform sensitivity analysis.",
            "Highlight key assumptions and risks.",
        ],
        output_schema=FinancialModel,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Financial Modeling Assistant - Demo")
    print("=" * 60)
    data = config.get("model_inputs", DEFAULT_CONFIG["model_inputs"])
    response = agent.run(f"Build financial model:\n\n{data}")
    result = response.content
    if isinstance(result, FinancialModel):
        print(f"\n📊 {result.model_name}")
        print(f"\n📈 Scenario Analysis:")
        for s in result.scenarios:
            print(f"  {s.name}: Y1 ${s.year1_revenue:,.0f} → Y3 ${s.year3_revenue:,.0f}")
            print(f"    Y3 Profit: ${s.year3_profit:,.0f}")
        print(f"\n🔬 Sensitivities:")
        for sens in result.sensitivities[:2]:
            print(f"  • {sens.variable}: {sens.base_value} → {sens.test_value}")
            print(f"    Impact: {sens.impact}")
        print(f"\n💡 Insights:")
        for i in result.key_insights[:3]:
            print(f"  • {i}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Financial Modeling Assistant")
    parser.add_argument("--inputs", "-i", type=str, default=DEFAULT_CONFIG["model_inputs"])
    args = parser.parse_args()
    agent = get_agent()
    run_demo(agent, {"model_inputs": args.inputs})

if __name__ == "__main__":
    main()
