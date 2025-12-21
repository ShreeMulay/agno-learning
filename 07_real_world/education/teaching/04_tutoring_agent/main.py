"""
Example #114: Tutoring Agent
Category: education/teaching
DESCRIPTION: Provides personalized tutoring with explanations and practice problems
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"subject": "algebra", "skill_level": "beginner"}

class PracticeProblem(BaseModel):
    problem: str = Field(description="Practice problem")
    hint: str = Field(description="Helpful hint")
    solution: str = Field(description="Step-by-step solution")

class TutoringResponse(BaseModel):
    topic: str = Field(description="Topic being taught")
    explanation: str = Field(description="Clear explanation of concept")
    examples: list[str] = Field(description="Worked examples")
    practice_problems: list[PracticeProblem] = Field(description="Practice problems")
    common_mistakes: list[str] = Field(description="Common mistakes to avoid")
    next_steps: list[str] = Field(description="What to learn next")
    encouragement: str = Field(description="Encouraging message")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Tutoring Agent",
        instructions=[
            "Explain concepts in clear, accessible language",
            "Use multiple representations (verbal, visual, symbolic)",
            "Scaffold learning with appropriate difficulty progression",
            "Anticipate and address common misconceptions",
            "Encourage growth mindset and persistence"
        ],
        output_schema=TutoringResponse, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Tutoring Agent - Demo\n" + "=" * 60)
    query = f"""Tutor me on:
Subject: {config['subject']}
Level: {config['skill_level']}
Topic: Solving two-step equations
Student says: "I don't understand how to solve 2x + 5 = 13" """
    response = agent.run(query)
    result = response.content
    if isinstance(result, TutoringResponse):
        print(f"\nTopic: {result.topic}")
        print(f"\nExplanation:\n{result.explanation[:300]}...")
        print(f"\nExamples: {len(result.examples)}")
        print(f"Practice Problems: {len(result.practice_problems)}")
        print(f"\nCommon Mistakes to Avoid:")
        for m in result.common_mistakes[:2]:
            print(f"  ⚠️ {m}")
        print(f"\n💪 {result.encouragement}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", "-s", default=DEFAULT_CONFIG["subject"])
    parser.add_argument("--skill-level", "-l", default=DEFAULT_CONFIG["skill_level"])
    args = parser.parse_args()
    run_demo(get_agent(), {"subject": args.subject, "skill_level": args.skill_level})

if __name__ == "__main__": main()
