"""
Example #053: Compliance Checker
Category: business/legal

DESCRIPTION:
Reviews business practices and documents against regulatory
requirements to identify potential compliance violations.

PATTERNS:
- Knowledge (regulatory frameworks)
- Structured Output (ComplianceReport)
- Reasoning (violation detection)

ARGUMENTS:
- practice_description (str): Business practice to check
- regulations (str): Applicable regulations
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "practice_description": """
    Our SaaS company collects user data including:
    - Email addresses and names for account creation
    - Usage analytics (pages visited, features used, session duration)
    - Payment information processed through Stripe
    - IP addresses and device information
    - Location data (city-level) for analytics
    
    Current practices:
    - Cookie consent banner shown on first visit
    - Privacy policy link in footer
    - Users can delete account via support ticket (takes 30 days)
    - Data stored on AWS servers in US-East-1
    - No explicit consent for marketing emails
    - Third-party analytics (Google Analytics, Mixpanel)
    - Data shared with advertising partners for retargeting
    """,
    "regulations": "GDPR, CCPA",
    "jurisdiction": "EU and California users",
}


class Violation(BaseModel):
    regulation: str = Field(description="Which regulation")
    requirement: str = Field(description="Specific requirement violated")
    current_practice: str = Field(description="What the company is doing")
    severity: str = Field(description="critical/high/medium/low")
    remediation: str = Field(description="How to fix it")
    deadline: Optional[str] = Field(default=None, description="Urgency")


class ComplianceReport(BaseModel):
    regulations_checked: list[str] = Field(description="Regulations reviewed")
    overall_status: str = Field(description="compliant/partial/non-compliant")
    compliance_score: int = Field(ge=0, le=100, description="Compliance percentage")
    violations: list[Violation] = Field(description="Identified violations")
    compliant_areas: list[str] = Field(description="Areas meeting requirements")
    immediate_actions: list[str] = Field(description="Must do now")
    recommended_improvements: list[str] = Field(description="Should do soon")
    documentation_needed: list[str] = Field(description="Docs to create/update")
    risk_assessment: str = Field(description="Potential penalties/exposure")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Compliance Checker",
        instructions=[
            "You are a privacy and compliance expert.",
            "Evaluate practices against regulatory requirements.",
            "",
            "Key GDPR Requirements:",
            "- Lawful basis for processing",
            "- Explicit consent for marketing",
            "- Right to erasure (within 30 days)",
            "- Data minimization",
            "- Privacy by design",
            "- DPA with processors",
            "- Cross-border transfer safeguards",
            "",
            "Key CCPA Requirements:",
            "- Right to know what data is collected",
            "- Right to delete",
            "- Right to opt-out of sale",
            "- No discrimination for exercising rights",
            "",
            "Be specific about violations and remediation steps.",
        ],
        output_schema=ComplianceReport,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Compliance Checker - Demo")
    print("=" * 60)
    
    practice = config.get("practice_description", DEFAULT_CONFIG["practice_description"])
    regulations = config.get("regulations", DEFAULT_CONFIG["regulations"])
    
    response = agent.run(f"Check compliance with {regulations}:\n\n{practice}")
    result = response.content
    
    if isinstance(result, ComplianceReport):
        print(f"\n📋 Regulations Checked: {', '.join(result.regulations_checked)}")
        
        status_icon = {"compliant": "✅", "partial": "🟡", "non-compliant": "🔴"}
        print(f"{status_icon.get(result.overall_status, '?')} Status: {result.overall_status.upper()}")
        print(f"📊 Compliance Score: {result.compliance_score}%")
        
        if result.violations:
            print(f"\n🚨 Violations Found ({len(result.violations)}):")
            for v in result.violations:
                sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                print(f"\n   {sev_icon.get(v.severity, '⚪')} [{v.regulation}] {v.requirement}")
                print(f"   Current: {v.current_practice}")
                print(f"   Fix: {v.remediation}")
        
        if result.compliant_areas:
            print(f"\n✅ Compliant Areas:")
            for a in result.compliant_areas:
                print(f"   • {a}")
        
        print(f"\n⚡ Immediate Actions Required:")
        for a in result.immediate_actions:
            print(f"   • {a}")
        
        print(f"\n📄 Documentation Needed:")
        for d in result.documentation_needed:
            print(f"   • {d}")
        
        print(f"\n⚠️ Risk Assessment:")
        print(f"   {result.risk_assessment}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Compliance Checker")
    parser.add_argument("--practice", "-p", type=str, default=DEFAULT_CONFIG["practice_description"])
    parser.add_argument("--regulations", "-r", type=str, default=DEFAULT_CONFIG["regulations"])
    args = parser.parse_args()
    agent = get_agent(config={"practice_description": args.practice, "regulations": args.regulations})
    run_demo(agent, {"practice_description": args.practice, "regulations": args.regulations})


if __name__ == "__main__":
    main()
