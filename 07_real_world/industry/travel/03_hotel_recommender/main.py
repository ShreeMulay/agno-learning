"""
Example #153: Hotel Recommender Agent
Category: industry/travel
DESCRIPTION: Recommends hotels based on preferences and location
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"city": "Barcelona", "check_in": "2024-06-20", "nights": 4, "budget_per_night": 200}

class HotelOption(BaseModel):
    name: str = Field(description="Hotel name")
    neighborhood: str = Field(description="Neighborhood")
    star_rating: float = Field(description="Star rating")
    price_per_night: int = Field(description="Price per night")
    highlights: list[str] = Field(description="Key highlights")
    walkability: str = Field(description="Walkability to attractions")

class HotelRecommendation(BaseModel):
    city: str = Field(description="City")
    stay_dates: str = Field(description="Check-in to check-out")
    top_pick: HotelOption = Field(description="Top recommendation")
    alternatives: list[HotelOption] = Field(description="Alternative options")
    neighborhood_guide: str = Field(description="Best neighborhoods")
    booking_tips: list[str] = Field(description="Booking tips")
    amenity_priorities: list[str] = Field(description="Recommended amenities")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Hotel Recommender",
        instructions=[
            "You are an expert hotel and accommodation specialist.",
            f"Recommend hotels in {cfg['city']} within ${cfg['budget_per_night']}/night",
            "Consider location, amenities, and value",
            "Highlight neighborhood characteristics",
            "Provide insider tips for getting best rates",
            "Balance comfort with proximity to attractions",
        ],
        output_schema=HotelRecommendation,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Hotel Recommender Agent - Demo")
    print("=" * 60)
    query = f"""Recommend hotels:
- City: {config['city']}
- Check-in: {config['check_in']}
- Nights: {config['nights']}
- Budget: ${config['budget_per_night']}/night

Find best options with location analysis."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, HotelRecommendation):
        print(f"\n🏨 {result.city} - {result.stay_dates}")
        tp = result.top_pick
        print(f"\n⭐ Top Pick: {tp.name}")
        print(f"   📍 {tp.neighborhood} | {tp.star_rating}★ | ${tp.price_per_night}/night")
        print(f"   ✨ {', '.join(tp.highlights[:2])}")
        print(f"\n🏠 Neighborhoods: {result.neighborhood_guide[:100]}...")
        print(f"\n💡 Tips:")
        for tip in result.booking_tips[:2]:
            print(f"   • {tip}")

def main():
    parser = argparse.ArgumentParser(description="Hotel Recommender Agent")
    parser.add_argument("--city", "-c", default=DEFAULT_CONFIG["city"])
    parser.add_argument("--checkin", default=DEFAULT_CONFIG["check_in"])
    parser.add_argument("--nights", "-n", type=int, default=DEFAULT_CONFIG["nights"])
    parser.add_argument("--budget", "-b", type=int, default=DEFAULT_CONFIG["budget_per_night"])
    args = parser.parse_args()
    config = {"city": args.city, "check_in": args.checkin, "nights": args.nights, "budget_per_night": args.budget}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
