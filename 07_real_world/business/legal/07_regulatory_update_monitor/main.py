"""
Example #057: Regulatory Update Monitor
Category: business/legal

DESCRIPTION:
Monitors regulatory changes and assesses impact on business operations.

PATTERNS:
- Knowledge (regulatory landscape)
- Structured Output (RegulatoryUpdate)

ARGUMENTS:
- update_text (str): Regulatory update or news
- industry (str): Business sector
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "update_text": """
    The Federal Trade Commission announced new rules regarding AI-generated content
    and advertising disclosures effective March 2025. Key requirements:
    
    1. AI-Generated Content Disclosure: Any marketing material using AI-generated
    images, text, or audio must include clear disclosure.
    
    2. Review Requirements: Companies must have human review processes for
    AI-generated advertising claims before publication.
    
    3. Documentation: Maintain records of AI systems used in marketing for 3 years.
    
    4. Penalties: Up to $50,000 per violation for non-compliance.
    """,
    "industry": "SaaS Technology",
}


class ImpactArea(BaseModel):
    area: str = Field(description="Business area affected")
    impact_level: str = Field(description="high/medium/low")
    changes_required: list[str] = Field(description="What needs to change")
    deadline: Optional[str] = Field(default=None, description="When to comply")


class RegulatoryUpdate(BaseModel):
    regulation_name: str = Field(description="Name of regulation")
    issuing_body: str = Field(description="Who issued it")
    effective_date: str = Field(description="When it takes effect")
    summary: str = Field(description="Brief summary")
    key_requirements: list[str] = Field(description="Main requirements")
    impact_areas: list[ImpactArea] = Field(description="Areas affected")
    compliance_actions: list[str] = Field(description="Steps to take")
    risk_if_ignored: str = Field(description="Consequences of non-compliance")
    priority: str = Field(description="critical/high/medium/low")
    estimated_effort: str = Field(description="Effort to comply")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Regulatory Update Monitor",
        instructions=[
            "You are a regulatory compliance analyst.",
            f"Assess regulatory updates for {cfg['industry']} companies.",
            "",
            "Analysis Framework:",
            "- Identify specific requirements",
            "- Map to business functions affected",
            "- Estimate compliance effort",
            "- Prioritize by deadline and penalty risk",
        ],
        output_schema=RegulatoryUpdate,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Regulatory Update Monitor - Demo")
    print("=" * 60)
    
    update = config.get("update_text", DEFAULT_CONFIG["update_text"])
    
    response = agent.run(f"Analyze this regulatory update:\n\n{update}")
    result = response.content
    
    if isinstance(result, RegulatoryUpdate):
        priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
        print(f"\n{priority_icon.get(result.priority, '?')} {result.regulation_name}")
        print(f"Issued by: {result.issuing_body}")
        print(f"Effective: {result.effective_date}")
        
        print(f"\n📋 Summary: {result.summary}")
        
        print(f"\n📜 Key Requirements:")
        for r in result.key_requirements:
            print(f"   • {r}")
        
        print(f"\n🎯 Impact Areas:")
        for a in result.impact_areas:
            print(f"   [{a.impact_level.upper()}] {a.area}")
            for c in a.changes_required:
                print(f"      • {c}")
        
        print(f"\n✅ Compliance Actions:")
        for a in result.compliance_actions:
            print(f"   • {a}")
        
        print(f"\n⚠️ Risk: {result.risk_if_ignored}")
        print(f"⏱️ Effort: {result.estimated_effort}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Regulatory Update Monitor")
    parser.add_argument("--update", "-u", type=str, default=DEFAULT_CONFIG["update_text"])
    parser.add_argument("--industry", "-i", type=str, default=DEFAULT_CONFIG["industry"])
    args = parser.parse_args()
    agent = get_agent(config={"update_text": args.update, "industry": args.industry})
    run_demo(agent, {"update_text": args.update})


if __name__ == "__main__":
    main()
