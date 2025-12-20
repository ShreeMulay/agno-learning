"""
Example #054: Privacy Policy Analyzer
Category: business/legal

DESCRIPTION:
Analyzes privacy policies for completeness, clarity, and
compliance with GDPR, CCPA, and other privacy regulations.

PATTERNS:
- Knowledge (privacy law requirements)
- Structured Output (PolicyAnalysis)
- Reasoning (gap identification)

ARGUMENTS:
- policy_text (str): Privacy policy to analyze
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "policy_text": """
    Privacy Policy
    Last Updated: January 2023
    
    We collect information you provide directly to us, such as when you create
    an account, make a purchase, or contact support.
    
    Information We Collect:
    - Account information (name, email, password)
    - Payment information
    - Usage data
    
    We use your information to provide our services, process transactions,
    and send you updates about our products.
    
    We may share information with third-party service providers who assist
    in operating our service.
    
    We use cookies to improve your experience.
    
    Contact us at privacy@example.com with questions.
    """,
}


class PolicySection(BaseModel):
    section: str = Field(description="Policy section name")
    present: bool = Field(description="Is this section present?")
    quality: str = Field(description="poor/adequate/good/excellent")
    issues: list[str] = Field(description="Problems with this section")
    suggestions: list[str] = Field(description="Improvements needed")


class PolicyAnalysis(BaseModel):
    last_updated: str = Field(description="When policy was last updated")
    readability_score: str = Field(description="easy/moderate/difficult")
    word_count: int = Field(description="Approximate word count")
    gdpr_compliant: bool = Field(description="Meets GDPR requirements?")
    ccpa_compliant: bool = Field(description="Meets CCPA requirements?")
    sections_reviewed: list[PolicySection] = Field(description="Section-by-section review")
    missing_elements: list[str] = Field(description="Required elements not present")
    vague_language: list[str] = Field(description="Unclear or ambiguous terms")
    concerning_clauses: list[str] = Field(description="Potentially problematic terms")
    overall_grade: str = Field(description="A/B/C/D/F")
    priority_fixes: list[str] = Field(description="Most important changes")
    summary: str = Field(description="Overall assessment")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Privacy Policy Analyzer",
        instructions=[
            "You are a privacy attorney reviewing privacy policies.",
            "Evaluate completeness, clarity, and regulatory compliance.",
            "",
            "Required Sections (GDPR/CCPA):",
            "- Identity and contact of data controller",
            "- Types of data collected",
            "- Purposes of processing",
            "- Legal basis for processing",
            "- Data retention periods",
            "- Third-party sharing",
            "- International transfers",
            "- User rights (access, deletion, portability)",
            "- How to exercise rights",
            "- Cookie policy",
            "- Children's privacy",
            "- Policy updates notification",
            "",
            "Flag vague language like 'may', 'might', 'sometimes'.",
        ],
        output_schema=PolicyAnalysis,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Privacy Policy Analyzer - Demo")
    print("=" * 60)
    
    policy = config.get("policy_text", DEFAULT_CONFIG["policy_text"])
    
    response = agent.run(f"Analyze this privacy policy:\n\n{policy}")
    result = response.content
    
    if isinstance(result, PolicyAnalysis):
        print(f"\n📄 Policy Analysis")
        print(f"Last Updated: {result.last_updated}")
        print(f"Readability: {result.readability_score} | Words: ~{result.word_count}")
        
        gdpr = "✅" if result.gdpr_compliant else "❌"
        ccpa = "✅" if result.ccpa_compliant else "❌"
        print(f"GDPR: {gdpr} | CCPA: {ccpa}")
        print(f"Grade: {result.overall_grade}")
        
        print(f"\n📋 Section Analysis:")
        for s in result.sections_reviewed:
            icon = "✅" if s.present else "❌"
            print(f"   {icon} {s.section} [{s.quality}]")
            if s.issues:
                for i in s.issues:
                    print(f"      ⚠️ {i}")
        
        if result.missing_elements:
            print(f"\n❌ Missing Required Elements:")
            for m in result.missing_elements:
                print(f"   • {m}")
        
        if result.vague_language:
            print(f"\n🔍 Vague Language:")
            for v in result.vague_language:
                print(f"   • {v}")
        
        print(f"\n🔧 Priority Fixes:")
        for i, f in enumerate(result.priority_fixes, 1):
            print(f"   {i}. {f}")
        
        print(f"\n📝 {result.summary}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Privacy Policy Analyzer")
    parser.add_argument("--policy", "-p", type=str, default=DEFAULT_CONFIG["policy_text"])
    args = parser.parse_args()
    agent = get_agent(config={"policy_text": args.policy})
    run_demo(agent, {"policy_text": args.policy})


if __name__ == "__main__":
    main()
