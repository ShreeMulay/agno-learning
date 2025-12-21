"""
Example #108: Quality Reporter
Category: healthcare/admin
DESCRIPTION: Generates quality metrics reports - HEDIS, MIPS, patient outcomes
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"measure_set": "HEDIS"}

class QualityMeasure(BaseModel):
    measure_id: str = Field(description="Measure identifier")
    measure_name: str = Field(description="Measure name")
    numerator: int = Field(description="Patients meeting criteria")
    denominator: int = Field(description="Eligible patients")
    rate: float = Field(description="Performance rate")
    benchmark: float = Field(description="Target benchmark")
    status: str = Field(description="above, at, below benchmark")

class QualityReport(BaseModel):
    report_period: str = Field(description="Reporting period")
    measure_set: str = Field(description="HEDIS, MIPS, etc.")
    measures: list[QualityMeasure] = Field(description="Quality measures")
    overall_score: float = Field(description="Composite score")
    improvement_areas: list[str] = Field(description="Areas needing improvement")
    action_plans: list[str] = Field(description="Recommended actions")
    patients_needing_outreach: int = Field(description="Patients with care gaps")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Quality Reporter",
        instructions=[
            "Calculate quality metrics per standard definitions",
            "Compare performance against benchmarks",
            "Identify gaps and improvement opportunities",
            "Recommend specific interventions",
            "Prioritize by impact and feasibility"
        ],
        output_schema=QualityReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Quality Reporter - Demo\n" + "=" * 60)
    query = f"""Generate {config['measure_set']} quality report:
Practice: Valley Family Medicine
Period: 2024
Patient panel: 2,500 Medicare patients

Current data:
- Diabetes A1c control (<8%): 412/520 patients
- Breast cancer screening: 280/350 eligible women
- Colorectal cancer screening: 390/480 eligible patients
- BP control (<140/90): 680/820 patients with HTN
- Statin therapy for CVD: 245/290 patients"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, QualityReport):
        print(f"\nReport Period: {result.report_period}")
        print(f"Measure Set: {result.measure_set}")
        print(f"Overall Score: {result.overall_score:.1f}%")
        print(f"\nMeasures ({len(result.measures)}):")
        for m in result.measures:
            status_icon = "✅" if m.status == "above" else "⚠️" if m.status == "at" else "❌"
            print(f"  {status_icon} {m.measure_name}: {m.rate:.1f}% (target: {m.benchmark:.1f}%)")
        print(f"\nPatients Needing Outreach: {result.patients_needing_outreach}")
        print(f"\nAction Plans:")
        for action in result.action_plans[:3]:
            print(f"  → {action}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--measure-set", "-m", default=DEFAULT_CONFIG["measure_set"])
    args = parser.parse_args()
    run_demo(get_agent(), {"measure_set": args.measure_set})

if __name__ == "__main__": main()
