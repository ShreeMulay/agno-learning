"""
Example #094: Treatment Planner
Category: healthcare/clinical
DESCRIPTION: Develops evidence-based treatment plans considering patient factors
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"condition": "hypertension"}

class TreatmentOption(BaseModel):
    intervention: str = Field(description="Treatment name")
    type: str = Field(description="medication, procedure, lifestyle, etc.")
    evidence_level: str = Field(description="Grade A/B/C or guideline source")
    rationale: str = Field(description="Why appropriate for this patient")
    considerations: list[str] = Field(description="Patient-specific factors")

class TreatmentPlan(BaseModel):
    diagnosis: str = Field(description="Condition being treated")
    goals: list[str] = Field(description="Treatment goals")
    first_line: list[TreatmentOption] = Field(description="First-line options")
    alternatives: list[TreatmentOption] = Field(description="Alternative options")
    monitoring: list[str] = Field(description="Parameters to monitor")
    patient_education: list[str] = Field(description="Key education points")
    follow_up: str = Field(description="Follow-up plan")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Treatment Planner",
        instructions=[
            "Develop evidence-based treatment plans per guidelines",
            "Consider patient-specific factors (age, comorbidities, preferences)",
            "Provide first-line and alternative options",
            "Include monitoring parameters and follow-up",
            "Generate patient education points"
        ],
        output_schema=TreatmentPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Treatment Planner - Demo\n" + "=" * 60)
    query = f"""Develop treatment plan for {config['condition']}:

Patient: 62yo F with newly diagnosed Stage 2 hypertension (158/94)
Comorbidities: Type 2 diabetes, mild CKD (eGFR 58)
Current meds: Metformin 1000mg BID
Allergies: ACE inhibitors (cough)
Preferences: Prefers once-daily dosing, cost-conscious"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, TreatmentPlan):
        print(f"\nDiagnosis: {result.diagnosis}")
        print(f"Goals: {', '.join(result.goals)}")
        print(f"\nFirst-Line Options:")
        for t in result.first_line:
            print(f"  - {t.intervention} ({t.evidence_level})")
            print(f"    {t.rationale[:80]}...")
        print(f"\nMonitoring: {', '.join(result.monitoring[:3])}")
        print(f"Follow-up: {result.follow_up}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", "-c", default=DEFAULT_CONFIG["condition"])
    args = parser.parse_args()
    run_demo(get_agent(), {"condition": args.condition})

if __name__ == "__main__": main()
