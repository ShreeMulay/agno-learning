"""
Example #099: Follow-up Scheduler
Category: healthcare/clinical
DESCRIPTION: Schedules and tracks follow-up appointments based on clinical needs
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"scheduling_mode": "post_discharge"}

class FollowUpAppointment(BaseModel):
    provider_type: str = Field(description="PCP, specialist, etc.")
    reason: str = Field(description="Purpose of visit")
    timing: str = Field(description="Within X days/weeks")
    priority: str = Field(description="critical, important, routine")
    preparation: list[str] = Field(description="Pre-visit requirements")

class SchedulingPlan(BaseModel):
    patient_context: str = Field(description="Relevant clinical context")
    appointments: list[FollowUpAppointment] = Field(description="Required appointments")
    labs_before_visits: list[str] = Field(description="Labs needed before appointments")
    imaging_needed: list[str] = Field(description="Imaging studies needed")
    barriers_identified: list[str] = Field(description="Potential scheduling barriers")
    patient_instructions: str = Field(description="Instructions for patient")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Follow-up Scheduler",
        instructions=[
            "Determine appropriate follow-up based on clinical condition",
            "Prioritize appointments by clinical urgency",
            "Sequence appointments logically (labs before visits)",
            "Identify barriers to scheduling (transportation, insurance)",
            "Provide clear timing expectations"
        ],
        output_schema=SchedulingPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Follow-up Scheduler - Demo\n" + "=" * 60)
    query = f"""Plan follow-up ({config['scheduling_mode']}):

Patient: 58yo M discharged after NSTEMI
Procedures: Cardiac cath with 2 stents to LAD
New medications: DAPT (aspirin + ticagrelor), high-intensity statin, beta-blocker, ACEi
Comorbidities: T2DM (A1c 8.2%), HTN, hyperlipidemia
Social: Works full-time, limited PTO, no car (uses public transit)
PCP: Dr. Smith (hasn't seen in 8 months)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SchedulingPlan):
        print(f"\nContext: {result.patient_context[:150]}...")
        print(f"\nAppointments ({len(result.appointments)}):")
        for a in result.appointments:
            print(f"  [{a.priority}] {a.provider_type}: {a.timing}")
            print(f"    Reason: {a.reason}")
        print(f"\nPre-visit Labs: {', '.join(result.labs_before_visits[:3])}")
        print(f"\nBarriers: {', '.join(result.barriers_identified)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scheduling-mode", "-m", default=DEFAULT_CONFIG["scheduling_mode"])
    args = parser.parse_args()
    run_demo(get_agent(), {"scheduling_mode": args.scheduling_mode})

if __name__ == "__main__": main()
