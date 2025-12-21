"""
Example #103: Claims Processor
Category: healthcare/admin
DESCRIPTION: Processes and validates healthcare claims for submission
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"claim_type": "professional"}

class ClaimLine(BaseModel):
    line_number: int = Field(description="Line number")
    cpt_code: str = Field(description="CPT/HCPCS code")
    diagnosis_codes: list[str] = Field(description="Linked ICD-10 codes")
    units: int = Field(description="Service units")
    charge: float = Field(description="Billed amount")
    modifier: str = Field(description="Modifier if applicable")

class ClaimValidation(BaseModel):
    claim_id: str = Field(description="Claim identifier")
    claim_type: str = Field(description="Professional, institutional, etc.")
    lines: list[ClaimLine] = Field(description="Claim lines")
    total_charges: float = Field(description="Total billed")
    validation_status: str = Field(description="valid, errors, warnings")
    errors: list[str] = Field(description="Validation errors")
    warnings: list[str] = Field(description="Validation warnings")
    suggestions: list[str] = Field(description="Optimization suggestions")
    ready_to_submit: bool = Field(description="Can submit to payer")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Claims Processor",
        instructions=[
            "Validate healthcare claims for completeness and accuracy",
            "Check CPT/ICD-10 code combinations for medical necessity",
            "Identify bundling issues and modifier requirements",
            "Ensure compliance with payer-specific rules",
            "Optimize claims for maximum appropriate reimbursement"
        ],
        output_schema=ClaimValidation, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Claims Processor - Demo\n" + "=" * 60)
    query = f"""Process this {config['claim_type']} claim:
Provider: Dr. Smith, Cardiology
Patient: Medicare beneficiary
Date of Service: 12/15/2024
Services:
- 99214 (Office visit, established) - $150
- 93000 (EKG) - $75
- 93306 (Echocardiogram complete) - $450
Diagnoses: I25.10 (CAD), I10 (HTN), R00.0 (Tachycardia)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ClaimValidation):
        print(f"\nClaim ID: {result.claim_id}")
        print(f"Type: {result.claim_type}")
        print(f"Total Charges: ${result.total_charges:,.2f}")
        print(f"Status: {result.validation_status}")
        print(f"\nLines ({len(result.lines)}):")
        for line in result.lines:
            print(f"  {line.cpt_code}: ${line.charge} (DX: {', '.join(line.diagnosis_codes[:2])})")
        if result.errors:
            print(f"\n❌ Errors: {', '.join(result.errors)}")
        if result.warnings:
            print(f"\n⚠️ Warnings: {', '.join(result.warnings)}")
        print(f"\nReady to Submit: {result.ready_to_submit}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-type", "-t", default=DEFAULT_CONFIG["claim_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"claim_type": args.claim_type})

if __name__ == "__main__": main()
