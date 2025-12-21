"""
Example #206: Writing Coach Agent
Category: personal/creative
DESCRIPTION: Provides writing feedback, suggestions, and coaching to improve craft
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"focus": "general"}

class WritingFeedback(BaseModel):
    overall_assessment: str = Field(description="General evaluation of the writing")
    strengths: list[str] = Field(description="What works well")
    areas_for_improvement: list[str] = Field(description="What could be better")
    specific_suggestions: list[str] = Field(description="Concrete revision suggestions")
    style_notes: str = Field(description="Observations about voice and style")
    grammar_issues: list[str] = Field(description="Grammar or mechanics to fix")
    exercises: list[str] = Field(description="Practice exercises to improve")
    encouragement: str = Field(description="Motivating closing message")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Writing Coach",
        instructions=[
            f"You coach writers with focus on {cfg['focus']} writing skills.",
            "Provide balanced feedback: strengths and improvements.",
            "Give specific, actionable suggestions.",
            "Be encouraging while being honest.",
            "Suggest exercises to build skills.",
        ],
        output_schema=WritingFeedback,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Writing Coach - Demo")
    print("=" * 60)
    query = """Review this opening paragraph:

    'The morning sun rose over the city, casting long shadows across 
    the empty streets. Sarah walked quickly, her footsteps echoing 
    in the silence. She was nervous. Very nervous. The meeting that 
    awaited her could change everything she had worked for.'
    
    I'm trying to create tension while establishing setting."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, WritingFeedback):
        print(f"\n📝 Assessment: {result.overall_assessment}")
        print(f"\n✅ Strengths:")
        for s in result.strengths:
            print(f"  • {s}")
        print(f"\n📈 To Improve:")
        for i in result.areas_for_improvement:
            print(f"  • {i}")
        print(f"\n🎯 Suggestions:")
        for sug in result.specific_suggestions[:3]:
            print(f"  • {sug}")
        print(f"\n💪 {result.encouragement}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--focus", "-f", default=DEFAULT_CONFIG["focus"])
    args = parser.parse_args()
    run_demo(get_agent(config={"focus": args.focus}), {"focus": args.focus})

if __name__ == "__main__": main()
