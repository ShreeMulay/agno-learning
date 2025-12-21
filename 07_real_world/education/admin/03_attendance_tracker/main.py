"""
Example #123: Attendance Tracker
Category: education/admin
DESCRIPTION: Tracks and analyzes student attendance patterns
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"report_type": "monthly"}

class AttendanceReport(BaseModel):
    student_name: str = Field(description="Student name")
    period: str = Field(description="Reporting period")
    days_present: int = Field(description="Days present")
    days_absent: int = Field(description="Days absent")
    days_tardy: int = Field(description="Days tardy")
    attendance_rate: float = Field(description="Attendance percentage")
    patterns: list[str] = Field(description="Identified patterns")
    risk_level: str = Field(description="low, medium, high")
    interventions: list[str] = Field(description="Recommended interventions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Attendance Tracker",
        instructions=["Track daily attendance", "Identify concerning patterns", "Calculate attendance rates", "Recommend interventions"],
        output_schema=AttendanceReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Attendance Tracker - Demo\n" + "=" * 60)
    response = agent.run(f"Generate {config['report_type']} report: Student Maria Garcia, November: Present 15 days, Absent 5 days (3 Mondays, 2 sick), Tardy 2 days")
    result = response.content
    if isinstance(result, AttendanceReport):
        print(f"\nStudent: {result.student_name} | Period: {result.period}")
        print(f"Present: {result.days_present} | Absent: {result.days_absent} | Tardy: {result.days_tardy}")
        print(f"Rate: {result.attendance_rate}% | Risk: {result.risk_level}")
        print(f"Patterns: {', '.join(result.patterns[:2])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-type", "-t", default=DEFAULT_CONFIG["report_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"report_type": args.report_type})

if __name__ == "__main__": main()
