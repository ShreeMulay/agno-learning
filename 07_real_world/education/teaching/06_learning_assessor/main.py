"""
Example #116: Learning Assessor
Category: education/teaching
DESCRIPTION: Assesses student learning and identifies knowledge gaps
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"subject": "mathematics"}

class SkillAssessment(BaseModel):
    skill: str = Field(description="Skill name")
    mastery_level: str = Field(description="mastered, developing, emerging, not_yet")
    evidence: str = Field(description="Evidence from student work")
    next_steps: str = Field(description="Recommended next steps")

class LearningAssessment(BaseModel):
    student_id: str = Field(description="Student identifier")
    subject: str = Field(description="Subject area")
    assessment_date: str = Field(description="Assessment date")
    skills: list[SkillAssessment] = Field(description="Skill assessments")
    strengths: list[str] = Field(description="Student strengths")
    gaps: list[str] = Field(description="Knowledge gaps")
    learning_style: str = Field(description="Observed learning preferences")
    recommendations: list[str] = Field(description="Instructional recommendations")
    intervention_needed: bool = Field(description="Needs intervention")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Learning Assessor",
        instructions=[
            "Analyze student work to assess skill mastery",
            "Identify patterns in errors and misconceptions",
            "Determine knowledge gaps and prerequisites needed",
            "Provide actionable recommendations for instruction",
            "Consider multiple sources of evidence"
        ],
        output_schema=LearningAssessment, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Learning Assessor - Demo\n" + "=" * 60)
    query = f"""Assess this student's {config['subject']} learning:
Student: S789
Recent work samples:
- Quiz 1: 65% (struggled with fractions)
- Homework: Completes basic problems, avoids word problems
- Class participation: Asks clarifying questions, needs extra time
- Quiz 2: 72% (improved on fractions, still weak on decimals)
Teacher notes: Works hard, gets frustrated with multi-step problems"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, LearningAssessment):
        print(f"\nStudent: {result.student_id} | Subject: {result.subject}")
        print(f"Intervention Needed: {result.intervention_needed}")
        print(f"\nSkills Assessment:")
        for s in result.skills:
            print(f"  [{s.mastery_level}] {s.skill}")
        print(f"\nGaps: {', '.join(result.gaps)}")
        print(f"\nRecommendations:")
        for r in result.recommendations[:3]:
            print(f"  → {r}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", "-s", default=DEFAULT_CONFIG["subject"])
    args = parser.parse_args()
    run_demo(get_agent(), {"subject": args.subject})

if __name__ == "__main__": main()
