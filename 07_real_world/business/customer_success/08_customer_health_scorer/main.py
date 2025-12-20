"""
Example #028: Customer Health Scorer
Category: business/customer_success

DESCRIPTION:
Calculates customer health scores based on usage metrics, engagement signals,
and support interactions. Identifies at-risk accounts and recommends
proactive interventions to improve retention.

PATTERNS:
- Structured Output (HealthScoreReport)
- Tools (metric calculations)

ARGUMENTS:
- customer_data (str): Customer metrics. Default: sample
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
    "customer_data": """
    Customer: TechFlow Inc
    Tier: Enterprise
    Contract Value: $120,000/year
    Contract Start: 18 months ago
    Renewal Date: 6 months
    
    Usage Metrics (Last 30 Days):
    - DAU: 45 (down from 62 last month)
    - MAU: 120 (down from 145)
    - Feature Adoption: 6 of 12 core features used
    - API Calls: 50,000 (stable)
    - Data Storage: 80GB (growing)
    
    Engagement Signals:
    - Last Login (Champion): 3 days ago
    - Training Completed: 40%
    - NPS Response: 6 (was 8 last quarter)
    - Community Posts: 0 in last 90 days
    - Webinar Attendance: 0 in last 90 days
    
    Support History:
    - Tickets (30 days): 8 (high)
    - Avg Resolution: 36 hours
    - CSAT: 3.2/5
    - Escalations: 2
    
    Business Context:
    - Champion left company 2 months ago
    - New stakeholder not yet engaged
    - Competitor evaluation rumored
    """,
}


# =============================================================================
# Output Schema
# =============================================================================

class HealthDimension(BaseModel):
    """Individual health dimension score."""
    
    dimension: str = Field(description="Dimension name")
    score: int = Field(ge=0, le=100, description="Score 0-100")
    weight: float = Field(description="Weight in overall score")
    trend: str = Field(description="improving/stable/declining")
    key_indicators: list[str] = Field(description="Key metrics for this dimension")
    concerns: list[str] = Field(description="Areas of concern")


class RiskFactor(BaseModel):
    """Identified risk factor."""
    
    factor: str = Field(description="Risk factor")
    severity: str = Field(description="critical/high/medium/low")
    evidence: str = Field(description="Supporting evidence")
    mitigation: str = Field(description="Recommended mitigation")


class InterventionPlan(BaseModel):
    """Proactive intervention recommendation."""
    
    action: str = Field(description="Action to take")
    owner: str = Field(description="Who should own this")
    timeline: str = Field(description="When to execute")
    expected_impact: str = Field(description="Expected improvement")
    success_criteria: str = Field(description="How to measure success")


class HealthScoreReport(BaseModel):
    """Complete customer health assessment."""
    
    customer: str = Field(description="Customer name")
    tier: str = Field(description="Customer tier")
    overall_score: int = Field(ge=0, le=100, description="Overall health 0-100")
    health_status: str = Field(description="healthy/at_risk/critical")
    churn_probability: int = Field(ge=0, le=100, description="Churn likelihood %")
    dimensions: list[HealthDimension] = Field(description="Dimension breakdown")
    risk_factors: list[RiskFactor] = Field(description="Identified risks")
    positive_signals: list[str] = Field(description="What's going well")
    intervention_plan: list[InterventionPlan] = Field(description="Recommended actions")
    renewal_readiness: str = Field(description="Assessment for renewal")
    expansion_potential: str = Field(description="Upsell/expansion opportunity")
    executive_summary: str = Field(description="Summary for leadership")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Customer Health Scorer agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for health scoring
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Customer Health Scorer",
        instructions=[
            "You are a customer success analyst specializing in health scoring.",
            "Calculate comprehensive health scores to predict retention.",
            "",
            "Health Dimensions (weighted):",
            "1. Product Usage (30%): DAU, MAU, feature adoption, depth",
            "2. Engagement (25%): Training, community, events, NPS",
            "3. Support Experience (20%): Ticket volume, CSAT, resolution",
            "4. Business Fit (15%): Use case success, ROI realization",
            "5. Relationship (10%): Champion strength, stakeholder engagement",
            "",
            "Health Status Thresholds:",
            "- Healthy: Score 70-100, low churn risk",
            "- At Risk: Score 40-69, intervention needed",
            "- Critical: Score 0-39, immediate action required",
            "",
            "Key Risk Indicators:",
            "- Champion change/loss",
            "- Declining usage (>20% drop)",
            "- Multiple escalations",
            "- NPS drop of 2+ points",
            "- Competitor mentions",
            "- Approaching renewal without engagement",
            "",
            "Provide actionable interventions with clear owners and timelines.",
        ],
        output_schema=HealthScoreReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of health scoring."""
    print("\n" + "=" * 60)
    print("  Customer Health Scorer - Demo")
    print("=" * 60)
    
    data = config.get("customer_data", DEFAULT_CONFIG["customer_data"])
    
    query = f"""
    Calculate health score for this customer:
    
    {data}
    
    Analyze all dimensions, identify risks, and recommend interventions.
    """
    
    print("\nCalculating health score...")
    print("-" * 40)
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, HealthScoreReport):
        status_emoji = {"healthy": "🟢", "at_risk": "🟡", "critical": "🔴"}
        
        print(f"\n{'='*50}")
        print(f"HEALTH REPORT: {result.customer}")
        print(f"{'='*50}")
        
        print(f"\n{status_emoji.get(result.health_status, '⚪')} Overall Health: {result.overall_score}/100 ({result.health_status.upper()})")
        print(f"📉 Churn Probability: {result.churn_probability}%")
        print(f"🔄 Renewal Readiness: {result.renewal_readiness}")
        print(f"📈 Expansion Potential: {result.expansion_potential}")
        
        print(f"\n📊 Dimension Breakdown:")
        for dim in result.dimensions:
            trend_icon = "↑" if dim.trend == "improving" else "↓" if dim.trend == "declining" else "→"
            print(f"\n  {dim.dimension}: {dim.score}/100 {trend_icon}")
            print(f"    Weight: {dim.weight*100:.0f}%")
            if dim.concerns:
                print(f"    ⚠️ Concerns: {', '.join(dim.concerns[:2])}")
        
        if result.positive_signals:
            print(f"\n✅ Positive Signals:")
            for signal in result.positive_signals:
                print(f"  • {signal}")
        
        print(f"\n⚠️ Risk Factors:")
        for risk in result.risk_factors:
            icon = "🔴" if risk.severity == "critical" else "🟠" if risk.severity == "high" else "🟡"
            print(f"\n  {icon} {risk.factor} ({risk.severity})")
            print(f"     Evidence: {risk.evidence}")
            print(f"     Mitigation: {risk.mitigation}")
        
        print(f"\n🎯 Intervention Plan:")
        for i, action in enumerate(result.intervention_plan, 1):
            print(f"\n  {i}. {action.action}")
            print(f"     Owner: {action.owner} | Timeline: {action.timeline}")
            print(f"     Expected Impact: {action.expected_impact}")
            print(f"     Success Metric: {action.success_criteria}")
        
        print(f"\n📋 Executive Summary:")
        print(f"  {result.executive_summary}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Customer Health Scorer - Calculate retention health"
    )
    
    parser.add_argument(
        "--data", "-d",
        type=str,
        default=DEFAULT_CONFIG["customer_data"],
        help="Customer data"
    )
    
    args = parser.parse_args()
    
    config = {
        "customer_data": args.data,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
