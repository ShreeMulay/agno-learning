"""
Example #156: Travel Advisor Agent
Category: industry/travel
DESCRIPTION: Provides personalized travel advice and destination recommendations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"travel_month": "October", "interests": "beaches, hiking", "budget_level": "moderate"}

class DestinationRec(BaseModel):
    destination: str = Field(description="Destination name")
    country: str = Field(description="Country")
    why_now: str = Field(description="Why visit this month")
    highlights: list[str] = Field(description="Top highlights")
    budget_estimate: str = Field(description="Budget estimate per week")
    match_score: int = Field(description="Match to preferences 0-100")

class TravelAdvice(BaseModel):
    traveler_profile: str = Field(description="Summary of preferences")
    top_destinations: list[DestinationRec] = Field(description="Recommended destinations")
    seasonal_insights: str = Field(description="Seasonal travel insights")
    budget_tips: list[str] = Field(description="Budget optimization tips")
    health_safety: list[str] = Field(description="Health and safety notes")
    packing_season: list[str] = Field(description="Seasonal packing tips")
    booking_timeline: str = Field(description="When to book")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Travel Advisor",
        instructions=[
            "You are an expert travel advisor with global destination knowledge.",
            f"Recommend destinations for {cfg['travel_month']} travel",
            f"Focus on {cfg['interests']} activities",
            f"Consider {cfg['budget_level']} budget level",
            "Provide honest seasonal advice",
            "Include practical health and safety info",
        ],
        output_schema=TravelAdvice,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Travel Advisor Agent - Demo")
    print("=" * 60)
    query = f"""Recommend travel destinations:
- Travel Month: {config['travel_month']}
- Interests: {config['interests']}
- Budget Level: {config['budget_level']}

Provide personalized destination recommendations."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, TravelAdvice):
        print(f"\n👤 Profile: {result.traveler_profile}")
        print(f"\n🌍 Top Destinations for {config['travel_month']}:")
        for dest in result.top_destinations[:3]:
            print(f"\n  📍 {dest.destination}, {dest.country} ({dest.match_score}% match)")
            print(f"     Why now: {dest.why_now}")
            print(f"     Budget: {dest.budget_estimate}")
        print(f"\n🌤️ Seasonal: {result.seasonal_insights}")
        print(f"📅 Book: {result.booking_timeline}")

def main():
    parser = argparse.ArgumentParser(description="Travel Advisor Agent")
    parser.add_argument("--month", "-m", default=DEFAULT_CONFIG["travel_month"])
    parser.add_argument("--interests", "-i", default=DEFAULT_CONFIG["interests"])
    parser.add_argument("--budget", "-b", default=DEFAULT_CONFIG["budget_level"])
    args = parser.parse_args()
    config = {"travel_month": args.month, "interests": args.interests, "budget_level": args.budget}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
