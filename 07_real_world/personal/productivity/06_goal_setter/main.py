"""
Example #186: Goal Setter Agent
Category: personal/productivity
DESCRIPTION: Helps define SMART goals, break them into milestones, and track progress
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"timeframe": "quarterly"}

class Milestone(BaseModel):
    title: str = Field(description="Milestone name")
    deadline: str = Field(description="Target date")
    success_criteria: str = Field(description="How to measure completion")
    dependencies: list[str] = Field(description="What needs to happen first")

class GoalPlan(BaseModel):
    goal_statement: str = Field(description="SMART goal statement")
    specific: str = Field(description="What exactly will be accomplished")
    measurable: str = Field(description="How progress will be measured")
    achievable: str = Field(description="Why this is realistic")
    relevant: str = Field(description="Why this matters")
    time_bound: str = Field(description="Deadline and timeframe")
    milestones: list[Milestone] = Field(description="Key milestones")
    first_actions: list[str] = Field(description="Immediate next steps")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Goal Setter",
        instructions=[
            f"You help set and plan {cfg['timeframe']} goals using SMART framework.",
            "Transform vague aspirations into specific, measurable goals.",
            "Break large goals into achievable milestones.",
            "Identify dependencies and potential blockers.",
            "Define clear success criteria for each milestone.",
        ],
        output_schema=GoalPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Goal Setter - Demo")
    print("=" * 60)
    query = """Help me set a goal:
    I want to get better at public speaking. I'm currently nervous
    presenting to groups larger than 5 people. I have a big presentation
    to the leadership team (20 people) in 3 months."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, GoalPlan):
        print(f"\n🎯 Goal: {result.goal_statement}")
        print(f"\n📊 SMART Breakdown:")
        print(f"  Specific: {result.specific}")
        print(f"  Measurable: {result.measurable}")
        print(f"  Time-bound: {result.time_bound}")
        print(f"\n🏁 Milestones:")
        for m in result.milestones:
            print(f"  • {m.title} (by {m.deadline})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeframe", "-t", default=DEFAULT_CONFIG["timeframe"])
    args = parser.parse_args()
    run_demo(get_agent(config={"timeframe": args.timeframe}), {"timeframe": args.timeframe})

if __name__ == "__main__": main()
