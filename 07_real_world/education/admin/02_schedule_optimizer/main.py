"""
Example #122: Schedule Optimizer
Category: education/admin
DESCRIPTION: Optimizes class schedules for students and teachers
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"optimization_goal": "minimize_conflicts"}

class ScheduleBlock(BaseModel):
    period: int = Field(description="Period number")
    course: str = Field(description="Course name")
    teacher: str = Field(description="Teacher name")
    room: str = Field(description="Room number")

class OptimizedSchedule(BaseModel):
    student_name: str = Field(description="Student name")
    schedule: list[ScheduleBlock] = Field(description="Weekly schedule")
    conflicts_resolved: int = Field(description="Conflicts resolved")
    utilization_rate: float = Field(description="Room utilization %")
    recommendations: list[str] = Field(description="Optimization suggestions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Schedule Optimizer",
        instructions=["Optimize schedules to minimize conflicts", "Balance teacher loads", "Maximize room utilization", "Consider student preferences"],
        output_schema=OptimizedSchedule, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Schedule Optimizer - Demo\n" + "=" * 60)
    response = agent.run(f"Optimize schedule ({config['optimization_goal']}): Student needs Algebra, English, Science, History, PE, Art. Constraints: PE must be periods 1-3, Art only offered period 6")
    result = response.content
    if isinstance(result, OptimizedSchedule):
        print(f"\nStudent: {result.student_name}")
        print(f"Conflicts Resolved: {result.conflicts_resolved} | Utilization: {result.utilization_rate}%")
        for block in result.schedule[:4]:
            print(f"  Period {block.period}: {block.course} - {block.room}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimization-goal", "-g", default=DEFAULT_CONFIG["optimization_goal"])
    args = parser.parse_args()
    run_demo(get_agent(), {"optimization_goal": args.optimization_goal})

if __name__ == "__main__": main()
