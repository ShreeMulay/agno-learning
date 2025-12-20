"""
Example #021: Ticket Router
Category: business/customer_success

DESCRIPTION:
Automatically classifies, prioritizes, and routes support tickets to the
appropriate team or agent. Uses NLP to understand ticket intent, extracts
key information, and applies routing rules based on urgency and expertise.

PATTERNS:
- Structured Output (TicketRouting with classification)
- Teams (route to appropriate team)

ARGUMENTS:
- ticket_subject (str): Ticket subject line. Default: sample
- ticket_body (str): Ticket description. Default: sample
- customer_tier (str): Customer tier. Default: "standard"
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
    "ticket_subject": "Cannot access my account after password reset",
    "ticket_body": """
    Hi,
    
    I tried to reset my password yesterday but now I can't log in at all.
    I've tried multiple times and even cleared my browser cache.
    This is urgent as I have a presentation tomorrow and need to access
    my files. I'm on the Enterprise plan.
    
    Please help ASAP!
    
    John Smith
    Acme Corp
    """,
    "customer_tier": "enterprise",
    "teams": "billing,technical,account,sales,product",
}


# =============================================================================
# Output Schema
# =============================================================================

class TicketClassification(BaseModel):
    """Ticket classification details."""
    
    category: str = Field(description="Primary category (billing/technical/account/sales/product)")
    subcategory: str = Field(description="More specific subcategory")
    intent: str = Field(description="Customer's primary intent")
    sentiment: str = Field(description="positive/neutral/negative/frustrated")
    complexity: str = Field(description="simple/moderate/complex")


class PriorityAssessment(BaseModel):
    """Priority determination."""
    
    priority: str = Field(description="critical/high/medium/low")
    urgency_score: int = Field(ge=1, le=10, description="Urgency 1-10")
    impact_score: int = Field(ge=1, le=10, description="Business impact 1-10")
    sla_tier: str = Field(description="SLA tier based on customer type")
    response_target: str = Field(description="Target response time")


class ExtractedInfo(BaseModel):
    """Key information extracted from ticket."""
    
    customer_name: Optional[str] = Field(default=None, description="Customer name if mentioned")
    company: Optional[str] = Field(default=None, description="Company name if mentioned")
    product_area: Optional[str] = Field(default=None, description="Product/feature mentioned")
    error_messages: list[str] = Field(default_factory=list, description="Any error messages")
    steps_tried: list[str] = Field(default_factory=list, description="Steps customer already tried")
    timeline: Optional[str] = Field(default=None, description="When issue started or deadline")


class RoutingDecision(BaseModel):
    """Routing recommendation."""
    
    primary_team: str = Field(description="Team to route to")
    backup_team: Optional[str] = Field(default=None, description="Backup team if primary unavailable")
    specialist_needed: bool = Field(description="Requires specialist attention")
    escalation_path: str = Field(description="Escalation path if needed")


class TicketRouting(BaseModel):
    """Complete ticket routing decision."""
    
    ticket_id: str = Field(description="Generated ticket reference")
    classification: TicketClassification = Field(description="Ticket classification")
    priority: PriorityAssessment = Field(description="Priority assessment")
    extracted_info: ExtractedInfo = Field(description="Extracted information")
    routing: RoutingDecision = Field(description="Routing decision")
    suggested_response_template: str = Field(description="Suggested initial response")
    similar_tickets_hint: str = Field(description="Hint about similar past issues")
    auto_resolution_possible: bool = Field(description="Can be auto-resolved with KB article")
    recommended_kb_articles: list[str] = Field(description="Relevant knowledge base articles")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Ticket Router agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for ticket routing
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Ticket Router",
        instructions=[
            "You are an expert support ticket router and classifier.",
            "Analyze tickets to determine optimal routing and priority.",
            "",
            f"Available Teams: {cfg['teams']}",
            f"Customer Tier: {cfg['customer_tier']}",
            "",
            "Classification Categories:",
            "- billing: Payment, invoices, subscriptions, refunds",
            "- technical: Bugs, errors, integrations, performance",
            "- account: Login, access, settings, permissions",
            "- sales: Upgrades, quotes, enterprise features",
            "- product: Feature requests, feedback, roadmap questions",
            "",
            "Priority Guidelines:",
            "- CRITICAL: System down, data loss, security breach",
            "- HIGH: Major feature broken, blocking customer work",
            "- MEDIUM: Feature degraded, workaround available",
            "- LOW: Questions, minor issues, feature requests",
            "",
            "SLA Tiers:",
            "- Enterprise: 1hr response, 4hr resolution",
            "- Professional: 4hr response, 24hr resolution",
            "- Standard: 24hr response, 72hr resolution",
            "",
            "Extract all relevant information and route appropriately.",
        ],
        output_schema=TicketRouting,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of ticket routing."""
    print("\n" + "=" * 60)
    print("  Ticket Router - Demo")
    print("=" * 60)
    
    subject = config.get("ticket_subject", DEFAULT_CONFIG["ticket_subject"])
    body = config.get("ticket_body", DEFAULT_CONFIG["ticket_body"])
    tier = config.get("customer_tier", DEFAULT_CONFIG["customer_tier"])
    
    query = f"""
    Route this support ticket:
    
    Customer Tier: {tier}
    Subject: {subject}
    
    Body:
    {body}
    
    Classify, prioritize, and route this ticket appropriately.
    """
    
    print(f"\nSubject: {subject}")
    print(f"Customer Tier: {tier}")
    print("-" * 40)
    print("Analyzing ticket...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, TicketRouting):
        print(f"\n{'='*50}")
        print(f"TICKET: {result.ticket_id}")
        print(f"{'='*50}")
        
        c = result.classification
        print(f"\n📋 Classification:")
        print(f"  Category: {c.category} → {c.subcategory}")
        print(f"  Intent: {c.intent}")
        print(f"  Sentiment: {c.sentiment} | Complexity: {c.complexity}")
        
        p = result.priority
        print(f"\n🚨 Priority: {p.priority.upper()}")
        print(f"  Urgency: {p.urgency_score}/10 | Impact: {p.impact_score}/10")
        print(f"  SLA: {p.sla_tier} - Response within {p.response_target}")
        
        e = result.extracted_info
        print(f"\n📝 Extracted Info:")
        if e.customer_name:
            print(f"  Customer: {e.customer_name}")
        if e.company:
            print(f"  Company: {e.company}")
        if e.product_area:
            print(f"  Product Area: {e.product_area}")
        if e.timeline:
            print(f"  Timeline: {e.timeline}")
        if e.steps_tried:
            print(f"  Already Tried: {', '.join(e.steps_tried)}")
        
        r = result.routing
        print(f"\n🎯 Routing Decision:")
        print(f"  Route to: {r.primary_team.upper()}")
        if r.backup_team:
            print(f"  Backup: {r.backup_team}")
        print(f"  Specialist Needed: {'Yes' if r.specialist_needed else 'No'}")
        print(f"  Escalation Path: {r.escalation_path}")
        
        print(f"\n💡 Auto-Resolution: {'Possible' if result.auto_resolution_possible else 'Manual handling required'}")
        
        if result.recommended_kb_articles:
            print(f"\n📚 KB Articles:")
            for article in result.recommended_kb_articles[:3]:
                print(f"  • {article}")
        
        print(f"\n💬 Suggested Response:")
        print(f"  {result.suggested_response_template[:200]}...")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ticket Router - Classify and route support tickets"
    )
    
    parser.add_argument(
        "--subject", "-s",
        type=str,
        default=DEFAULT_CONFIG["ticket_subject"],
        help="Ticket subject"
    )
    parser.add_argument(
        "--body", "-b",
        type=str,
        default=DEFAULT_CONFIG["ticket_body"],
        help="Ticket body/description"
    )
    parser.add_argument(
        "--tier", "-t",
        type=str,
        choices=["enterprise", "professional", "standard"],
        default=DEFAULT_CONFIG["customer_tier"],
        help="Customer tier"
    )
    
    args = parser.parse_args()
    
    config = {
        "ticket_subject": args.subject,
        "ticket_body": args.body,
        "customer_tier": args.tier,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
