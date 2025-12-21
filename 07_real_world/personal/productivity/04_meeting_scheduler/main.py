"""
Example #184: Meeting Scheduler Agent
Category: personal/productivity
DESCRIPTION: Finds optimal meeting times considering availability, time zones, and preferences
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"timezone": "US/Eastern"}

class MeetingSlot(BaseModel):
    datetime: str = Field(description="Proposed meeting time")
    duration: str = Field(description="Meeting duration")
    participants_available: list[str] = Field(description="Who can attend")
    conflicts: list[str] = Field(description="Any conflicts to resolve")
    score: int = Field(description="Suitability score 1-10")

class MeetingSchedule(BaseModel):
    recommended_slot: MeetingSlot = Field(description="Best meeting time")
    alternatives: list[MeetingSlot] = Field(description="Backup options")
    preparation_needed: list[str] = Field(description="Pre-meeting prep items")
    agenda_suggestions: list[str] = Field(description="Suggested agenda items")
    logistics: str = Field(description="Room/link recommendations")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Meeting Scheduler",
        instructions=[
            f"You schedule meetings optimally in {cfg['timezone']} timezone.",
            "Consider all participants' availability and preferences.",
            "Avoid scheduling during focus time or lunch hours.",
            "Minimize timezone conflicts for remote participants.",
            "Suggest appropriate meeting duration based on agenda.",
        ],
        output_schema=MeetingSchedule,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Meeting Scheduler - Demo")
    print("=" * 60)
    query = """Schedule a project kickoff meeting:
    Participants:
    - Alice (US/Eastern, busy 9-11am)
    - Bob (US/Pacific, prefers mornings)
    - Carol (Europe/London, available afternoons)
    Duration: 1 hour
    Purpose: Q1 planning discussion
    Needs: Screen sharing capability"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, MeetingSchedule):
        rec = result.recommended_slot
        print(f"\n✅ Recommended: {rec.datetime} ({rec.duration})")
        print(f"   Score: {rec.score}/10")
        print(f"   Available: {', '.join(rec.participants_available)}")
        print(f"\n📋 Agenda Suggestions:")
        for item in result.agenda_suggestions:
            print(f"  • {item}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timezone", "-t", default=DEFAULT_CONFIG["timezone"])
    args = parser.parse_args()
    run_demo(get_agent(config={"timezone": args.timezone}), {"timezone": args.timezone})

if __name__ == "__main__": main()
