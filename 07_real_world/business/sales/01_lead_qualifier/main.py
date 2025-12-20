"""
Example #001: Lead Qualifier
Category: business/sales

DESCRIPTION:
Scores and qualifies sales leads based on company information, engagement signals,
and fit criteria. Uses web search to enrich lead data and returns a structured
qualification score with reasoning. Perfect for prioritizing outreach efforts.

PATTERNS:
- Tools (DuckDuckGo for company research)
- Structured Output (LeadScore with qualification details)

ARGUMENTS:
- company_name (str): Company to research. Default: "Acme Corp"
- contact_email (str): Lead's email address. Default: "john@acme.com"
- industry (str): Target industry filter. Default: "technology"
- min_employees (int): Minimum company size. Default: 50
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
    "company_name": "Acme Corp",
    "contact_email": "john@acme.com",
    "industry": "technology",
    "min_employees": 50,
}


# =============================================================================
# Output Schema
# =============================================================================

class CompanyInfo(BaseModel):
    """Enriched company information."""
    
    name: str = Field(description="Company name")
    description: str = Field(description="Brief company description")
    industry: str = Field(description="Primary industry")
    estimated_size: str = Field(description="Estimated company size (startup/SMB/enterprise)")
    website: Optional[str] = Field(default=None, description="Company website if found")
    recent_news: list[str] = Field(default_factory=list, description="Recent news or updates")


class LeadScore(BaseModel):
    """Lead qualification result."""
    
    company: CompanyInfo = Field(description="Enriched company information")
    qualification_score: int = Field(ge=0, le=100, description="Lead score 0-100")
    qualification_tier: str = Field(description="hot/warm/cold based on score")
    fit_signals: list[str] = Field(description="Positive fit indicators")
    risk_signals: list[str] = Field(description="Concerns or red flags")
    recommended_action: str = Field(description="Suggested next step")
    reasoning: str = Field(description="Explanation of the score")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Lead Qualifier agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for lead qualification
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Lead Qualifier",
        instructions=[
            "You are an expert sales development representative (SDR) who qualifies leads.",
            "Use web search to research the company and gather relevant information.",
            "",
            "Qualification Criteria:",
            f"- Target Industry: {cfg['industry']}",
            f"- Minimum Company Size: {cfg['min_employees']} employees",
            "- Look for: funding news, hiring signals, tech stack mentions, pain points",
            "",
            "Scoring Guidelines:",
            "- 80-100 (HOT): Perfect fit, strong buying signals, decision-maker contact",
            "- 50-79 (WARM): Good fit, some interest indicators, worth nurturing",
            "- 0-49 (COLD): Poor fit, no signals, or disqualifying factors",
            "",
            "Be thorough but concise. Focus on actionable insights.",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=LeadScore,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of lead qualification."""
    print("\n" + "=" * 60)
    print("  Lead Qualifier - Demo")
    print("=" * 60)
    
    company = config.get("company_name", DEFAULT_CONFIG["company_name"])
    email = config.get("contact_email", DEFAULT_CONFIG["contact_email"])
    
    query = f"""
    Qualify this lead:
    - Company: {company}
    - Contact Email: {email}
    
    Research the company, assess fit, and provide a qualification score.
    """
    
    print(f"\nQualifying: {company} ({email})")
    print("-" * 40)
    print("Researching company...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, LeadScore):
        print(f"\n{'='*40}")
        print(f"LEAD SCORE: {result.qualification_score}/100 ({result.qualification_tier.upper()})")
        print(f"{'='*40}")
        
        print(f"\nCompany: {result.company.name}")
        print(f"Industry: {result.company.industry}")
        print(f"Size: {result.company.estimated_size}")
        if result.company.website:
            print(f"Website: {result.company.website}")
        
        print(f"\n📝 Description:\n{result.company.description}")
        
        if result.company.recent_news:
            print(f"\n📰 Recent News:")
            for news in result.company.recent_news[:3]:
                print(f"  • {news}")
        
        print(f"\n✅ Fit Signals:")
        for signal in result.fit_signals:
            print(f"  • {signal}")
        
        if result.risk_signals:
            print(f"\n⚠️  Risk Signals:")
            for risk in result.risk_signals:
                print(f"  • {risk}")
        
        print(f"\n💡 Recommended Action:\n{result.recommended_action}")
        print(f"\n📊 Reasoning:\n{result.reasoning}")
    else:
        # Fallback for when structured output parsing fails
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Lead Qualifier - Score and qualify sales leads"
    )
    
    parser.add_argument(
        "--company", "-c",
        type=str,
        default=DEFAULT_CONFIG["company_name"],
        help=f"Company name to research (default: {DEFAULT_CONFIG['company_name']})"
    )
    parser.add_argument(
        "--email", "-e",
        type=str,
        default=DEFAULT_CONFIG["contact_email"],
        help=f"Contact email (default: {DEFAULT_CONFIG['contact_email']})"
    )
    parser.add_argument(
        "--industry", "-i",
        type=str,
        default=DEFAULT_CONFIG["industry"],
        help=f"Target industry (default: {DEFAULT_CONFIG['industry']})"
    )
    parser.add_argument(
        "--min-employees", "-m",
        type=int,
        default=DEFAULT_CONFIG["min_employees"],
        help=f"Minimum company size (default: {DEFAULT_CONFIG['min_employees']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "company_name": args.company,
        "contact_email": args.email,
        "industry": args.industry,
        "min_employees": args.min_employees,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
