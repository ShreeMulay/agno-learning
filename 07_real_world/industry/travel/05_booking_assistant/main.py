"""
Example #155: Booking Assistant Agent
Category: industry/travel
DESCRIPTION: Assists with travel bookings and reservations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"booking_type": "restaurant", "location": "Paris", "date": "2024-06-25", "party_size": 4}

class BookingOption(BaseModel):
    name: str = Field(description="Venue name")
    availability: str = Field(description="Available times")
    price_range: str = Field(description="Price range")
    rating: float = Field(description="Rating")
    special_notes: str = Field(description="Special requirements notes")

class BookingAssistance(BaseModel):
    booking_type: str = Field(description="Type of booking")
    location: str = Field(description="Location")
    date: str = Field(description="Requested date")
    available_options: list[BookingOption] = Field(description="Available options")
    recommended: str = Field(description="Top recommendation")
    booking_steps: list[str] = Field(description="Steps to complete booking")
    confirmation_checklist: list[str] = Field(description="What to confirm")
    cancellation_policy: str = Field(description="Typical cancellation terms")
    tips: list[str] = Field(description="Booking tips")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Booking Assistant",
        instructions=[
            "You are an expert travel booking assistant.",
            f"Help with {cfg['booking_type']} bookings in {cfg['location']}",
            "Provide availability options and recommendations",
            "Guide through booking process",
            "Highlight important policies and confirmations",
            "Offer practical booking tips",
        ],
        output_schema=BookingAssistance,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Booking Assistant Agent - Demo")
    print("=" * 60)
    query = f"""Help with booking:
- Type: {config['booking_type']}
- Location: {config['location']}
- Date: {config['date']}
- Party Size: {config['party_size']}

Find options and guide the booking process."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, BookingAssistance):
        print(f"\n📋 {result.booking_type.title()} Booking - {result.location}")
        print(f"📅 Date: {result.date}")
        print(f"\n⭐ Recommended: {result.recommended}")
        print(f"\n🔍 Options:")
        for opt in result.available_options[:3]:
            print(f"  • {opt.name} ({opt.rating}★) - {opt.price_range}")
            print(f"    Available: {opt.availability}")
        print(f"\n📝 Booking Steps:")
        for i, step in enumerate(result.booking_steps[:3], 1):
            print(f"  {i}. {step}")
        print(f"\n❌ Cancellation: {result.cancellation_policy}")

def main():
    parser = argparse.ArgumentParser(description="Booking Assistant Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["booking_type"])
    parser.add_argument("--location", "-l", default=DEFAULT_CONFIG["location"])
    parser.add_argument("--date", "-d", default=DEFAULT_CONFIG["date"])
    parser.add_argument("--party", "-p", type=int, default=DEFAULT_CONFIG["party_size"])
    args = parser.parse_args()
    config = {"booking_type": args.type, "location": args.location, "date": args.date, "party_size": args.party}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
