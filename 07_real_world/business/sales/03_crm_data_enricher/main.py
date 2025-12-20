"""
Example #003: CRM Data Enricher
Category: business/sales

DESCRIPTION:
Automatically enriches CRM contact records with company information,
LinkedIn insights, recent news, and technology stack details.
Perfect for keeping CRM data fresh and actionable.

PATTERNS:
- Tools (DuckDuckGo for company research)
- Knowledge (company database for context)
- Structured Output (EnrichedContact schema)

ARGUMENTS:
- company_name (str): Company to enrich. Default: "Stripe"
- contact_name (str): Contact name. Default: "Patrick Collison"
- existing_data (str): Known info. Default: ""
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "company_name": "Stripe",
    "contact_name": "Patrick Collison",
    "existing_data": "",
}


# =============================================================================
# Output Schema
# =============================================================================

class TechStack(BaseModel):
    """Technology stack information."""
    languages: list[str] = Field(default_factory=list, description="Programming languages")
    frameworks: list[str] = Field(default_factory=list, description="Frameworks used")
    cloud_providers: list[str] = Field(default_factory=list, description="Cloud platforms")
    tools: list[str] = Field(default_factory=list, description="Dev tools and services")


class EnrichedContact(BaseModel):
    """Enriched CRM contact record."""
    
    # Company Info
    company_name: str = Field(description="Official company name")
    company_description: str = Field(description="What the company does")
    industry: str = Field(description="Primary industry")
    company_size: str = Field(description="Employee count range")
    headquarters: str = Field(description="HQ location")
    founded_year: Optional[int] = Field(default=None, description="Year founded")
    website: str = Field(description="Company website")
    
    # Funding & Financial
    funding_stage: str = Field(description="Seed/Series A/B/C/Public/Bootstrapped")
    recent_funding: Optional[str] = Field(default=None, description="Recent funding info")
    
    # Technology
    tech_stack: TechStack = Field(description="Technology stack details")
    
    # Contact Context
    contact_title: Optional[str] = Field(default=None, description="Likely title if found")
    relevant_news: list[str] = Field(default_factory=list, description="Recent company news")
    
    # Sales Intelligence
    potential_pain_points: list[str] = Field(description="Likely challenges")
    talking_points: list[str] = Field(description="Conversation starters")
    confidence_score: int = Field(ge=0, le=100, description="Data confidence 0-100")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the CRM Data Enricher agent.
    
    Args:
        model: Override default model
        config: Configuration options
    
    Returns:
        Configured Agent for data enrichment
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    existing = cfg.get("existing_data", "")
    existing_context = f"\nExisting data to verify/update:\n{existing}" if existing else ""
    
    return Agent(
        model=model or default_model(),
        name="CRM Data Enricher",
        instructions=[
            "You are a data enrichment specialist for CRM systems.",
            "Research companies thoroughly using web search.",
            "",
            "Data Collection Priorities:",
            "1. Company basics (industry, size, HQ)",
            "2. Funding and financial status",
            "3. Technology stack (especially if B2B tech)",
            "4. Recent news and developments",
            "5. Potential pain points for sales context",
            "",
            "Quality Guidelines:",
            "- Only include verified information",
            "- Note when data is estimated vs confirmed",
            "- Provide a confidence score for overall data quality",
            "- Flag any conflicting information found",
            existing_context,
        ],
        tools=[DuckDuckGoTools()],
        output_schema=EnrichedContact,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of data enrichment."""
    print("\n" + "=" * 60)
    print("  CRM Data Enricher - Demo")
    print("=" * 60)
    
    company = config.get("company_name", DEFAULT_CONFIG["company_name"])
    contact = config.get("contact_name", DEFAULT_CONFIG["contact_name"])
    
    query = f"""
    Enrich this CRM record:
    - Company: {company}
    - Contact: {contact}
    
    Research and provide comprehensive company data.
    """
    
    print(f"\nEnriching: {contact} @ {company}")
    print("-" * 40)
    print("Researching...")
    
    response = agent.run(query)
    
    result = response.content
    if isinstance(result, EnrichedContact):
        data = result
        
        print(f"\n{'='*50}")
        print(f"  {data.company_name}")
        print(f"  Confidence: {data.confidence_score}%")
        print(f"{'='*50}")
        
        print(f"\n📋 Company Overview:")
        print(f"  Industry: {data.industry}")
        print(f"  Size: {data.company_size}")
        print(f"  HQ: {data.headquarters}")
        print(f"  Website: {data.website}")
        if data.founded_year:
            print(f"  Founded: {data.founded_year}")
        
        print(f"\n💰 Funding:")
        print(f"  Stage: {data.funding_stage}")
        if data.recent_funding:
            print(f"  Recent: {data.recent_funding}")
        
        print(f"\n💻 Tech Stack:")
        if data.tech_stack.languages:
            print(f"  Languages: {', '.join(data.tech_stack.languages)}")
        if data.tech_stack.frameworks:
            print(f"  Frameworks: {', '.join(data.tech_stack.frameworks)}")
        if data.tech_stack.cloud_providers:
            print(f"  Cloud: {', '.join(data.tech_stack.cloud_providers)}")
        
        if data.relevant_news:
            print(f"\n📰 Recent News:")
            for news in data.relevant_news[:3]:
                print(f"  • {news}")
        
        print(f"\n🎯 Sales Intelligence:")
        print(f"  Pain Points:")
        for pain in data.potential_pain_points[:3]:
            print(f"    • {pain}")
        print(f"  Talking Points:")
        for point in data.talking_points[:3]:
            print(f"    • {point}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CRM Data Enricher - Enrich contact records"
    )
    
    parser.add_argument(
        "--company", "-c",
        type=str,
        default=DEFAULT_CONFIG["company_name"],
        help="Company name to research"
    )
    parser.add_argument(
        "--contact", "-n",
        type=str,
        default=DEFAULT_CONFIG["contact_name"],
        help="Contact name"
    )
    parser.add_argument(
        "--existing", "-e",
        type=str,
        default="",
        help="Existing data to verify"
    )
    
    args = parser.parse_args()
    
    config = {
        "company_name": args.company,
        "contact_name": args.contact,
        "existing_data": args.existing,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
