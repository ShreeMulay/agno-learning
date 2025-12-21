"""
Example #130: Compliance Reporter
Category: education/admin
DESCRIPTION: Generates education compliance and regulatory reports
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"report_type": "title_ix"}

class ComplianceItem(BaseModel):
    requirement: str = Field(description="Compliance requirement")
    status: str = Field(description="compliant, non_compliant, in_progress")
    evidence: str = Field(description="Supporting documentation")
    action_needed: str = Field(description="Required action if any")

class ComplianceReport(BaseModel):
    institution: str = Field(description="Institution name")
    report_type: str = Field(description="Type of compliance report")
    reporting_period: str = Field(description="Period covered")
    items: list[ComplianceItem] = Field(description="Compliance items")
    overall_status: str = Field(description="Overall compliance status")
    risk_areas: list[str] = Field(description="Areas of concern")
    remediation_plan: list[str] = Field(description="Remediation steps")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Compliance Reporter",
        instructions=["Assess regulatory compliance", "Document evidence thoroughly", "Identify risk areas", "Recommend remediation"],
        output_schema=ComplianceReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Compliance Reporter - Demo\n" + "=" * 60)
    response = agent.run(f"Generate {config['report_type']} report: Valley University, reviewing grievance procedures, training records, incident reports, policy documentation")
    result = response.content
    if isinstance(result, ComplianceReport):
        print(f"\nInstitution: {result.institution} | Report: {result.report_type}")
        print(f"Period: {result.reporting_period} | Status: {result.overall_status}")
        print(f"\nCompliance Items:")
        for item in result.items[:3]:
            print(f"  [{item.status}] {item.requirement}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-type", "-t", default=DEFAULT_CONFIG["report_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"report_type": args.report_type})

if __name__ == "__main__": main()
