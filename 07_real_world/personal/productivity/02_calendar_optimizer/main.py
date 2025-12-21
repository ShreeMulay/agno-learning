"""
Example #182: Calendar Optimizer Agent
Category: personal/productivity
DESCRIPTION: Optimizes calendar scheduling for productivity, focus time, and work-life balance
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"work_hours": "9-17"}

class TimeBlock(BaseModel):
    time_slot: str = Field(description="Time range")
    activity: str = Field(description="Recommended activity")
    block_type: str = Field(description="focus, meetings, admin, break")
    energy_match: str = Field(description="Why this time suits this activity")

class CalendarOptimization(BaseModel):
    schedule: list[TimeBlock] = Field(description="Optimized daily schedule")
    focus_blocks: list[str] = Field(description="Protected deep work times")
    meeting_windows: list[str] = Field(description="Ideal meeting times")
    buffer_recommendations: list[str] = Field(description="Suggested buffers between activities")
    productivity_tips: list[str] = Field(description="Schedule optimization tips")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Calendar Optimizer",
        instructions=[
            f"You optimize calendars for productivity within {cfg['work_hours']} work hours.",
            "Apply time-blocking principles for deep work.",
            "Match high-energy tasks to peak performance times.",
            "Ensure adequate breaks and transition buffers.",
            "Protect focus time from meeting fragmentation.",
        ],
        output_schema=CalendarOptimization,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Calendar Optimizer - Demo")
    print("=" * 60)
    query = """Optimize my calendar for tomorrow:
    - Need 3 hours for coding project
    - 2 team meetings (30 min each)
    - Email catch-up
    - 1:1 with manager (45 min)
    - Review documents
    I'm most focused in the morning."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CalendarOptimization):
        print(f"\n📅 Optimized Schedule:")
        for block in result.schedule[:5]:
            print(f"  {block.time_slot}: {block.activity} ({block.block_type})")
        print(f"\n🎯 Focus Blocks: {', '.join(result.focus_blocks)}")
        print(f"📞 Meeting Windows: {', '.join(result.meeting_windows)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work-hours", "-w", default=DEFAULT_CONFIG["work_hours"])
    args = parser.parse_args()
    run_demo(get_agent(config={"work_hours": args.work_hours}), {"work_hours": args.work_hours})

if __name__ == "__main__": main()
