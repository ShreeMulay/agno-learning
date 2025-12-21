"""
Example #107: Census Manager
Category: healthcare/admin
DESCRIPTION: Manages hospital/facility census - admissions, discharges, bed management
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"facility_type": "hospital"}

class PatientStatus(BaseModel):
    name: str = Field(description="Patient name/ID")
    unit: str = Field(description="Current unit")
    bed: str = Field(description="Bed assignment")
    status: str = Field(description="admitted, discharge_pending, transferred")
    los: int = Field(description="Length of stay in days")
    expected_discharge: str = Field(description="Expected discharge date")

class CensusReport(BaseModel):
    facility: str = Field(description="Facility name")
    report_time: str = Field(description="Report timestamp")
    total_census: int = Field(description="Total patients")
    total_capacity: int = Field(description="Total beds")
    occupancy_rate: float = Field(description="Occupancy percentage")
    admissions_today: int = Field(description="Today's admissions")
    discharges_expected: int = Field(description="Expected discharges")
    patients: list[PatientStatus] = Field(description="Patient status list")
    bottlenecks: list[str] = Field(description="Identified bottlenecks")
    recommendations: list[str] = Field(description="Flow recommendations")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Census Manager",
        instructions=[
            "Track real-time census and bed availability",
            "Identify patients ready for discharge or transfer",
            "Predict capacity needs based on admissions/discharges",
            "Flag bottlenecks affecting patient flow",
            "Recommend actions to optimize throughput"
        ],
        output_schema=CensusReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Census Manager - Demo\n" + "=" * 60)
    query = f"""Generate census report for {config['facility_type']}:
Unit data:
- ICU: 12/15 beds occupied, 2 potential transfers out
- Med/Surg: 45/50 beds, 8 discharges expected today
- Telemetry: 20/22 beds, 1 admission pending from ED
- ED: 15 patients, 5 awaiting beds
- OR: 8 cases scheduled, 3 will need ICU beds post-op"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CensusReport):
        print(f"\nFacility: {result.facility}")
        print(f"Time: {result.report_time}")
        print(f"\nCensus: {result.total_census}/{result.total_capacity} ({result.occupancy_rate:.1f}%)")
        print(f"Today: +{result.admissions_today} admissions, -{result.discharges_expected} discharges expected")
        print(f"\nBottlenecks:")
        for b in result.bottlenecks:
            print(f"  ⚠️ {b}")
        print(f"\nRecommendations:")
        for r in result.recommendations[:3]:
            print(f"  → {r}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--facility-type", "-f", default=DEFAULT_CONFIG["facility_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"facility_type": args.facility_type})

if __name__ == "__main__": main()
