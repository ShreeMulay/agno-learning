"""
Example #097: Care Coordinator
Category: healthcare/clinical
DESCRIPTION: Coordinates multi-disciplinary care - referrals, appointments, care gaps
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"patient_complexity": "high"}

class CareGap(BaseModel):
    gap_type: str = Field(description="Screening, chronic care, preventive, etc.")
    description: str = Field(description="What's missing")
    priority: str = Field(description="high, medium, low")
    due_date: str = Field(description="When needed")

class Referral(BaseModel):
    specialty: str = Field(description="Specialty needed")
    reason: str = Field(description="Referral reason")
    urgency: str = Field(description="stat, urgent, routine")
    preparation: list[str] = Field(description="Pre-referral requirements")

class CarePlan(BaseModel):
    patient_summary: str = Field(description="Brief patient summary")
    active_conditions: list[str] = Field(description="Conditions being managed")
    care_team: list[str] = Field(description="Involved providers")
    pending_referrals: list[Referral] = Field(description="Referrals needed")
    care_gaps: list[CareGap] = Field(description="Care gaps identified")
    upcoming_appointments: list[str] = Field(description="Scheduled visits")
    care_coordination_notes: str = Field(description="Coordination needs")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Care Coordinator",
        instructions=[
            "Coordinate care across multiple providers and conditions",
            "Identify care gaps and overdue screenings",
            "Prioritize referrals by urgency and clinical need",
            "Track care team members and their roles",
            "Ensure continuity and communication across settings"
        ],
        output_schema=CarePlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Care Coordinator - Demo\n" + "=" * 60)
    query = f"""Coordinate care for this {config['patient_complexity']} complexity patient:

Patient: 68yo M with multiple chronic conditions
Active problems: CHF (EF 35%), T2DM, CKD stage 3b, afib
Recent events: CHF exacerbation admission 2 weeks ago

Current care team:
- PCP: Dr. Smith (last visit 3 months ago)
- Cardiologist: Dr. Jones (saw during admission)

Outstanding items:
- No nephrology referral despite CKD progression
- Overdue for diabetic eye exam (18 months)
- No cardiac rehab after CHF admission
- A1c not checked in 6 months
- Echo ordered but not completed"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CarePlan):
        print(f"\nPatient: {result.patient_summary[:100]}...")
        print(f"Active Conditions: {', '.join(result.active_conditions)}")
        print(f"\nPending Referrals ({len(result.pending_referrals)}):")
        for r in result.pending_referrals:
            print(f"  [{r.urgency}] {r.specialty}: {r.reason}")
        print(f"\nCare Gaps ({len(result.care_gaps)}):")
        for g in result.care_gaps:
            print(f"  [{g.priority}] {g.description}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patient-complexity", "-c", default=DEFAULT_CONFIG["patient_complexity"])
    args = parser.parse_args()
    run_demo(get_agent(), {"patient_complexity": args.patient_complexity})

if __name__ == "__main__": main()
