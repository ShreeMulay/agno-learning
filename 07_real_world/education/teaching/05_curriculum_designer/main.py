"""
Example #115: Curriculum Designer
Category: education/teaching
DESCRIPTION: Designs course curricula with scope, sequence, and learning outcomes
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"course": "introduction_to_python", "duration_weeks": 12}

class Unit(BaseModel):
    number: int = Field(description="Unit number")
    title: str = Field(description="Unit title")
    weeks: int = Field(description="Duration in weeks")
    objectives: list[str] = Field(description="Learning objectives")
    topics: list[str] = Field(description="Topics covered")
    assessment: str = Field(description="Unit assessment")

class Curriculum(BaseModel):
    course_title: str = Field(description="Course title")
    description: str = Field(description="Course description")
    target_audience: str = Field(description="Who this is for")
    prerequisites: list[str] = Field(description="Required prerequisites")
    learning_outcomes: list[str] = Field(description="Course-level outcomes")
    units: list[Unit] = Field(description="Course units")
    materials: list[str] = Field(description="Required materials")
    grading_policy: str = Field(description="How grades are determined")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Curriculum Designer",
        instructions=[
            "Design coherent, well-sequenced curricula",
            "Align units with overarching learning outcomes",
            "Build skills progressively across units",
            "Include varied assessment methods",
            "Consider pacing and student workload"
        ],
        output_schema=Curriculum, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Curriculum Designer - Demo\n" + "=" * 60)
    query = f"""Design curriculum for:
Course: {config['course']}
Duration: {config['duration_weeks']} weeks
Audience: College freshmen, no prior programming experience
Format: 3 hours/week lecture + 2 hours lab"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, Curriculum):
        print(f"\n{result.course_title}")
        print(f"Audience: {result.target_audience}")
        print(f"\nLearning Outcomes:")
        for lo in result.learning_outcomes[:3]:
            print(f"  • {lo}")
        print(f"\nUnits ({len(result.units)}):")
        for u in result.units:
            print(f"  {u.number}. {u.title} ({u.weeks} weeks)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", "-c", default=DEFAULT_CONFIG["course"])
    parser.add_argument("--duration-weeks", "-d", type=int, default=DEFAULT_CONFIG["duration_weeks"])
    args = parser.parse_args()
    run_demo(get_agent(), {"course": args.course, "duration_weeks": args.duration_weeks})

if __name__ == "__main__": main()
