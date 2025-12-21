"""
Example #126: Accreditation Manager
Category: education/admin
DESCRIPTION: Manages accreditation requirements and documentation
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"accreditation_body": "regional"}

class StandardStatus(BaseModel):
    standard: str = Field(description="Standard name")
    status: str = Field(description="met, partial, not_met")
    evidence: list[str] = Field(description="Supporting evidence")
    gaps: list[str] = Field(description="Gaps to address")

class AccreditationReport(BaseModel):
    institution: str = Field(description="Institution name")
    accreditation_body: str = Field(description="Accrediting body")
    standards: list[StandardStatus] = Field(description="Standard compliance")
    overall_status: str = Field(description="ready, needs_work, at_risk")
    action_plan: list[str] = Field(description="Action items")
    timeline: str = Field(description="Review timeline")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Accreditation Manager",
        instructions=["Assess compliance with standards", "Identify documentation gaps", "Create action plans", "Track progress"],
        output_schema=AccreditationReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Accreditation Manager - Demo\n" + "=" * 60)
    response = agent.run(f"Assess {config['accreditation_body']} accreditation: Westbrook High, standards: Governance (documented), Curriculum (needs update), Assessment (partial data), Resources (adequate)")
    result = response.content
    if isinstance(result, AccreditationReport):
        print(f"\nInstitution: {result.institution} | Body: {result.accreditation_body}")
        print(f"Status: {result.overall_status}")
        for s in result.standards[:3]:
            print(f"  [{s.status}] {s.standard}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--accreditation-body", "-b", default=DEFAULT_CONFIG["accreditation_body"])
    args = parser.parse_args()
    run_demo(get_agent(), {"accreditation_body": args.accreditation_body})

if __name__ == "__main__": main()
