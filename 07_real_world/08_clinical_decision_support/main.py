#!/usr/bin/env python3
"""Example 08: Clinical Decision Support - Medical knowledge agent.

A domain-specific agent for clinical information (educational only).

Run with:
    python main.py "What are the first-line treatments for hypertension?"

DISCLAIMER: This is for educational purposes only. Always consult
healthcare professionals for medical decisions.
"""

import argparse
import sys
from pathlib import Path
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


class ClinicalEvidence(BaseModel):
    """Evidence for a clinical recommendation."""
    source: str = Field(description="Source of evidence")
    strength: str = Field(description="Evidence strength: strong, moderate, weak")
    summary: str = Field(description="Evidence summary")


class ClinicalResponse(BaseModel):
    """Structured clinical decision support response."""
    condition: str = Field(description="Medical condition addressed")
    summary: str = Field(description="Clinical summary")
    recommendations: list[str] = Field(description="Clinical recommendations")
    evidence: list[ClinicalEvidence] = Field(description="Supporting evidence")
    considerations: list[str] = Field(description="Special considerations")
    when_to_refer: list[str] = Field(description="Referral indicators")
    disclaimer: str = Field(description="Medical disclaimer")


# Sample medical knowledge (in real app, this would be a proper knowledge base)
MEDICAL_KNOWLEDGE = """
## Hypertension Management Guidelines

### First-Line Treatments
1. ACE Inhibitors (e.g., lisinopril, enalapril)
2. ARBs (e.g., losartan, valsartan)
3. Calcium Channel Blockers (e.g., amlodipine)
4. Thiazide Diuretics (e.g., hydrochlorothiazide)

### Evidence Level: Strong (ACC/AHA 2017 Guidelines)

### Special Populations
- Diabetes: ACE inhibitors or ARBs preferred
- African American: CCBs or thiazides often first choice
- Heart Failure: ACE inhibitors, ARBs, or specific beta-blockers

### Lifestyle Modifications (All Patients)
- DASH diet
- Sodium restriction (<2.3g/day)
- Regular exercise (150 min/week)
- Weight management
- Limit alcohol
"""


def create_clinical_agent(model):
    """Create a clinical decision support agent."""
    
    return Agent(
        name="ClinicalAdvisor",
        model=model,
        instructions=[
            "You are a clinical decision support assistant.",
            "Provide evidence-based medical information.",
            "Always cite sources and evidence strength.",
            "Include appropriate disclaimers.",
            "Mention when to seek specialist consultation.",
            "",
            "IMPORTANT: Remind users this is for educational purposes only.",
            "Real clinical decisions require healthcare professionals.",
            "",
            f"Reference Knowledge:\n{MEDICAL_KNOWLEDGE}",
        ],
        markdown=True,
    )



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_clinical_agent(model)


def main():
    parser = argparse.ArgumentParser(description="Clinical Decision Support")
    add_model_args(parser)
    parser.add_argument(
        "query", type=str, nargs="?",
        default="What are the first-line treatments for hypertension?",
        help="Clinical question"
    )
    args = parser.parse_args()

    print_header("Clinical Decision Support")
    
    print("=" * 60)
    print("  DISCLAIMER: Educational purposes only.")
    print("  Not for real clinical decision-making.")
    print("  Always consult healthcare professionals.")
    print("=" * 60)
    print()
    
    print_section("Query")
    print(f"  {args.query}")
    print()
    
    model = get_model(args.provider, args.model, temperature=0.3)  # Lower temp for medical
    agent = create_clinical_agent(model)
    
    print_section("Processing...")
    response = agent.run(args.query, output_schema=ClinicalResponse)
    result = response.content
    
    print_section(f"Condition: {result.condition}")
    print(f"\n  {result.summary}")
    
    print_section("Recommendations")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"  {i}. {rec}")
    
    print_section("Evidence")
    for evidence in result.evidence:
        strength_icon = "🟢" if evidence.strength == "strong" else "🟡" if evidence.strength == "moderate" else "🔴"
        print(f"\n  {strength_icon} {evidence.source}")
        print(f"     Strength: {evidence.strength}")
        print(f"     {evidence.summary}")
    
    print_section("Special Considerations")
    for consideration in result.considerations:
        print(f"  • {consideration}")
    
    print_section("When to Refer")
    for indicator in result.when_to_refer:
        print(f"  ⚠️  {indicator}")
    
    print_section("Disclaimer")
    print(f"  {result.disclaimer}")


if __name__ == "__main__":
    main()
