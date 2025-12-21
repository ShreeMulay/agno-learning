"""
Example #187: Time Blocker Agent
Category: personal/productivity
DESCRIPTION: Creates time-blocked schedules for maximum focus and productivity
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"style": "pomodoro"}

class TimeBlock(BaseModel):
    start_time: str = Field(description="Block start time")
    end_time: str = Field(description="Block end time")
    activity: str = Field(description="What to work on")
    block_type: str = Field(description="deep_work, shallow, admin, break")
    energy_level: str = Field(description="high, medium, low energy required")

class TimeBlockedDay(BaseModel):
    blocks: list[TimeBlock] = Field(description="Time blocks for the day")
    deep_work_hours: float = Field(description="Total deep work hours")
    break_minutes: int = Field(description="Total break time")
    buffer_time: str = Field(description="Unscheduled buffer for overflow")
    evening_cutoff: str = Field(description="When to stop working")
    productivity_score: int = Field(description="Expected productivity 1-10")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Time Blocker",
        instructions=[
            f"You create time-blocked schedules using {cfg['style']} technique.",
            "Prioritize deep work during peak energy hours.",
            "Include adequate breaks to prevent burnout.",
            "Batch similar tasks together to minimize context switching.",
            "Build in buffer time for unexpected interruptions.",
        ],
        output_schema=TimeBlockedDay,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Time Blocker - Demo")
    print("=" * 60)
    query = """Create a time-blocked schedule for tomorrow:
    Work hours: 8am - 5pm
    Tasks:
    - Write technical documentation (needs 2 hours focus)
    - Team standup at 10am (15 min)
    - Code review (1 hour)
    - Email and Slack (ongoing)
    - 1:1 meeting at 2pm (30 min)
    - Bug fixes (1.5 hours)
    I'm most focused in the morning."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, TimeBlockedDay):
        print(f"\n📅 Time-Blocked Schedule:")
        for block in result.blocks:
            emoji = "🔴" if block.block_type == "deep_work" else "🟡" if block.block_type == "shallow" else "🟢"
            print(f"  {emoji} {block.start_time}-{block.end_time}: {block.activity}")
        print(f"\n📊 Deep Work: {result.deep_work_hours}h | Breaks: {result.break_minutes}min")
        print(f"🛑 Evening cutoff: {result.evening_cutoff}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", "-s", default=DEFAULT_CONFIG["style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"style": args.style}), {"style": args.style})

if __name__ == "__main__": main()
