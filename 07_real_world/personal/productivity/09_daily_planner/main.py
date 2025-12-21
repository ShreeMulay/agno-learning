"""
Example #189: Daily Planner Agent
Category: personal/productivity
DESCRIPTION: Creates comprehensive daily plans balancing work, personal, and wellness goals
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"planning_style": "balanced"}

class DailyItem(BaseModel):
    time: str = Field(description="Scheduled time")
    activity: str = Field(description="What to do")
    category: str = Field(description="work, personal, health, admin")
    priority: str = Field(description="must_do, should_do, nice_to_have")
    notes: str = Field(description="Additional context or tips")

class DailyPlan(BaseModel):
    morning_routine: list[DailyItem] = Field(description="Morning activities")
    work_blocks: list[DailyItem] = Field(description="Work-related items")
    personal_time: list[DailyItem] = Field(description="Personal activities")
    evening_routine: list[DailyItem] = Field(description="Evening wind-down")
    top_3_priorities: list[str] = Field(description="Most important outcomes")
    self_care_reminder: str = Field(description="Wellness check-in")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Daily Planner",
        instructions=[
            f"You create {cfg['planning_style']} daily plans.",
            "Balance productivity with self-care and personal time.",
            "Include morning and evening routines for consistency.",
            "Identify the 3 most important outcomes for the day.",
            "Build in flexibility for unexpected events.",
        ],
        output_schema=DailyPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Daily Planner - Demo")
    print("=" * 60)
    query = """Plan my day tomorrow:
    Work: Product launch presentation, team sync, code review
    Personal: Pick up dry cleaning, call mom
    Health: Want to exercise and eat well
    I wake at 6:30am, work 9-5, want to sleep by 10:30pm"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DailyPlan):
        print(f"\n🌅 Morning Routine:")
        for item in result.morning_routine:
            print(f"  {item.time}: {item.activity}")
        print(f"\n💼 Work Blocks:")
        for item in result.work_blocks[:3]:
            print(f"  {item.time}: {item.activity} ({item.priority})")
        print(f"\n🎯 Top 3 Priorities:")
        for i, p in enumerate(result.top_3_priorities, 1):
            print(f"  {i}. {p}")
        print(f"\n💚 {result.self_care_reminder}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--planning-style", "-p", default=DEFAULT_CONFIG["planning_style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"planning_style": args.planning_style}), {"planning_style": args.planning_style})

if __name__ == "__main__": main()
