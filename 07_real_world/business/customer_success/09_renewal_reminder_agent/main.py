"""
Example #029: Renewal Reminder Agent
Category: business/customer_success

DESCRIPTION:
Proactively manages renewal outreach with personalized timing and messaging.
Tracks renewal pipeline, identifies upsell opportunities, and generates
customized renewal communications based on customer context.

PATTERNS:
- Memory (track outreach history)
- Tools (date calculations)
- Structured Output (RenewalPlan)

ARGUMENTS:
- customer_data (str): Customer renewal info. Default: sample
- days_to_renewal (int): Days until renewal. Default: 90
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
    Customer: DataSync Corp
    Tier: Professional
    Current ARR: $36,000
    Contract Start: 11 months ago
    Renewal Date: 30 days from now
    
    Account Health: 78/100 (Healthy)
    NPS: 8
    Product Usage: High (top 20% of cohort)
    
    Key Contacts:
    - Sarah Chen (Champion, VP Engineering) - Engaged
    - Mike Ross (Decision Maker, CTO) - Met twice
    - Finance Contact: Unknown
    
    History:
    - Onboarding: Smooth, completed in 3 weeks
    - Support Tickets: 4 total, all resolved satisfactorily
    - Feature Requests: 2 (both in roadmap)
    - Expansion Discussions: Mentioned adding 2 more teams
    
    Competitor Intelligence:
    - No known competitor evaluation
    - Happy with product fit
    
    Outreach History:
    - QBR: 2 months ago (positive)
    - Last CSM Call: 3 weeks ago
    - Renewal Mentioned: Not yet discussed
    """,
    "days_to_renewal": 30,
}


# =============================================================================
# Output Schema
# =============================================================================

class OutreachMessage(BaseModel):
    """Personalized outreach message."""
    
    channel: str = Field(description="email/call/meeting")
    recipient: str = Field(description="Who to contact")
    timing: str = Field(description="When to send/schedule")
    subject: str = Field(description="Email subject or call purpose")
    message: str = Field(description="Message content or talking points")
    goal: str = Field(description="Objective of this outreach")


class UpsellOpportunity(BaseModel):
    """Identified expansion opportunity."""
    
    opportunity: str = Field(description="What to propose")
    rationale: str = Field(description="Why this makes sense")
    potential_value: str = Field(description="Additional revenue")
    timing: str = Field(description="When to discuss")
    stakeholder: str = Field(description="Who to pitch to")


class RenewalRisk(BaseModel):
    """Risk to renewal."""
    
    risk: str = Field(description="Risk description")
    likelihood: str = Field(description="high/medium/low")
    mitigation: str = Field(description="How to address")


