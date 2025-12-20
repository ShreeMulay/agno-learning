"""
Example #059: Risk Assessment Agent
Category: business/legal

DESCRIPTION:
Evaluates legal risks in business decisions, contracts,
or activities with scoring and mitigation recommendations.

PATTERNS:
- Reasoning (risk analysis)
- Structured Output (RiskAssessment)

ARGUMENTS:
- scenario (str): Business scenario to assess
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "scenario": """
    We're a US-based SaaS company considering:
    
    1. Expanding to EU customers without EU entity
    2. Using customer data to train AI models (per existing ToS)
    3. Open-sourcing our core algorithm under MIT license
    4. Hiring contractors in 5 countries without local entities
    5. Accepting cryptocurrency payments
    
    Current situation:
    - 500 B2B customers, $5M ARR
    - No dedicated legal team (use outside counsel)
    - SOC 2 Type 1 certified
    - Standard clickwrap agreements
    """,
}


class RiskItem(BaseModel):
    risk: str = Field(description="The risk identified")
    category: str = Field(description="regulatory/contractual/IP/employment/financial")
    likelihood: str = Field(description="high/medium/low")
    impact: str = Field(description="severe/moderate/minor")
    risk_score: int = Field(ge=1, le=10, description="Overall risk 1-10")
    mitigation: str = Field(description="How to reduce risk")
    cost_to_mitigate: str = Field(description="Estimated cost/effort")


class RiskAssessment(BaseModel):
    scenario_summary: str = Field(description="Brief scenario description")
    overall_risk_level: str = Field(description="high/medium/low")
    overall_risk_score: int = Field(ge=1, le=100, description="Combined score")
    risks_identified: list[RiskItem] = Field(description="Individual risks")
    highest_priority_risks: list[str] = Field(description="Top 3 to address")
    recommended_actions: list[str] = Field(description="Prioritized steps")
    estimated_legal_budget: str = Field(description="Suggested legal spend")
    timeline_recommendation: str = Field(description="When to act")
    executive_summary: str = Field(description="Summary for leadership")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Risk Assessment Agent",
        instructions=[
            "You are a legal risk analyst for technology companies.",
            "Identify and quantify legal risks in business decisions.",
            "",
            "Risk Categories:",
            "- Regulatory: Compliance, privacy, industry-specific",
            "- Contractual: Customer agreements, vendor contracts",
            "- IP: Patents, trade secrets, open source",
            "- Employment: Hiring, classification, international",
            "- Financial: Payments, taxes, securities",
            "",
            "Scoring:",
            "- Likelihood × Impact = Risk Score",
            "- Consider both probability and severity",
            "- Factor in company stage and resources",
        ],
        output_schema=RiskAssessment,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Risk Assessment Agent - Demo")
    print("=" * 60)
    
    scenario = config.get("scenario", DEFAULT_CONFIG["scenario"])
    
    response = agent.run(f"Assess legal risks:\n\n{scenario}")
    result = response.content
    
    if isinstance(result, RiskAssessment):
        level_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        print(f"\n{level_icon.get(result.overall_risk_level, '?')} Overall Risk: {result.overall_risk_level.upper()}")
        print(f"📊 Risk Score: {result.overall_risk_score}/100")
        
        print(f"\n🔍 Risks Identified ({len(result.risks_identified)}):")
        for r in result.risks_identified:
            print(f"\n   [{r.risk_score}/10] {r.risk}")
            print(f"   Category: {r.category} | Likelihood: {r.likelihood} | Impact: {r.impact}")
            print(f"   Mitigation: {r.mitigation}")
        
        print(f"\n🚨 Highest Priority:")
        for p in result.highest_priority_risks:
            print(f"   • {p}")
        
        print(f"\n✅ Recommended Actions:")
        for i, a in enumerate(result.recommended_actions, 1):
            print(f"   {i}. {a}")
        
        print(f"\n💰 Suggested Legal Budget: {result.estimated_legal_budget}")
        print(f"⏱️ Timeline: {result.timeline_recommendation}")
        print(f"\n📝 {result.executive_summary}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Risk Assessment Agent")
    parser.add_argument("--scenario", "-s", type=str, default=DEFAULT_CONFIG["scenario"])
    args = parser.parse_args()
    agent = get_agent(config={"scenario": args.scenario})
    run_demo(agent, {"scenario": args.scenario})


if __name__ == "__main__":
    main()
