"""
Example #100: Clinical Notes Generator
Category: healthcare/clinical
DESCRIPTION: Generates structured clinical documentation - SOAP notes, H&Ps, progress notes
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"note_type": "progress"}

class SOAPNote(BaseModel):
    subjective: str = Field(description="Patient's reported symptoms and history")
    objective: str = Field(description="Exam findings and data")
    assessment: str = Field(description="Clinical assessment and diagnoses")
    plan: str = Field(description="Treatment plan")

class ClinicalNote(BaseModel):
    note_type: str = Field(description="progress, H&P, consult, etc.")
    chief_complaint: str = Field(description="Primary concern")
    soap: SOAPNote = Field(description="SOAP format content")
    diagnoses: list[str] = Field(description="ICD-10 ready diagnoses")
    orders: list[str] = Field(description="Orders placed")
    patient_education: str = Field(description="Education provided")
    follow_up: str = Field(description="Follow-up plan")
    time_spent: str = Field(description="Documentation of time for billing")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Clinical Notes Generator",
        instructions=[
            "Generate professional clinical documentation",
            "Use appropriate medical terminology and abbreviations",
            "Structure notes in standard SOAP format",
            "Include all elements required for billing compliance",
            "Be thorough but concise"
        ],
        output_schema=ClinicalNote, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Clinical Notes Generator - Demo\n" + "=" * 60)
    query = f"""Generate a {config['note_type']} note:

Encounter: Follow-up visit for diabetes management
Patient: 52yo F with T2DM x 5 years
Vitals: BP 138/84, HR 78, BMI 32

Subjective notes:
- Doing better with diet, lost 4 lbs
- Checking sugars - fasting 130-150s
- Some tingling in feet, bilateral
- Compliant with metformin
- Denies chest pain, SOB, vision changes

Exam findings:
- A&O, NAD
- CV: RRR, no murmurs
- Ext: no edema, DP pulses 2+, monofilament decreased toes

Labs from last week:
- A1c: 7.8% (was 8.4%)
- Cr: 0.9, UACR: 45"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ClinicalNote):
        print(f"\nNote Type: {result.note_type}")
        print(f"Chief Complaint: {result.chief_complaint}")
        print(f"\n--- SOAP NOTE ---")
        print(f"\nS: {result.soap.subjective[:200]}...")
        print(f"\nO: {result.soap.objective[:200]}...")
        print(f"\nA: {result.soap.assessment[:200]}...")
        print(f"\nP: {result.soap.plan[:200]}...")
        print(f"\nDiagnoses: {', '.join(result.diagnoses[:3])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--note-type", "-n", default=DEFAULT_CONFIG["note_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"note_type": args.note_type})

if __name__ == "__main__": main()
