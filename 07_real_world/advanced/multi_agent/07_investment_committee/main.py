"""
Example #217: Investment Committee Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Investment analysis team with analysts and risk assessment
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"risk_tolerance": "moderate"}

class InvestmentAnalysis(BaseModel):
    analyst: str = Field(description="Which analyst")
    recommendation: str = Field(description="buy, hold, sell")
    target_price: str = Field(description="Price target if applicable")
    key_factors: list[str] = Field(description="Key decision factors")
    risks: list[str] = Field(description="Identified risks")

class InvestmentDecision(BaseModel):
    asset: str = Field(description="Asset being evaluated")
    committee_decision: str = Field(description="buy, hold, sell, pass")
    confidence: str = Field(description="high, medium, low")
    position_size: str = Field(description="Recommended allocation")
    analyses: list[InvestmentAnalysis] = Field(description="Individual analyses")
    risk_assessment: str = Field(description="Overall risk evaluation")
    entry_strategy: str = Field(description="How to enter position")
    exit_criteria: list[str] = Field(description="When to exit")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_fundamental_analyst(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Fundamental Analyst",
        instructions=[
            "You analyze investments based on fundamentals.",
            "Evaluate financials, competitive position, management.",
            "Determine intrinsic value.",
        ],
        markdown=True,
    )

def get_technical_analyst(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Technical Analyst",
        instructions=[
            "You analyze price patterns and market trends.",
            "Identify entry and exit points.",
            "Assess market sentiment and momentum.",
        ],
        markdown=True,
    )

def get_committee_chair(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Investment Committee Chair",
        instructions=[
            "You synthesize analyst recommendations.",
            "Balance risk and return expectations.",
            "Make final investment decisions.",
            "Define position sizing and exit strategies.",
        ],
        output_schema=InvestmentDecision,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_committee_chair(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Investment Committee - Demo")
    print("=" * 60)
    
    opportunity = """
    Investment Opportunity: TechGrowth Inc.
    Sector: Enterprise SaaS
    Market Cap: $5B
    Revenue Growth: 40% YoY
    Gross Margin: 75%
    Net Retention: 125%
    Current P/S: 15x
    Recent News: New product launch, expanding to Europe"""
    
    fundamental = get_fundamental_analyst()
    technical = get_technical_analyst()
    chair = agent
    
    print(f"\n📈 Evaluating: TechGrowth Inc.")
    
    fund_analysis = fundamental.run(f"Analyze this investment:\n{opportunity}")
    tech_analysis = technical.run(f"Technical analysis for:\n{opportunity}")
    
    decision_prompt = f"""
    Investment Opportunity: {opportunity}
    
    Fundamental Analysis: {fund_analysis.content}
    Technical Analysis: {tech_analysis.content}
    
    Risk Tolerance: {config.get('risk_tolerance', 'moderate')}
    
    Make investment committee decision."""
    
    result = chair.run(decision_prompt)
    
    if isinstance(result.content, InvestmentDecision):
        r = result.content
        dec_emoji = "🟢" if r.committee_decision == "buy" else "🟡" if r.committee_decision == "hold" else "🔴"
        print(f"\n{dec_emoji} Decision: {r.committee_decision.upper()}")
        print(f"📊 Confidence: {r.confidence} | Position: {r.position_size}")
        print(f"\n⚠️ Risk Assessment: {r.risk_assessment}")
        print(f"\n📍 Entry Strategy: {r.entry_strategy}")
        print(f"\n🚪 Exit Criteria:")
        for criteria in r.exit_criteria:
            print(f"  • {criteria}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--risk-tolerance", "-r", default=DEFAULT_CONFIG["risk_tolerance"])
    args = parser.parse_args()
    run_demo(get_agent(), {"risk_tolerance": args.risk_tolerance})

if __name__ == "__main__": main()
