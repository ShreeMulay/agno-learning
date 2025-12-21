"""
Example #101: Appointment Scheduler
Category: healthcare/admin
DESCRIPTION: Optimizes appointment scheduling - availability, duration, provider matching
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"appointment_type": "new_patient"}

class AppointmentSlot(BaseModel):
    date: str = Field(description="Date")
    time: str = Field(description="Time")
    provider: str = Field(description="Provider name")
    duration: int = Field(description="Duration in minutes")
    location: str = Field(description="Office location")

class SchedulingResult(BaseModel):
    patient_name: str = Field(description="Patient name")
    visit_type: str = Field(description="Type of visit")
    recommended_slots: list[AppointmentSlot] = Field(description="Available slots")
    provider_match_reason: str = Field(description="Why provider was selected")
    preparation_instructions: list[str] = Field(description="Pre-visit instructions")
    estimated_duration: int = Field(description="Expected visit length")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Appointment Scheduler",
        instructions=[
            "Match patients with appropriate providers and times",
            "Consider visit type, urgency, and provider specialization",
            "Optimize schedule utilization and minimize wait times",
            "Account for patient preferences and constraints",
            "Provide clear preparation instructions"
        ],
        output_schema=SchedulingResult, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Appointment Scheduler - Demo\n" + "=" * 60)
    query = f"""Schedule a {config['appointment_type']} appointment:
Patient: Jane Smith, new patient
Reason: Diabetes management, referred by PCP
Preferences: Afternoons preferred, needs after 3pm
Insurance: Blue Cross PPO
Available providers: Dr. Chen (endocrine), Dr. Patel (endocrine), Dr. Kim (internal med)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SchedulingResult):
        print(f"\nPatient: {result.patient_name}")
        print(f"Visit Type: {result.visit_type} ({result.estimated_duration} min)")
        print(f"\nRecommended Slots:")
        for slot in result.recommended_slots[:3]:
            print(f"  - {slot.date} at {slot.time} with {slot.provider}")
        print(f"\nProvider Match: {result.provider_match_reason}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--appointment-type", "-t", default=DEFAULT_CONFIG["appointment_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"appointment_type": args.appointment_type})

if __name__ == "__main__": main()
