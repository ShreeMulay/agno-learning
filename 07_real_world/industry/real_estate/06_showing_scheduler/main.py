"""
Example #136: Showing Scheduler Agent
Category: industry/real_estate
DESCRIPTION: Optimizes property showing schedules for agents and buyers
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"properties_count": 5, "available_time": "Saturday 10am-4pm", "location": "Austin metro"}

class ScheduledShowing(BaseModel):
    time_slot: str = Field(description="Scheduled time for showing")
    property_address: str = Field(description="Property address")
    duration_minutes: int = Field(description="Expected showing duration")
    drive_time_from_previous: int = Field(description="Drive time from previous showing")
    priority: str = Field(description="high/medium/low priority")
    notes: str = Field(description="Showing notes or special instructions")

class ShowingSchedule(BaseModel):
    schedule_date: str = Field(description="Date of showings")
    total_properties: int = Field(description="Number of properties scheduled")
    showings: list[ScheduledShowing] = Field(description="Scheduled showings in order")
    total_drive_time: int = Field(description="Total drive time in minutes")
    route_efficiency: str = Field(description="Route efficiency assessment")
    preparation_checklist: list[str] = Field(description="Pre-showing checklist items")
    backup_properties: list[str] = Field(description="Backup properties if time permits")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Showing Scheduler",
        instructions=[
            "You are an expert real estate showing coordinator.",
            f"Schedule showings in the {cfg['location']} area",
            "Optimize routes to minimize drive time between properties",
            "Allow adequate time for thorough viewings",
            "Consider property priorities and client preferences",
            "Include buffer time for traffic and delays",
        ],
        output_schema=ShowingSchedule,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Showing Scheduler Agent - Demo")
    print("=" * 60)
    query = f"""Create an optimized showing schedule:
- Number of properties: {config['properties_count']}
- Available time: {config['available_time']}
- Area: {config['location']}

Optimize for route efficiency and adequate viewing time."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ShowingSchedule):
        print(f"\n📅 Schedule for: {result.schedule_date}")
        print(f"🏠 Properties: {result.total_properties}")
        print(f"\n🗓️ Showings:")
        for s in result.showings[:4]:
            print(f"  {s.time_slot} - {s.property_address}")
            print(f"    ⏱️ {s.duration_minutes}min | 🚗 {s.drive_time_from_previous}min drive | {s.priority} priority")
        print(f"\n🚗 Total Drive Time: {result.total_drive_time} minutes")
        print(f"📊 Efficiency: {result.route_efficiency}")

def main():
    parser = argparse.ArgumentParser(description="Showing Scheduler Agent")
    parser.add_argument("--count", "-c", type=int, default=DEFAULT_CONFIG["properties_count"])
    parser.add_argument("--time", "-t", default=DEFAULT_CONFIG["available_time"])
    parser.add_argument("--location", "-l", default=DEFAULT_CONFIG["location"])
    args = parser.parse_args()
    config = {"properties_count": args.count, "available_time": args.time, "location": args.location}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
