"""
Example #178: Grant Writer Agent
Category: research/science
DESCRIPTION: Assists with research grant proposal writing
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"project_title": "AI-Driven Drug Discovery", "funding_agency": "NIH", "amount": 500000}

class GrantSection(BaseModel):
    section_name: str = Field(description="Section name")
    content: str = Field(description="Section content")
    tips: list[str] = Field(description="Writing tips for section")

class GrantProposal(BaseModel):
    project_title: str = Field(description="Project title")
    executive_summary: str = Field(description="Executive summary")
    specific_aims: list[str] = Field(description="Specific aims")
    significance: str = Field(description="Significance statement")
    innovation: str = Field(description="Innovation statement")
    approach_summary: str = Field(description="Approach summary")
    timeline_overview: str = Field(description="Timeline overview")
    budget_justification: str = Field(description="Budget justification")
    sections: list[GrantSection] = Field(description="Key sections")
    common_pitfalls: list[str] = Field(description="Pitfalls to avoid")
    success_factors: list[str] = Field(description="Success factors")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Grant Writer",
        instructions=[
            "You are an expert research grant writer.",
            f"Write grants for {cfg['funding_agency']}",
            f"Target funding: ${cfg['amount']:,}",
            "Follow agency-specific guidelines",
            "Emphasize significance and innovation",
            "Provide clear, achievable aims",
        ],
        output_schema=GrantProposal,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Grant Writer Agent - Demo")
    print("=" * 60)
    query = f"""Write grant proposal:
- Title: {config['project_title']}
- Agency: {config['funding_agency']}
- Amount: ${config['amount']:,}

Create compelling grant proposal content."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, GrantProposal):
        print(f"\n📋 {result.project_title}")
        print(f"\n📝 Executive Summary:\n{result.executive_summary[:200]}...")
        print(f"\n🎯 Specific Aims:")
        for i, aim in enumerate(result.specific_aims[:3], 1):
            print(f"  {i}. {aim}")
        print(f"\n⭐ Significance: {result.significance[:100]}...")
        print(f"💡 Innovation: {result.innovation[:100]}...")
        print(f"\n⚠️ Avoid: {result.common_pitfalls[0]}")

def main():
    parser = argparse.ArgumentParser(description="Grant Writer Agent")
    parser.add_argument("--title", "-t", default=DEFAULT_CONFIG["project_title"])
    parser.add_argument("--agency", "-a", default=DEFAULT_CONFIG["funding_agency"])
    parser.add_argument("--amount", type=int, default=DEFAULT_CONFIG["amount"])
    args = parser.parse_args()
    config = {"project_title": args.title, "funding_agency": args.agency, "amount": args.amount}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
