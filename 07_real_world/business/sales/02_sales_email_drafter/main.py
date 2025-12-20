"""
Example #002: Sales Email Drafter
Category: business/sales

DESCRIPTION:
Generates personalized cold outreach emails based on prospect research.
Uses web search to find relevant talking points and crafts emails that
reference specific company news, challenges, or initiatives.

PATTERNS:
- Tools (DuckDuckGo for prospect research)
- Memory (conversation history for follow-up sequences)

ARGUMENTS:
- prospect_name (str): Contact's name. Default: "Sarah Johnson"
- company_name (str): Target company. Default: "TechCorp"
- your_company (str): Your company name. Default: "SalesBot Inc"
- product (str): Product/service being sold. Default: "AI Sales Assistant"
- email_type (str): cold/follow_up/breakup. Default: "cold"
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.db.sqlite import SqliteDb
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "prospect_name": "Sarah Johnson",
    "company_name": "TechCorp",
    "your_company": "SalesBot Inc",
    "product": "AI Sales Assistant",
    "email_type": "cold",
    "session_id": "default",
}


# =============================================================================
# Output Schema
# =============================================================================

class SalesEmail(BaseModel):
    """Generated sales email."""
    
    subject_line: str = Field(description="Email subject line")
    body: str = Field(description="Email body text")
    personalization_points: list[str] = Field(
        description="Specific personalization elements used"
    )
    call_to_action: str = Field(description="The specific CTA in the email")
    follow_up_timing: str = Field(description="Suggested time to follow up")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Sales Email Drafter agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for email drafting
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Sales Email Drafter",
        instructions=[
            "You are an expert sales copywriter who crafts personalized outreach emails.",
            "Research the prospect's company to find relevant talking points.",
            "",
            f"You work for: {cfg['your_company']}",
            f"Product/Service: {cfg['product']}",
            "",
            "Email Guidelines:",
            "- Keep emails under 150 words",
            "- Lead with value, not features",
            "- Use specific, researched personalization",
            "- Include one clear call-to-action",
            "- Sound human, not salesy",
            "",
            "Email Types:",
            "- cold: First touch, focus on relevance and curiosity",
            "- follow_up: Reference previous email, add new value",
            "- breakup: Final attempt, create urgency",
        ],
        tools=[DuckDuckGoTools()],
        db=SqliteDb(db_file="sales_data.db"),
        session_id=cfg.get("session_id", "default"),
        output_schema=SalesEmail,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of email drafting."""
    print("\n" + "=" * 60)
    print("  Sales Email Drafter - Demo")
    print("=" * 60)
    
    prospect = config.get("prospect_name", DEFAULT_CONFIG["prospect_name"])
    company = config.get("company_name", DEFAULT_CONFIG["company_name"])
    email_type = config.get("email_type", DEFAULT_CONFIG["email_type"])
    
    query = f"""
    Draft a {email_type} email to:
    - Name: {prospect}
    - Company: {company}
    
    Research the company first to personalize the email.
    """
    
    print(f"\nDrafting {email_type} email to {prospect} at {company}...")
    print("-" * 40)
    
    response = agent.run(query)
    
    result = response.content
    if isinstance(result, SalesEmail):
        email = result
        print(f"\n📧 Subject: {email.subject_line}")
        print(f"\n{'─'*50}")
        print(email.body)
        print(f"{'─'*50}")
        
        print(f"\n🎯 Personalization Used:")
        for point in email.personalization_points:
            print(f"  • {point}")
        
        print(f"\n📞 CTA: {email.call_to_action}")
        print(f"⏰ Follow up: {email.follow_up_timing}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Sales Email Drafter - Personalized outreach emails"
    )
    
    parser.add_argument(
        "--prospect", "-p",
        type=str,
        default=DEFAULT_CONFIG["prospect_name"],
        help="Prospect's name"
    )
    parser.add_argument(
        "--company", "-c",
        type=str,
        default=DEFAULT_CONFIG["company_name"],
        help="Target company"
    )
    parser.add_argument(
        "--your-company",
        type=str,
        default=DEFAULT_CONFIG["your_company"],
        help="Your company name"
    )
    parser.add_argument(
        "--product",
        type=str,
        default=DEFAULT_CONFIG["product"],
        help="Product/service being sold"
    )
    parser.add_argument(
        "--type", "-t",
        type=str,
        choices=["cold", "follow_up", "breakup"],
        default=DEFAULT_CONFIG["email_type"],
        help="Email type"
    )
    parser.add_argument(
        "--session",
        type=str,
        default="default",
        help="Session ID for conversation memory"
    )
    
    args = parser.parse_args()
    
    config = {
        "prospect_name": args.prospect,
        "company_name": args.company,
        "your_company": args.your_company,
        "product": args.product,
        "email_type": args.type,
        "session_id": args.session,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
