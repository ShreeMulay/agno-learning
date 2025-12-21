"""
Example #128: Transcript Processor
Category: education/admin
DESCRIPTION: Processes and evaluates academic transcripts
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"process_type": "transfer_evaluation"}

class CourseEquivalency(BaseModel):
    original_course: str = Field(description="Original course")
    equivalent_course: str = Field(description="Equivalent at new school")
    credits: float = Field(description="Credits transferred")
    status: str = Field(description="accepted, denied, pending_review")

class TranscriptEvaluation(BaseModel):
    student_name: str = Field(description="Student name")
    source_institution: str = Field(description="Sending institution")
    total_credits_submitted: float = Field(description="Credits submitted")
    credits_accepted: float = Field(description="Credits accepted")
    equivalencies: list[CourseEquivalency] = Field(description="Course equivalencies")
    requirements_met: list[str] = Field(description="Requirements satisfied")
    remaining_requirements: list[str] = Field(description="Still needed")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Transcript Processor",
        instructions=["Evaluate course equivalencies", "Calculate transfer credits", "Identify requirements met", "Flag issues for review"],
        output_schema=TranscriptEvaluation, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Transcript Processor - Demo\n" + "=" * 60)
    response = agent.run(f"Process {config['process_type']}: Student from State Community College, 45 credits including English Comp I/II, College Algebra, Intro Psychology, General Biology I/II")
    result = response.content
    if isinstance(result, TranscriptEvaluation):
        print(f"\nStudent: {result.student_name} | From: {result.source_institution}")
        print(f"Credits: {result.credits_accepted}/{result.total_credits_submitted} accepted")
        print(f"\nEquivalencies:")
        for e in result.equivalencies[:3]:
            print(f"  {e.original_course} → {e.equivalent_course} ({e.status})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--process-type", "-t", default=DEFAULT_CONFIG["process_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"process_type": args.process_type})

if __name__ == "__main__": main()
