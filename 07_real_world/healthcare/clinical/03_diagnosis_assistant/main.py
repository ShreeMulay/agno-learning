"""
Example #093: Diagnosis Assistant
Category: healthcare/clinical
DESCRIPTION: Supports clinical decision-making with differential diagnosis and evidence
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"specialty": "internal_medicine"}

class DiagnosticEvidence(BaseModel):
    finding: str = Field(description="Clinical finding")
    supports: list[str] = Field(description="Conditions this supports")
    against: list[str] = Field(description="Conditions this argues against")

class DifferentialItem(BaseModel):
    diagnosis: str = Field(description="Diagnosis name")
    probability: str = Field(description="Probability estimate")
    supporting_evidence: list[str] = Field(description="Evidence for")
    against_evidence: list[str] = Field(description="Evidence against")
    next_steps: list[str] = Field(description="Tests to confirm/rule out")

class DiagnosticAssessment(BaseModel):
    clinical_summary: str = Field(description="Case summary")
    differential: list[DifferentialItem] = Field(description="Ranked differential")
    critical_diagnoses: list[str] = Field(description="Must-not-miss diagnoses")
    recommended_workup: list[str] = Field(description="Diagnostic tests")
    clinical_pearls: list[str] = Field(description="Teaching points")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Diagnosis Assistant",
        instructions=[
            "Analyze clinical presentation systematically",
            "Generate ranked differential diagnosis with probabilities",
            "Identify critical must-not-miss diagnoses",
            "Recommend appropriate diagnostic workup",
            "Provide clinical reasoning and teaching pearls"
        ],
        output_schema=DiagnosticAssessment, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Diagnosis Assistant - Demo\n" + "=" * 60)
    query = f"""Clinical case ({config['specialty']}):

45yo M presents with:
- 2 weeks progressive fatigue
- Unintentional 10lb weight loss
- Night sweats
- Enlarged lymph nodes (cervical, axillary)
- No fever, no recent infections
- Labs: mild anemia, elevated LDH, low albumin
- CXR: mediastinal widening"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DiagnosticAssessment):
        print(f"\nSummary: {result.clinical_summary[:200]}...")
        print(f"\n⚠️ Critical Diagnoses: {', '.join(result.critical_diagnoses)}")
        print(f"\nDifferential ({len(result.differential)}):")
        for d in result.differential[:3]:
            print(f"  {d.probability}: {d.diagnosis}")
            print(f"    Next: {', '.join(d.next_steps[:2])}")
        print(f"\nWorkup: {', '.join(result.recommended_workup[:4])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--specialty", "-s", default=DEFAULT_CONFIG["specialty"])
    args = parser.parse_args()
    run_demo(get_agent(), {"specialty": args.specialty})

if __name__ == "__main__": main()