class RenewalPlan(BaseModel):
    """Complete renewal management plan."""
    
    customer: str = Field(description="Customer name")
    current_arr: str = Field(description="Current annual revenue")
    days_to_renewal: int = Field(description="Days until renewal")
    renewal_likelihood: int = Field(ge=0, le=100, description="Renewal probability %")
    recommended_action: str = Field(description="Primary recommended action")
    outreach_sequence: list[OutreachMessage] = Field(description="Planned outreach")
    upsell_opportunities: list[UpsellOpportunity] = Field(description="Expansion possibilities")
    renewal_risks: list[RenewalRisk] = Field(description="Identified risks")
    stakeholder_strategy: dict = Field(description="Approach per stakeholder")
    negotiation_prep: list[str] = Field(description="Negotiation talking points")
    fallback_options: list[str] = Field(description="If they want to downgrade/churn")
    success_metrics: list[str] = Field(description="What success looks like")
    timeline: list[str] = Field(description="Key dates and milestones")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Renewal Reminder Agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for renewal management
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Renewal Reminder Agent",
        instructions=[
            "You are a renewal management specialist.",
            "Create personalized renewal strategies to maximize retention and expansion.",
            "",
            f"Days to Renewal: {cfg['days_to_renewal']}",
            "",
            "Renewal Timeline Best Practices:",
            "- 90 days out: Health check, address any issues",
            "- 60 days out: Begin renewal conversation",
            "- 45 days out: Proposal and negotiation",
            "- 30 days out: Close deal, get signatures",
            "- 14 days out: Escalate if not closed",
            "",
            "Outreach Principles:",
            "- Personalize based on relationship history",
            "- Lead with value delivered, not the ask",
            "- Address concerns proactively",
            "- Multi-thread (engage multiple stakeholders)",
            "- Have upsell ready but don't force it",
            "",
            "Negotiation Strategies:",
            "- Know your walk-away point",
            "- Prepare value documentation",
            "- Have discount authority clear",
            "- Offer multi-year for better terms",
            "",
            "Create a comprehensive renewal plan with specific actions and timing.",
        ],
        output_schema=RenewalPlan,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of renewal planning."""
    print("\n" + "=" * 60)
    print("  Renewal Reminder Agent - Demo")
    print("=" * 60)
    
    data = config.get("customer_data", DEFAULT_CONFIG["customer_data"])
    days = config.get("days_to_renewal", DEFAULT_CONFIG["days_to_renewal"])
    
    query = f"""
    Create a renewal plan for this customer:
    
    {data}
    
    Days to Renewal: {days}
    
    Generate outreach sequence, identify upsell opportunities,
    and prepare negotiation strategy.
    """
    
    print(f"\nDays to Renewal: {days}")
    print("-" * 40)
    print("Creating renewal plan...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, RenewalPlan):
        print(f"\n{'='*50}")
        print(f"RENEWAL PLAN: {result.customer}")
        print(f"{'='*50}")
        
        print(f"\n💰 Current ARR: {result.current_arr}")
        print(f"📅 Days to Renewal: {result.days_to_renewal}")
        print(f"📊 Renewal Likelihood: {result.renewal_likelihood}%")
        print(f"\n🎯 Recommended Action: {result.recommended_action}")
        
        print(f"\n📧 Outreach Sequence:")
        for i, msg in enumerate(result.outreach_sequence, 1):
            print(f"\n  {i}. [{msg.channel.upper()}] {msg.timing}")
            print(f"     To: {msg.recipient}")
            print(f"     Subject: {msg.subject}")
            print(f"     Goal: {msg.goal}")
            print(f"     Message: {msg.message[:100]}...")
        
        if result.upsell_opportunities:
            print(f"\n📈 Upsell Opportunities:")
            for opp in result.upsell_opportunities:
                print(f"\n  {opp.opportunity}")
                print(f"    Value: {opp.potential_value}")
                print(f"    Pitch to: {opp.stakeholder}")
                print(f"    Rationale: {opp.rationale}")
        
        if result.renewal_risks:
            print(f"\n⚠️ Renewal Risks:")
            for risk in result.renewal_risks:
                print(f"  • {risk.risk} ({risk.likelihood})")
                print(f"    Mitigation: {risk.mitigation}")
        
        print(f"\n👥 Stakeholder Strategy:")
        for stakeholder, strategy in result.stakeholder_strategy.items():
            print(f"  {stakeholder}: {strategy}")
        
        print(f"\n🎤 Negotiation Prep:")
        for point in result.negotiation_prep[:4]:
            print(f"  • {point}")
        
        print(f"\n📅 Timeline:")
        for milestone in result.timeline[:5]:
            print(f"  • {milestone}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Renewal Reminder Agent - Manage renewal outreach"
    )
    
    parser.add_argument(
        "--data", "-d",
        type=str,
        default=DEFAULT_CONFIG["customer_data"],
        help="Customer renewal data"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_CONFIG["days_to_renewal"],
        help="Days to renewal"
    )
    
    args = parser.parse_args()
    
    config = {
        "customer_data": args.data,
        "days_to_renewal": args.days,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
