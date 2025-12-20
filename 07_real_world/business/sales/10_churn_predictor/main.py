"""
Example #010: Churn Predictor
Category: business/sales

DESCRIPTION:
Analyzes customer usage patterns, support tickets, and engagement signals
to predict churn risk and recommend retention strategies.

PATTERNS:
- Structured Output (ChurnAnalysis schema)
- Knowledge (customer health metrics)

ARGUMENTS:
- customer_name (str): Customer to analyze. Default: "Acme Corp"
- arr (int): Annual recurring revenue. Default: 50000
- months_active (int): Months as customer. Default: 18
- nps_score (int): NPS score 0-10. Default: 6
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "customer_name": "Acme Corp",
    "arr": 50000,
    "months_active": 18,
    "nps_score": 6,
    "usage_trend": "declining",
    "support_tickets_30d": 5,
    "last_login_days": 14,
    "champion_status": "left_company",
}


class ChurnSignal(BaseModel):
    """Individual churn signal."""
    signal: str = Field(description="What we observed")
    severity: str = Field(description="low/medium/high/critical")
    weight: float = Field(description="Impact on churn score 0-1")


class RetentionAction(BaseModel):
    """Recommended retention action."""
    action: str = Field(description="What to do")
    owner: str = Field(description="csm/sales/product/exec")
    urgency: str = Field(description="immediate/this_week/this_month")
    expected_impact: str = Field(description="How this helps")


class ChurnAnalysis(BaseModel):
    """Complete churn prediction analysis."""
    
    customer_name: str = Field(description="Customer name")
    arr_at_risk: int = Field(description="ARR at risk")
    
    # Risk scoring
    churn_probability: int = Field(ge=0, le=100, description="Churn likelihood %")
    risk_tier: str = Field(description="low/medium/high/critical")
    predicted_churn_window: str = Field(description="When churn likely to occur")
    
    # Signals
    churn_signals: list[ChurnSignal] = Field(description="Risk indicators")
    health_signals: list[str] = Field(description="Positive indicators")
    
    # Analysis
    root_cause: str = Field(description="Primary driver of risk")
    similar_churned_customers: list[str] = Field(description="Similar customers who churned")
    
    # Recommendations
    retention_actions: list[RetentionAction] = Field(description="Recommended actions")
    save_probability: int = Field(ge=0, le=100, description="Likelihood of saving")
    
    executive_summary: str = Field(description="Summary for leadership")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Create the Churn Predictor agent."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Churn Predictor",
        instructions=[
            "You are a customer success analyst who predicts and prevents churn.",
            "",
            "Customer Health Signals:",
            f"- Usage Trend: {cfg['usage_trend']}",
            f"- NPS Score: {cfg['nps_score']}/10",
            f"- Support Tickets (30d): {cfg['support_tickets_30d']}",
            f"- Last Login: {cfg['last_login_days']} days ago",
            f"- Champion Status: {cfg['champion_status']}",
            "",
            "Churn Risk Framework:",
            "- 0-25%: Low risk, monitor",
            "- 26-50%: Medium risk, proactive outreach",
            "- 51-75%: High risk, immediate intervention",
            "- 76-100%: Critical, executive escalation",
            "",
            "Provide specific, actionable retention recommendations.",
        ],
        output_schema=ChurnAnalysis,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    """Analyze churn risk demo."""
    print("\n" + "=" * 60)
    print("  Churn Predictor - Demo")
    print("=" * 60)
    
    query = f"""
    Analyze churn risk for:
    - Customer: {config['customer_name']}
    - ARR: ${config['arr']:,}
    - Tenure: {config['months_active']} months
    - NPS: {config['nps_score']}/10
    
    Current signals:
    - Usage: {config['usage_trend']}
    - Support tickets (30d): {config['support_tickets_30d']}
    - Last login: {config['last_login_days']} days ago
    - Champion: {config['champion_status']}
    """
    
    print(f"\nAnalyzing: {config['customer_name']}...")
    print("-" * 40)
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, ChurnAnalysis):
        risk_emoji = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(result.risk_tier, "⚪")
        
        print(f"\n{'='*60}")
        print(f"  {risk_emoji} CHURN RISK: {result.risk_tier.upper()}")
        print(f"  {result.customer_name} | ${result.arr_at_risk:,} ARR at risk")
        print(f"{'='*60}")
        
        print(f"\n📊 RISK ASSESSMENT")
        print(f"  Churn Probability: {result.churn_probability}%")
        print(f"  Predicted Window: {result.predicted_churn_window}")
        print(f"  Save Probability: {result.save_probability}%")
        
        print(f"\n🚨 CHURN SIGNALS")
        for s in result.churn_signals:
            sev_emoji = {"low": "🔵", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(s.severity, "⚪")
            print(f"  {sev_emoji} {s.signal} (weight: {s.weight:.1f})")
        
        if result.health_signals:
            print(f"\n✅ POSITIVE SIGNALS")
            for h in result.health_signals:
                print(f"  • {h}")
        
        print(f"\n🔍 ROOT CAUSE\n  {result.root_cause}")
        
        print(f"\n🛡️ RETENTION ACTIONS")
        for a in result.retention_actions:
            urg_emoji = {"immediate": "🔴", "this_week": "🟠", "this_month": "🟡"}.get(a.urgency, "🔵")
            print(f"  {urg_emoji} [{a.owner.upper()}] {a.action}")
            print(f"     Impact: {a.expected_impact}")
        
        print(f"\n📋 EXECUTIVE SUMMARY\n{result.executive_summary}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    parser = argparse.ArgumentParser(description="Churn Predictor")
    parser.add_argument("--customer", type=str, default=DEFAULT_CONFIG["customer_name"])
    parser.add_argument("--arr", type=int, default=DEFAULT_CONFIG["arr"])
    parser.add_argument("--nps", type=int, default=DEFAULT_CONFIG["nps_score"])
    args = parser.parse_args()
    
    config = {**DEFAULT_CONFIG, "customer_name": args.customer, "arr": args.arr, "nps_score": args.nps}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
