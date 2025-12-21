"""
Example #154: Itinerary Builder Agent
Category: industry/travel
DESCRIPTION: Builds detailed daily itineraries with timing and logistics
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"city": "New York", "date": "2024-07-04", "interests": "museums, food, architecture"}

class Activity(BaseModel):
    time: str = Field(description="Start time")
    duration_minutes: int = Field(description="Duration")
    activity: str = Field(description="Activity name")
    location: str = Field(description="Location/address")
    cost: int = Field(description="Estimated cost")
    tips: str = Field(description="Insider tips")

class DayItinerary(BaseModel):
    date: str = Field(description="Itinerary date")
    theme: str = Field(description="Day theme")
    activities: list[Activity] = Field(description="Scheduled activities")
    meals: list[Activity] = Field(description="Meal stops")
    total_walking_km: float = Field(description="Total walking distance")
    total_cost: int = Field(description="Total estimated cost")
    transport_notes: str = Field(description="Transport recommendations")
    weather_backup: str = Field(description="Rainy day alternatives")
    energy_level: str = Field(description="Day intensity level")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Itinerary Builder",
        instructions=[
            "You are an expert daily itinerary planner.",
            f"Build itineraries for {cfg['city']} focusing on {cfg['interests']}",
            "Create realistic timings with transit time",
            "Balance activities with rest and meals",
            "Consider opening hours and peak times",
            "Provide practical logistics and alternatives",
        ],
        output_schema=DayItinerary,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Itinerary Builder Agent - Demo")
    print("=" * 60)
    query = f"""Build a day itinerary:
- City: {config['city']}
- Date: {config['date']}
- Interests: {config['interests']}

Create a detailed schedule with timings."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DayItinerary):
        print(f"\n📅 {result.date} - {result.theme}")
        print(f"🚶 {result.total_walking_km}km walk | 💰 ~${result.total_cost}")
        print(f"\n⏰ Schedule:")
        for act in result.activities[:4]:
            print(f"  {act.time} - {act.activity} ({act.duration_minutes}min)")
            print(f"    📍 {act.location} | ${act.cost}")
        print(f"\n🍽️ Meals:")
        for meal in result.meals[:2]:
            print(f"  {meal.time} - {meal.activity}")
        print(f"\n🚇 Transport: {result.transport_notes}")
        print(f"☔ Backup: {result.weather_backup}")

def main():
    parser = argparse.ArgumentParser(description="Itinerary Builder Agent")
    parser.add_argument("--city", "-c", default=DEFAULT_CONFIG["city"])
    parser.add_argument("--date", "-d", default=DEFAULT_CONFIG["date"])
    parser.add_argument("--interests", "-i", default=DEFAULT_CONFIG["interests"])
    args = parser.parse_args()
    config = {"city": args.city, "date": args.date, "interests": args.interests}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
