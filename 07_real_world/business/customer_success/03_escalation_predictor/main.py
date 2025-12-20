"""
Example #023: Escalation Predictor
Category: business/customer_success

DESCRIPTION:
Predicts which support tickets are likely to escalate based on sentiment,
history, and issue complexity. Flags high-risk tickets for proactive
intervention before customer frustration peaks.

PATTERNS:
- Knowledge (escalation patterns)
- Structured Output (EscalationPrediction with risk factors)

ARGUMENTS:
- ticket_data (str): Ticket information. Default: sample
- customer_history (str): Customer interaction history. Default: sample
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
    "ticket_data": """
    Ticket ID: TKT-5892
    Subject: STILL waiting for resolution - 3rd follow-up
    Created: 5 days ago
    Last Update: 2 days ago
    
    Message:
    This is absolutely unacceptable. I've been waiting for 5 days now and 
    nobody seems to care about my issue. Your system deleted all my project 
    files and I've lost weeks of work. I've already escalated this twice 
    and keep getting generic responses.
    
    If this isn't resolved TODAY, I'm canceling our enterprise contract 
    and moving to your competitor. I've already been in touch with their 
    sales team.
    
    This is my FINAL warning.
    """,
    "customer_history": """
    Customer: Enterprise tier, 3 year customer
    Contract Value: $150,000/year
    Previous Tickets: 12 (10 resolved, 2 escalated)
    Average Satisfaction: 3.2/5 (declining trend)
    Last CSAT: 1/5 (2 weeks ago)
    Renewal Date: 45 days
    Champion Status: At-risk (was Advocate)
    """,
}


# =============================================================================
# Output Schema
# =============================================================================

class RiskFactor(BaseModel):
    """Individual risk factor."""
    
    factor: str = Field(description="Risk factor name")
    severity: str = Field(description="critical/high/medium/low")
    evidence: str = Field(description="Evidence from ticket/history")
    weight: float = Field(description="Weight in overall score")


class SentimentAnalysis(BaseModel):
    """Detailed sentiment breakdown."""
    
    overall: str = Field(description="positive/neutral/negative/hostile")
    frustration_level: int = Field(ge=1, le=10, description="Frustration 1-10")
    urgency_expressed: int = Field(ge=1, le=10, description="Urgency 1-10")
    churn_signals: list[str] = Field(description="Explicit churn indicators")
    emotional_triggers: list[str] = Field(description="Emotional language used")


class EscalationPrediction(BaseModel):
    """Complete escalation prediction."""
    
    ticket_id: str = Field(description="Ticket reference")
    escalation_probability: int = Field(ge=0, le=100, description="Escalation likelihood %")
    risk_level: str = Field(description="critical/high/medium/low")
    sentiment: SentimentAnalysis = Field(description="Sentiment analysis")
    risk_factors: list[RiskFactor] = Field(description="Contributing risk factors")
    time_to_escalation: str = Field(description="Estimated time until escalation")
    churn_risk: int = Field(ge=0, le=100, description="Churn probability %")
    revenue_at_risk: str = Field(description="Potential revenue impact")
    recommended_actions: list[str] = Field(description="Immediate actions to take")
    owner_recommendation: str = Field(description="Who should handle this")
    talking_points: list[str] = Field(description="Key points for customer call")
    resolution_path: str = Field(description="Suggested resolution approach")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Escalation Predictor agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for escalation prediction
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Escalation Predictor",
        instructions=[
            "You are an expert at predicting support ticket escalations.",
            "Analyze tickets and customer history to identify escalation risk.",
            "",
            "Key Escalation Indicators:",
            "- Multiple follow-ups without resolution",
            "- Escalating language (CAPS, threats, ultimatums)",
            "- Competitor mentions",
            "- Contract/cancellation references",
            "- Declining satisfaction trend",
            "- High-value customer at risk",
            "- Approaching renewal date",
            "",
            "Risk Severity Levels:",
            "- CRITICAL: Immediate exec intervention needed",
            "- HIGH: Same-day senior response required",
            "- MEDIUM: Priority handling within 24h",
            "- LOW: Standard process sufficient",
            "",
            "Churn Signals:",
            "- Direct cancellation threats",
            "- Competitor evaluation mentions",
            "- Contract review requests",
            "- Reduced usage patterns",
            "- Multiple recent negative interactions",
            "",
            "Be thorough but actionable in recommendations.",
        ],
        output_schema=EscalationPrediction,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of escalation prediction."""
    print("\n" + "=" * 60)
    print("  Escalation Predictor - Demo")
    print("=" * 60)
    
    ticket = config.get("ticket_data", DEFAULT_CONFIG["ticket_data"])
    history = config.get("customer_history", DEFAULT_CONFIG["customer_history"])
    
    query = f"""
    Predict escalation risk for this ticket:
    
    TICKET DATA:
    {ticket}
    
    CUSTOMER HISTORY:
    {history}
    
    Analyze the escalation probability, identify risk factors,
    and provide recommendations for de-escalation.
    """
    
    print("\nAnalyzing ticket for escalation risk...")
    print("-" * 40)
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, EscalationPrediction):
        risk_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        
        print(f"\n{'='*50}")
        print(f"ESCALATION ANALYSIS: {result.ticket_id}")
        print(f"{'='*50}")
        
        print(f"\n{risk_emoji.get(result.risk_level, '⚪')} RISK LEVEL: {result.risk_level.upper()}")
        print(f"📊 Escalation Probability: {result.escalation_probability}%")
        print(f"⏰ Time to Escalation: {result.time_to_escalation}")
        print(f"💰 Churn Risk: {result.churn_risk}% | Revenue at Risk: {result.revenue_at_risk}")
        
        s = result.sentiment
        print(f"\n😤 Sentiment Analysis:")
        print(f"  Overall: {s.overall} | Frustration: {s.frustration_level}/10 | Urgency: {s.urgency_expressed}/10")
        if s.churn_signals:
            print(f"  ⚠️ Churn Signals: {', '.join(s.churn_signals)}")
        if s.emotional_triggers:
            print(f"  💢 Triggers: {', '.join(s.emotional_triggers[:3])}")
        
        print(f"\n⚠️ Risk Factors:")
        for rf in result.risk_factors:
            icon = "🔴" if rf.severity == "critical" else "🟠" if rf.severity == "high" else "🟡"
            print(f"  {icon} {rf.factor} ({rf.severity})")
            print(f"      Evidence: {rf.evidence[:60]}...")
        
        print(f"\n🎯 Recommended Actions:")
        for i, action in enumerate(result.recommended_actions, 1):
            print(f"  {i}. {action}")
        
        print(f"\n👤 Owner: {result.owner_recommendation}")
        
        print(f"\n📞 Talking Points for Call:")
        for point in result.talking_points[:4]:
            print(f"  • {point}")
        
        print(f"\n🛤️ Resolution Path:")
        print(f"  {result.resolution_path}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Escalation Predictor - Identify at-risk tickets"
    )
    
    parser.add_argument(
        "--ticket", "-t",
        type=str,
        default=DEFAULT_CONFIG["ticket_data"],
        help="Ticket data"
    )
    parser.add_argument(
        "--history", "-h",
        type=str,
        default=DEFAULT_CONFIG["customer_history"],
        help="Customer history"
    )
    
    args = parser.parse_args()
    
    config = {
        "ticket_data": args.ticket,
        "customer_history": args.history,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
