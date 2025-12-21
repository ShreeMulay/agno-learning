"""
Example #106: Medical Billing Coder
Category: healthcare/admin
DESCRIPTION: Assigns appropriate CPT, ICD-10, and HCPCS codes from clinical documentation
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"encounter_type": "office_visit"}

class CodeAssignment(BaseModel):
    code: str = Field(description="CPT/ICD-10/HCPCS code")
    description: str = Field(description="Code description")
    code_type: str = Field(description="CPT, ICD-10, HCPCS")
    rationale: str = Field(description="Why this code applies")
    modifier: str = Field(description="Modifier if applicable")

class CodingResult(BaseModel):
    encounter_date: str = Field(description="Date of service")
    encounter_type: str = Field(description="Type of encounter")
    procedure_codes: list[CodeAssignment] = Field(description="CPT/HCPCS codes")
    diagnosis_codes: list[CodeAssignment] = Field(description="ICD-10 codes")
    primary_diagnosis: str = Field(description="Primary diagnosis code")
    coding_notes: list[str] = Field(description="Documentation notes")
    query_opportunities: list[str] = Field(description="Possible physician queries")
    estimated_rvu: float = Field(description="Total RVUs")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Medical Billing Coder",
        instructions=[
            "Assign accurate CPT/HCPCS codes based on documentation",
            "Select ICD-10 codes to highest specificity supported",
            "Ensure code linkage supports medical necessity",
            "Identify documentation improvement opportunities",
            "Follow coding guidelines and payer requirements"
        ],
        output_schema=CodingResult, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Medical Billing Coder - Demo\n" + "=" * 60)
    query = f"""Code this {config['encounter_type']}:
Provider: Dr. Martinez, Family Medicine
Date: 12/18/2024
Documentation:
- Established patient, 55yo M
- Chief complaint: Cough x 2 weeks, productive
- Detailed history, detailed exam
- Moderate complexity decision making
- Ordered chest X-ray, prescribed antibiotics
- Diagnoses: Acute bronchitis, Type 2 diabetes (controlled), HTN
- Time: 25 minutes total, 20 minutes face-to-face"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CodingResult):
        print(f"\nEncounter: {result.encounter_type} ({result.encounter_date})")
        print(f"Estimated RVUs: {result.estimated_rvu}")
        print(f"\nProcedure Codes:")
        for code in result.procedure_codes:
            print(f"  {code.code}: {code.description}")
        print(f"\nDiagnosis Codes (Primary: {result.primary_diagnosis}):")
        for code in result.diagnosis_codes:
            print(f"  {code.code}: {code.description}")
        if result.query_opportunities:
            print(f"\nQuery Opportunities: {', '.join(result.query_opportunities)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--encounter-type", "-e", default=DEFAULT_CONFIG["encounter_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"encounter_type": args.encounter_type})

if __name__ == "__main__": main()
