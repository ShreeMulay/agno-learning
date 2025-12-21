"""
Example #102: Insurance Verifier
Category: healthcare/admin
DESCRIPTION: Verifies insurance eligibility and benefits for patient visits
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"service_type": "office_visit"}

class CoverageDetails(BaseModel):
    covered: bool = Field(description="Is service covered")
    copay: str = Field(description="Patient copay amount")
    deductible_remaining: str = Field(description="Remaining deductible")
    coinsurance: str = Field(description="Coinsurance percentage")
    notes: str = Field(description="Coverage notes")

class InsuranceVerification(BaseModel):
    patient_name: str = Field(description="Patient name")
    insurance_plan: str = Field(description="Plan name")
    member_id: str = Field(description="Member ID")
    effective_date: str = Field(description="Coverage start")
    eligibility_status: str = Field(description="active, inactive, pending")
    coverage: CoverageDetails = Field(description="Coverage details")
    prior_auth_required: bool = Field(description="Prior auth needed")
    network_status: str = Field(description="in-network, out-of-network")
    verification_notes: list[str] = Field(description="Important notes")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Insurance Verifier",
        instructions=[
            "Verify insurance eligibility and active coverage",
            "Determine benefits for specific service types",
            "Calculate patient responsibility (copay, deductible, coinsurance)",
            "Check prior authorization requirements",
            "Identify network status and any coverage limitations"
        ],
        output_schema=InsuranceVerification, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Insurance Verifier - Demo\n" + "=" * 60)
    query = f"""Verify insurance for {config['service_type']}:
Patient: Robert Johnson
DOB: 03/15/1965
Insurance: United Healthcare Choice Plus
Member ID: UHC987654321
Group: ACME Corp
Service: Specialist office visit with procedure (echocardiogram)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, InsuranceVerification):
        print(f"\nPatient: {result.patient_name}")
        print(f"Plan: {result.insurance_plan}")
        print(f"Status: {result.eligibility_status} | Network: {result.network_status}")
        print(f"\nCoverage:")
        print(f"  Covered: {result.coverage.covered}")
        print(f"  Copay: {result.coverage.copay}")
        print(f"  Deductible Remaining: {result.coverage.deductible_remaining}")
        print(f"  Prior Auth Required: {result.prior_auth_required}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-type", "-s", default=DEFAULT_CONFIG["service_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"service_type": args.service_type})

if __name__ == "__main__": main()
