"""
Example #091: Patient Intake Assistant
Category: healthcare/clinical
DESCRIPTION: Guides patient intake - demographics, chief complaint, medical history collection
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"visit_type": "new_patient"}

class PatientDemographics(BaseModel):
    age: int = Field(description="Patient age")
    sex: str = Field(description="Biological sex")
    height: str = Field(description="Height")
    weight: str = Field(description="Weight")

class IntakeForm(BaseModel):
    chief_complaint: str = Field(description="Primary reason for visit")
    history_present_illness: str = Field(description="HPI narrative")
    past_medical_history: list[str] = Field(description="PMH conditions")
    medications: list[str] = Field(description="Current medications")
    allergies: list[str] = Field(description="Known allergies")
    family_history: list[str] = Field(description="Relevant family history")
    social_history: str = Field(description="Smoking, alcohol, occupation")
    review_of_systems: dict[str, str] = Field(description="ROS by system")
    questions_for_provider: list[str] = Field(description="Patient questions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Patient Intake Assistant",
        instructions=[
            "Guide patient through comprehensive intake process",
            "Collect demographics, chief complaint, and HPI",
            "Document past medical history, medications, and allergies",
            "Perform systematic review of systems",
            "Use patient-friendly language, avoid medical jargon"
        ],
        output_schema=IntakeForm, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Patient Intake Assistant - Demo\n" + "=" * 60)
    query = f"""Process this intake for a {config['visit_type']} visit:

Patient: 58-year-old male
Chief complaint: Chest pain for 2 days
Notes from patient:
- Pain is sharp, left side, worse with deep breath
- Started after lifting heavy boxes
- Takes lisinopril for blood pressure
- Had appendectomy 20 years ago
- Father had heart attack at 65
- Smokes half pack/day, drinks socially
- Works in construction"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, IntakeForm):
        print(f"\nChief Complaint: {result.chief_complaint}")
        print(f"\nHPI: {result.history_present_illness[:200]}...")
        print(f"\nPMH: {', '.join(result.past_medical_history)}")
        print(f"Medications: {', '.join(result.medications)}")
        print(f"Allergies: {', '.join(result.allergies) or 'NKDA'}")
        print(f"\nPatient Questions: {len(result.questions_for_provider)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--visit-type", "-v", default=DEFAULT_CONFIG["visit_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"visit_type": args.visit_type})

if __name__ == "__main__": main()
