"""
Example #127: Student Advisor
Category: education/admin
DESCRIPTION: Provides academic advising and course recommendations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"advising_type": "course_selection"}

class CourseRecommendation(BaseModel):
    course: str = Field(description="Course name")
    reason: str = Field(description="Why recommended")
    priority: str = Field(description="required, recommended, optional")

class AdvisingResult(BaseModel):
    student_name: str = Field(description="Student name")
    current_status: str = Field(description="Academic standing")
    gpa: float = Field(description="Current GPA")
    recommendations: list[CourseRecommendation] = Field(description="Course recommendations")
    graduation_progress: str = Field(description="Progress to graduation")
    concerns: list[str] = Field(description="Academic concerns")
    next_meeting: str = Field(description="Follow-up recommendation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Student Advisor",
        instructions=["Review academic progress", "Recommend appropriate courses", "Identify concerns early", "Support student goals"],
        output_schema=AdvisingResult, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Student Advisor - Demo\n" + "=" * 60)
    response = agent.run(f"Advise on {config['advising_type']}: Junior, GPA 3.2, completed core requirements, interested in pre-med, needs to complete 2 science electives")
    result = response.content
    if isinstance(result, AdvisingResult):
        print(f"\nStudent: {result.student_name} | GPA: {result.gpa}")
        print(f"Status: {result.current_status} | Progress: {result.graduation_progress}")
        print(f"\nRecommendations:")
        for r in result.recommendations[:3]:
            print(f"  [{r.priority}] {r.course}: {r.reason[:50]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--advising-type", "-t", default=DEFAULT_CONFIG["advising_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"advising_type": args.advising_type})

if __name__ == "__main__": main()
