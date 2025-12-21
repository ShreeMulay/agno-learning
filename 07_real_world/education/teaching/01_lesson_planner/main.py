"""
Example #111: Lesson Planner
Category: education/teaching
DESCRIPTION: Creates structured lesson plans with objectives, activities, and assessments
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"subject": "mathematics", "grade_level": "8"}

class Activity(BaseModel):
    name: str = Field(description="Activity name")
    duration: int = Field(description="Duration in minutes")
    description: str = Field(description="Activity description")
    materials: list[str] = Field(description="Required materials")

class LessonPlan(BaseModel):
    title: str = Field(description="Lesson title")
    subject: str = Field(description="Subject area")
    grade_level: str = Field(description="Grade level")
    duration: int = Field(description="Total duration in minutes")
    objectives: list[str] = Field(description="Learning objectives")
    standards: list[str] = Field(description="Aligned standards")
    activities: list[Activity] = Field(description="Lesson activities")
    assessment: str = Field(description="How to assess understanding")
    differentiation: list[str] = Field(description="Differentiation strategies")
    homework: str = Field(description="Homework assignment")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Lesson Planner",
        instructions=[
            "Create engaging, standards-aligned lesson plans",
            "Include clear learning objectives and success criteria",
            "Design varied activities for different learning styles",
            "Incorporate formative assessment throughout",
            "Provide differentiation for diverse learners"
        ],
        output_schema=LessonPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Lesson Planner - Demo\n" + "=" * 60)
    query = f"""Create a lesson plan:
Subject: {config['subject']}
Grade: {config['grade_level']}
Topic: Introduction to linear equations
Duration: 50 minutes
Context: Students have learned variables and basic algebra"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, LessonPlan):
        print(f"\n{result.title}")
        print(f"Subject: {result.subject} | Grade: {result.grade_level} | Duration: {result.duration} min")
        print(f"\nObjectives:")
        for obj in result.objectives:
            print(f"  • {obj}")
        print(f"\nActivities ({len(result.activities)}):")
        for act in result.activities:
            print(f"  - {act.name} ({act.duration} min)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", "-s", default=DEFAULT_CONFIG["subject"])
    parser.add_argument("--grade-level", "-g", default=DEFAULT_CONFIG["grade_level"])
    args = parser.parse_args()
    run_demo(get_agent(), {"subject": args.subject, "grade_level": args.grade_level})

if __name__ == "__main__": main()
