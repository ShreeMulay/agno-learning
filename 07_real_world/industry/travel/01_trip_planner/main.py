"""
Example #151: Trip Planner Agent
Category: industry/travel
DESCRIPTION: Creates personalized trip plans based on preferences and budget
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"destination": "Tokyo, Japan", "duration_days": 7, "budget": 3000, "travel_style": "cultural"}

class DayPlan(BaseModel):
    day: int = Field(description="Day number")
    theme: str = Field(description="Day theme")
    activities: list[str] = Field(description="Planned activities")
    meals: list[str] = Field(description="Meal recommendations")
    estimated_cost: int = Field(description="Estimated daily cost")

class TripPlan(BaseModel):
    destination: str = Field(description="Trip destination")
    duration: int = Field(description="Trip duration in days")
    total_budget: int = Field(description="Total budget")
    daily_plans: list[DayPlan] = Field(description="Day by day plans")
    accommodation_suggestion: str = Field(description="Where to stay")
    packing_essentials: list[str] = Field(description="What to pack")
    local_tips: list[str] = Field(description="Local insider tips")
    budget_breakdown: dict = Field(description="Budget allocation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Trip Planner",
        instructions=[
            "You are an expert travel planner specializing in personalized trips.",
            f"Plan trips with {cfg['travel_style']} focus",
            "Create detailed day-by-day itineraries",
            "Balance must-see attractions with local experiences",
            "Consider practical factors like jet lag and travel time",
            "Stay within budget constraints",
        ],
        output_schema=TripPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Trip Planner Agent - Demo")
    print("=" * 60)
    query = f"""Plan a trip:
- Destination: {config['destination']}
- Duration: {config['duration_days']} days
- Budget: ${config['budget']}
- Style: {config['travel_style']}

Create a detailed day-by-day itinerary."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, TripPlan):
        print(f"\n✈️ {result.destination} - {result.duration} days (${result.total_budget} budget)")
        print(f"🏨 Stay: {result.accommodation_suggestion}")
        print(f"\n📅 Itinerary:")
        for day in result.daily_plans[:3]:
            print(f"  Day {day.day}: {day.theme} (~${day.estimated_cost})")
            print(f"    • {day.activities[0]}")
        print(f"\n💡 Tips: {result.local_tips[0]}")

def main():
    parser = argparse.ArgumentParser(description="Trip Planner Agent")
    parser.add_argument("--dest", "-d", default=DEFAULT_CONFIG["destination"])
    parser.add_argument("--days", type=int, default=DEFAULT_CONFIG["duration_days"])
    parser.add_argument("--budget", "-b", type=int, default=DEFAULT_CONFIG["budget"])
    parser.add_argument("--style", "-s", default=DEFAULT_CONFIG["travel_style"])
    args = parser.parse_args()
    config = {"destination": args.dest, "duration_days": args.days, "budget": args.budget, "travel_style": args.style}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
