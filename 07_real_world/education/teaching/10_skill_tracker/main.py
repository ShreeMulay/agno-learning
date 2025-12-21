"""
Example #120: Skill Tracker
Category: education/teaching
DESCRIPTION: Tracks student skill development over time with progress reports
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"subject": "writing"}

class SkillProgress(BaseModel):
    skill: str = Field(description="Skill name")
    starting_level: str = Field(description="Beginning level")
    current_level: str = Field(description="Current level")
    growth: str = Field(description="Growth observed")
    evidence: list[str] = Field(description="Evidence of progress")

class ProgressReport(BaseModel):
    student_name: str = Field(description="Student name")
    subject: str = Field(description="Subject area")
    reporting_period: str = Field(description="Time period")
    skills: list[SkillProgress] = Field(description="Skill progress")
    achievements: list[str] = Field(description="Notable achievements")
    areas_of_growth: list[str] = Field(description="Areas showing growth")
    focus_areas: list[str] = Field(description="Areas needing focus")
    goals_for_next_period: list[str] = Field(description="Goals ahead")
    narrative_summary: str = Field(description="Overall narrative")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Skill Tracker",
        instructions=[
            "Track skill development with specific evidence",
            "Show growth trajectory over time",
            "Celebrate achievements and progress",
            "Identify areas for continued focus",
            "Set meaningful, achievable goals"
        ],
        output_schema=ProgressReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Skill Tracker - Demo\n" + "=" * 60)
    query = f"""Create progress report:
Student: Marcus
Subject: {config['subject']}
Period: Fall semester

Data points:
- September essay: Basic paragraph structure, simple vocabulary
- October essay: Improved transitions, attempted thesis statement
- November essay: Clear thesis, better evidence, still needs work on conclusions
- Class participation: Actively shares ideas, asks good questions
- Peer editing: Provides helpful feedback to others"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ProgressReport):
        print(f"\nStudent: {result.student_name}")
        print(f"Subject: {result.subject} | Period: {result.reporting_period}")
        print(f"\nSkill Progress:")
        for s in result.skills:
            print(f"  {s.skill}: {s.starting_level} → {s.current_level}")
        print(f"\n🏆 Achievements:")
        for a in result.achievements[:2]:
            print(f"  {a}")
        print(f"\n🎯 Goals for Next Period:")
        for g in result.goals_for_next_period[:2]:
            print(f"  {g}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", "-s", default=DEFAULT_CONFIG["subject"])
    args = parser.parse_args()
    run_demo(get_agent(), {"subject": args.subject})

if __name__ == "__main__": main()
