"""
Example #188: Focus Coach Agent
Category: personal/productivity
DESCRIPTION: Provides strategies and coaching to improve concentration and reduce distractions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"challenge": "general"}

class FocusStrategy(BaseModel):
    technique: str = Field(description="Focus technique name")
    description: str = Field(description="How to apply it")
    when_to_use: str = Field(description="Best situations for this technique")
    duration: str = Field(description="Recommended session length")

class FocusCoaching(BaseModel):
    diagnosis: str = Field(description="Assessment of focus challenges")
    root_causes: list[str] = Field(description="Likely causes of distraction")
    immediate_actions: list[str] = Field(description="Quick wins to try now")
    strategies: list[FocusStrategy] = Field(description="Recommended techniques")
    environment_tips: list[str] = Field(description="Workspace improvements")
    accountability_plan: str = Field(description="How to stay on track")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Focus Coach",
        instructions=[
            f"You coach people on improving focus, especially with {cfg['challenge']} challenges.",
            "Diagnose root causes of distraction, not just symptoms.",
            "Recommend evidence-based focus techniques.",
            "Suggest environmental and behavioral changes.",
            "Be encouraging while setting realistic expectations.",
        ],
        output_schema=FocusCoaching,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Focus Coach - Demo")
    print("=" * 60)
    query = """Help me focus better. My challenges:
    - I check my phone every 10 minutes
    - Open office makes it hard to concentrate
    - I procrastinate on difficult tasks
    - By 3pm I'm mentally exhausted
    - I have trouble starting deep work sessions"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, FocusCoaching):
        print(f"\n🔍 Diagnosis: {result.diagnosis}")
        print(f"\n🎯 Root Causes:")
        for cause in result.root_causes:
            print(f"  • {cause}")
        print(f"\n⚡ Try Now:")
        for action in result.immediate_actions:
            print(f"  • {action}")
        print(f"\n📱 Environment Tips:")
        for tip in result.environment_tips:
            print(f"  • {tip}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--challenge", "-c", default=DEFAULT_CONFIG["challenge"])
    args = parser.parse_args()
    run_demo(get_agent(config={"challenge": args.challenge}), {"challenge": args.challenge})

if __name__ == "__main__": main()
