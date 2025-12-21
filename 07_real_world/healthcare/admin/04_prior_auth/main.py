"""
Example #104: Prior Authorization Manager
Category: healthcare/admin
DESCRIPTION: Manages prior authorization requests - requirements, submissions, tracking
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"service_category": "imaging"}

class AuthRequirement(BaseModel):
    document: str = Field(description="Required document")
    status: str = Field(description="provided, missing, pending")
    notes: str = Field(description="Additional notes")

class PriorAuthRequest(BaseModel):
    patient_name: str = Field(description="Patient name")
    requested_service: str = Field(description="Service requiring auth")
    diagnosis: str = Field(description="Supporting diagnosis")
    urgency: str = Field(description="routine, urgent, emergent")
    payer: str = Field(description="Insurance payer")
    requirements: list[AuthRequirement] = Field(description="Documentation requirements")
    clinical_rationale: str = Field(description="Medical necessity statement")
    likelihood_approval: str = Field(description="high, medium, low")
    alternative_options: list[str] = Field(description="If denied, alternatives")
    submission_ready: bool = Field(description="Ready for submission")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Prior Authorization Manager",
        instructions=[
            "Determine prior authorization requirements by payer and service",
            "Compile required clinical documentation",
            "Draft compelling medical necessity statements",
            "Track authorization status and timelines",
            "Suggest alternatives if authorization is unlikely"
        ],
        output_schema=PriorAuthRequest, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Prior Authorization Manager - Demo\n" + "=" * 60)
    query = f"""Prepare prior auth request for {config['service_category']}:
Patient: Mary Wilson, 67yo F
Insurance: Aetna Medicare Advantage
Requested: MRI lumbar spine with contrast
Diagnosis: Lumbar radiculopathy (M54.16), failed 6 weeks PT
Clinical notes: Progressive weakness, failed conservative treatment
Ordering provider: Dr. Jones, Orthopedics"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PriorAuthRequest):
        print(f"\nPatient: {result.patient_name}")
        print(f"Service: {result.requested_service}")
        print(f"Urgency: {result.urgency} | Payer: {result.payer}")
        print(f"\nRequirements Status:")
        for req in result.requirements:
            status_icon = "✅" if req.status == "provided" else "❌"
            print(f"  {status_icon} {req.document}: {req.status}")
        print(f"\nApproval Likelihood: {result.likelihood_approval}")
        print(f"Submission Ready: {result.submission_ready}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-category", "-s", default=DEFAULT_CONFIG["service_category"])
    args = parser.parse_args()
    run_demo(get_agent(), {"service_category": args.service_category})

if __name__ == "__main__": main()
