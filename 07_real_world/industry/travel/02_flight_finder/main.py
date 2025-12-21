"""
Example #152: Flight Finder Agent
Category: industry/travel
DESCRIPTION: Finds optimal flight options based on preferences
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"origin": "SFO", "destination": "LHR", "date": "2024-06-15", "passengers": 2}

class FlightOption(BaseModel):
    airline: str = Field(description="Airline name")
    flight_number: str = Field(description="Flight number")
    departure: str = Field(description="Departure time")
    arrival: str = Field(description="Arrival time")
    duration: str = Field(description="Flight duration")
    stops: int = Field(description="Number of stops")
    price_per_person: int = Field(description="Price per person")
    class_type: str = Field(description="Cabin class")

class FlightSearch(BaseModel):
    route: str = Field(description="Route summary")
    search_date: str = Field(description="Travel date")
    best_value: FlightOption = Field(description="Best value option")
    fastest: FlightOption = Field(description="Fastest option")
    all_options: list[FlightOption] = Field(description="All flight options")
    price_trend: str = Field(description="Price trend analysis")
    booking_recommendation: str = Field(description="When to book")
    flexibility_tips: list[str] = Field(description="Tips for better prices")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Flight Finder",
        instructions=[
            "You are an expert flight search specialist.",
            f"Search flights from {cfg['origin']} to {cfg['destination']}",
            "Compare airlines on price, duration, and comfort",
            "Consider layover times and connection airports",
            "Provide realistic pricing based on market knowledge",
            "Offer booking timing recommendations",
        ],
        output_schema=FlightSearch,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Flight Finder Agent - Demo")
    print("=" * 60)
    query = f"""Find flights:
- From: {config['origin']}
- To: {config['destination']}
- Date: {config['date']}
- Passengers: {config['passengers']}

Compare options and recommend best choices."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, FlightSearch):
        print(f"\n✈️ {result.route} on {result.search_date}")
        bv = result.best_value
        print(f"\n💰 Best Value: {bv.airline} {bv.flight_number}")
        print(f"   {bv.departure} → {bv.arrival} ({bv.duration}, {bv.stops} stops)")
        print(f"   ${bv.price_per_person}/person - {bv.class_type}")
        f = result.fastest
        print(f"\n⚡ Fastest: {f.airline} {f.flight_number} ({f.duration})")
        print(f"\n📊 Trend: {result.price_trend}")
        print(f"🎯 Book: {result.booking_recommendation}")

def main():
    parser = argparse.ArgumentParser(description="Flight Finder Agent")
    parser.add_argument("--origin", "-o", default=DEFAULT_CONFIG["origin"])
    parser.add_argument("--dest", "-d", default=DEFAULT_CONFIG["destination"])
    parser.add_argument("--date", default=DEFAULT_CONFIG["date"])
    parser.add_argument("--pax", "-p", type=int, default=DEFAULT_CONFIG["passengers"])
    args = parser.parse_args()
    config = {"origin": args.origin, "destination": args.dest, "date": args.date, "passengers": args.pax}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
