"""
Example #095: Medication Reviewer
Category: healthcare/clinical
DESCRIPTION: Reviews medication lists for interactions, duplications, and appropriateness
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"review_type": "comprehensive"}

class DrugInteraction(BaseModel):
    drugs: list[str] = Field(description="Interacting drugs")
    severity: str = Field(description="major, moderate, minor")
    effect: str = Field(description="Clinical effect")
    recommendation: str = Field(description="Action to take")

class MedicationIssue(BaseModel):
    medication: str = Field(description="Drug name")
    issue_type: str = Field(description="interaction, duplicate, inappropriate, etc.")
    details: str = Field(description="Issue details")
    recommendation: str = Field(description="Suggested action")

class MedicationReview(BaseModel):
    total_medications: int = Field(description="Number reviewed")
    interactions: list[DrugInteraction] = Field(description="Drug interactions")
    issues: list[MedicationIssue] = Field(description="Other issues")
    duplications: list[str] = Field(description="Therapeutic duplications")
    deprescribing_candidates: list[str] = Field(description="Consider stopping")
    optimization_suggestions: list[str] = Field(description="Optimization opportunities")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Medication Reviewer",
        instructions=[
            "Review complete medication list for safety issues",
            "Identify drug-drug interactions by severity",
            "Flag therapeutic duplications and inappropriate medications",
            "Consider patient factors (age, renal function, etc.)",
            "Suggest deprescribing and optimization opportunities"
        ],
        output_schema=MedicationReview, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Medication Reviewer - Demo\n" + "=" * 60)
    query = f"""Perform {config['review_type']} medication review:

Patient: 78yo M, CKD stage 4 (eGFR 22), CHF, afib, T2DM
Medications:
1. Metformin 1000mg BID
2. Lisinopril 20mg daily
3. Carvedilol 25mg BID
4. Warfarin 5mg daily
5. Aspirin 81mg daily
6. Omeprazole 40mg daily
7. Ibuprofen 400mg PRN (patient takes daily for arthritis)
8. Gabapentin 300mg TID
9. Atorvastatin 40mg daily
10. Furosemide 40mg BID"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, MedicationReview):
        print(f"\nMedications Reviewed: {result.total_medications}")
        print(f"\n⚠️ Interactions ({len(result.interactions)}):")
        for i in result.interactions:
            print(f"  [{i.severity.upper()}] {' + '.join(i.drugs)}")
            print(f"    Effect: {i.effect}")
        print(f"\nIssues ({len(result.issues)}):")
        for issue in result.issues[:3]:
            print(f"  - {issue.medication}: {issue.issue_type}")
        print(f"\nDeprescribing Candidates: {', '.join(result.deprescribing_candidates)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-type", "-r", default=DEFAULT_CONFIG["review_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"review_type": args.review_type})

if __name__ == "__main__": main()
