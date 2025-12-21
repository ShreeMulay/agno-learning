"""
Example #113: Grading Assistant
Category: education/teaching
DESCRIPTION: Assists with grading assignments using rubrics and providing feedback
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"assignment_type": "essay"}

class RubricScore(BaseModel):
    criterion: str = Field(description="Rubric criterion")
    score: int = Field(description="Score achieved")
    max_score: int = Field(description="Maximum possible")
    feedback: str = Field(description="Specific feedback")

class GradingResult(BaseModel):
    student_id: str = Field(description="Student identifier")
    assignment: str = Field(description="Assignment name")
    rubric_scores: list[RubricScore] = Field(description="Scores by criterion")
    total_score: int = Field(description="Total points")
    max_score: int = Field(description="Maximum points")
    percentage: float = Field(description="Percentage score")
    letter_grade: str = Field(description="Letter grade")
    strengths: list[str] = Field(description="What was done well")
    improvements: list[str] = Field(description="Areas to improve")
    overall_feedback: str = Field(description="Summary feedback")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Grading Assistant",
        instructions=[
            "Apply rubric criteria consistently and fairly",
            "Provide specific, actionable feedback",
            "Balance positive reinforcement with constructive criticism",
            "Identify patterns in student work",
            "Suggest concrete steps for improvement"
        ],
        output_schema=GradingResult, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Grading Assistant - Demo\n" + "=" * 60)
    query = f"""Grade this {config['assignment_type']}:
Student: S12345
Assignment: Persuasive Essay on Climate Change
Rubric: Thesis (20), Evidence (25), Organization (20), Style (20), Mechanics (15)

Submission excerpt:
"Climate change is bad and we should do something. Many scientists say it's real.
The ice is melting which is causing problems. We need to use less gas and more
solar power. In conclusion, climate change is a big problem that needs solving."
(500 words total, basic structure, some grammar errors)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, GradingResult):
        print(f"\nStudent: {result.student_id} | Assignment: {result.assignment}")
        print(f"Score: {result.total_score}/{result.max_score} ({result.percentage:.1f}%) - {result.letter_grade}")
        print(f"\nRubric Breakdown:")
        for r in result.rubric_scores:
            print(f"  {r.criterion}: {r.score}/{r.max_score}")
        print(f"\nStrengths: {', '.join(result.strengths[:2])}")
        print(f"Improvements: {', '.join(result.improvements[:2])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignment-type", "-t", default=DEFAULT_CONFIG["assignment_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"assignment_type": args.assignment_type})

if __name__ == "__main__": main()
