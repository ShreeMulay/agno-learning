"""
Example #139: Neighborhood Reporter Agent
Category: industry/real_estate
DESCRIPTION: Generates comprehensive neighborhood reports for buyers
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"neighborhood": "Mueller", "city": "Austin, TX"}

class SchoolInfo(BaseModel):
    name: str = Field(description="School name")
    type: str = Field(description="Elementary/Middle/High")
    rating: int = Field(description="Rating out of 10")
    distance: str = Field(description="Distance from neighborhood")

class NeighborhoodReport(BaseModel):
    neighborhood_name: str = Field(description="Neighborhood name")
    overview: str = Field(description="Neighborhood overview")
    demographics: dict = Field(description="Key demographic info")
    schools: list[SchoolInfo] = Field(description="Nearby schools")
    amenities: list[str] = Field(description="Key amenities")
    walkability_score: int = Field(description="Walk score 0-100")
    transit_score: int = Field(description="Transit score 0-100")
    safety_rating: str = Field(description="Safety assessment")
    price_trends: str = Field(description="Recent price trends")
    lifestyle_fit: list[str] = Field(description="Best for these lifestyles")
    pros: list[str] = Field(description="Neighborhood pros")
    cons: list[str] = Field(description="Neighborhood cons")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Neighborhood Reporter",
        instructions=[
            "You are an expert neighborhood analyst and local area specialist.",
            f"Generate detailed reports for {cfg['city']} neighborhoods",
            "Provide comprehensive, honest assessments",
            "Include schools, safety, amenities, and lifestyle factors",
            "Give realistic walkability and transit scores",
            "Highlight both pros and cons objectively",
        ],
        output_schema=NeighborhoodReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Neighborhood Reporter Agent - Demo")
    print("=" * 60)
    query = f"""Generate a comprehensive neighborhood report:
- Neighborhood: {config['neighborhood']}
- City: {config['city']}

Include schools, safety, amenities, and lifestyle assessment."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, NeighborhoodReport):
        print(f"\n📍 {result.neighborhood_name}")
        print(f"\n📝 Overview: {result.overview}")
        print(f"\n🚶 Walkability: {result.walkability_score}/100 | 🚌 Transit: {result.transit_score}/100")
        print(f"🔒 Safety: {result.safety_rating}")
        print(f"\n🏫 Schools:")
        for s in result.schools[:3]:
            print(f"  • {s.name} ({s.type}): {s.rating}/10")
        print(f"\n✅ Pros: {', '.join(result.pros[:3])}")
        print(f"⚠️ Cons: {', '.join(result.cons[:3])}")
        print(f"\n👥 Best for: {', '.join(result.lifestyle_fit[:3])}")

def main():
    parser = argparse.ArgumentParser(description="Neighborhood Reporter Agent")
    parser.add_argument("--neighborhood", "-n", default=DEFAULT_CONFIG["neighborhood"])
    parser.add_argument("--city", "-c", default=DEFAULT_CONFIG["city"])
    args = parser.parse_args()
    config = {"neighborhood": args.neighborhood, "city": args.city}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
