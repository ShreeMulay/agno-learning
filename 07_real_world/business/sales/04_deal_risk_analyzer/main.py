"""
Example #004: Deal Risk Analyzer
Category: business/sales

DESCRIPTION:
Analyzes sales deals to predict closure probability and identify risks.
Uses deal context (stage, engagement, competition) to score risk and
suggest mitigation strategies.

PATTERNS:
- Structured Output (DealRiskAssessment)
- Knowledge (optional: historical deal data)

ARGUMENTS:
- deal_name (str): Deal/opportunity name. Default: "Enterprise SaaS Deal"
- deal_value (int): Deal value in USD. Default: 100000
- stage (str): Current pipeline stage. Default: "negotiation"
- days_in_stage (int): Days stuck in current stage. Default: 14
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "deal_name": "Enterprise SaaS Deal",
    "deal_value": 100000,
    "stage": "negotiation",
    "days_in_stage": 14,
    "competitor": "",
    "last_contact_days": 7,
    "champion_status": "active",
}


# =============================================================================
# Output Schema
# =============================================================================

class RiskFactor(BaseModel):
    """Individual risk factor."""
    factor: str = Field(description="The risk factor")
    severity: str = Field(description="low/medium/high/critical")
    mitigation: str = Field(description="How to address this risk")


class DealRiskAssessment(BaseModel):
    """Complete deal risk analysis."""
    
    deal_name: str = Field(description="Deal identifier")
    closure_probability: int = Field(ge=0, le=100, description="Likelihood to close 0-100%")
    risk_score: int = Field(ge=0, le=100, description="Overall risk score 0-100")
    risk_level: str = Field(description="low/medium/high/critical")
    
    risk_factors: list[RiskFactor] = Field(description="Identified risks")
    positive_signals: list[str] = Field(description="Positive indicators")
    
    recommended_actions: list[str] = Field(description="Priority actions to take")
    forecast_change: str = Field(description="commit/upside/pipeline/at_risk")
    next_milestone: str = Field(description="Next critical milestone")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Create the Deal Risk Analyzer agent."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Deal Risk Analyzer",
        instructions=[
            "You are a sales operations analyst who predicts deal outcomes.",
            "",
            "Risk Assessment Framework:",
            "- Stage velocity: How long deals typically stay in each stage",
            "- Champion engagement: Is the internal champion active?",
            "- Competitive pressure: Known competitors in the deal",
            "- Budget cycle: Alignment with buyer's fiscal calendar",
            "- Decision maker access: Direct line to economic buyer",
            "",
            "Risk Scoring:",
            "- 0-25: Low risk, high confidence close",
            "- 26-50: Medium risk, needs attention",
            "- 51-75: High risk, requires intervention",
            "- 76-100: Critical, deal may be lost",
            "",
            "Provide actionable recommendations for each risk identified.",
        ],
        output_schema=DealRiskAssessment,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run deal risk analysis demo."""
    print("\n" + "=" * 60)
    print("  Deal Risk Analyzer - Demo")
    print("=" * 60)
    
    query = f"""
    Analyze this deal:
    - Deal: {config['deal_name']}
    - Value: ${config['deal_value']:,}
    - Stage: {config['stage']}
    - Days in stage: {config['days_in_stage']}
    - Last contact: {config['last_contact_days']} days ago
    - Champion: {config['champion_status']}
    - Competitor: {config.get('competitor') or 'Unknown'}
    """
    
    print(f"\nAnalyzing: {config['deal_name']}")
    print(f"Value: ${config['deal_value']:,}")
    print("-" * 40)
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, DealRiskAssessment):
        # Risk indicator
        risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(result.risk_level, "⚪")
        
        print(f"\n{'='*50}")
        print(f"  {risk_emoji} RISK LEVEL: {result.risk_level.upper()}")
        print(f"  Closure Probability: {result.closure_probability}%")
        print(f"  Risk Score: {result.risk_score}/100")
        print(f"  Forecast: {result.forecast_change.upper()}")
        print(f"{'='*50}")
        
        print(f"\n⚠️  Risk Factors:")
        for risk in result.risk_factors:
            sev_emoji = {"low": "🔵", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(risk.severity, "⚪")
            print(f"  {sev_emoji} {risk.factor}")
            print(f"     → {risk.mitigation}")
        
        print(f"\n✅ Positive Signals:")
        for signal in result.positive_signals:
            print(f"  • {signal}")
        
        print(f"\n📋 Recommended Actions:")
        for i, action in enumerate(result.recommended_actions, 1):
            print(f"  {i}. {action}")
        
        print(f"\n🎯 Next Milestone: {result.next_milestone}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    parser = argparse.ArgumentParser(description="Deal Risk Analyzer")
    parser.add_argument("--deal", type=str, default=DEFAULT_CONFIG["deal_name"])
    parser.add_argument("--value", type=int, default=DEFAULT_CONFIG["deal_value"])
    parser.add_argument("--stage", type=str, default=DEFAULT_CONFIG["stage"],
                        choices=["prospecting", "qualification", "demo", "proposal", "negotiation", "closed"])
    parser.add_argument("--days", type=int, default=DEFAULT_CONFIG["days_in_stage"])
    parser.add_argument("--competitor", type=str, default="")
    args = parser.parse_args()
    
    config = {
        **DEFAULT_CONFIG,
        "deal_name": args.deal,
        "deal_value": args.value,
        "stage": args.stage,
        "days_in_stage": args.days,
        "competitor": args.competitor,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
