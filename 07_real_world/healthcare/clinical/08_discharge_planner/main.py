"""
Example #098: Discharge Planner
Category: healthcare/clinical
DESCRIPTION: Creates comprehensive discharge plans - medications, follow-up, patient instructions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"discharge_type": "home"}

class MedicationChange(BaseModel):
    medication: str = Field(description="Drug name")
    change_type: str = Field(description="new, changed, stopped")
    instructions: str = Field(description="Specific instructions")

class DischargePlan(BaseModel):
    diagnosis: str = Field(description="Primary discharge diagnosis")
    hospital_course: str = Field(description="Brief summary of stay")
    discharge_destination: str = Field(description="Home, SNF, rehab, etc.")
    medication_changes: list[MedicationChange] = Field(description="Med changes")
    follow_up_appointments: list[str] = Field(description="Required follow-up")
    warning_signs: list[str] = Field(description="When to seek care")
    activity_restrictions: list[str] = Field(description="Activity limits")
    diet_instructions: str = Field(description="Dietary guidance")
    patient_education: list[str] = Field(description="Key teaching points")
    equipment_needs: list[str] = Field(description="DME or supplies needed")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Discharge Planner",
        instructions=[
            "Create comprehensive, patient-friendly discharge plans",
            "Clearly document all medication changes with reasons",
            "Specify follow-up appointments and timing",
            "List warning signs in plain language",
            "Consider social support and home environment"
        ],
        output_schema=DischargePlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Discharge Planner - Demo\n" + "=" * 60)
    query = f"""Create discharge plan ({config['discharge_type']}):

Patient: 72yo F admitted for CHF exacerbation
Hospital course: 4-day stay, IV diuresis, symptom improvement
Home meds adjusted:
- Furosemide increased 20mg->40mg BID
- Added metolazone 2.5mg PRN
- Stopped NSAID (was taking ibuprofen)
- K+ supplement added
Lives alone, has daughter nearby
Oxygen sat 94% on room air at rest"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DischargePlan):
        print(f"\nDiagnosis: {result.diagnosis}")
        print(f"Destination: {result.discharge_destination}")
        print(f"\nMedication Changes:")
        for m in result.medication_changes:
            print(f"  [{m.change_type.upper()}] {m.medication}")
            print(f"    {m.instructions}")
        print(f"\n⚠️ Warning Signs:")
        for w in result.warning_signs[:3]:
            print(f"  • {w}")
        print(f"\nFollow-up: {', '.join(result.follow_up_appointments[:2])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--discharge-type", "-d", default=DEFAULT_CONFIG["discharge_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"discharge_type": args.discharge_type})

if __name__ == "__main__": main()
