"""
Example #159: Local Guide Agent
Category: industry/travel
DESCRIPTION: Provides local insider knowledge and recommendations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"city": "Lisbon", "interest": "food and wine"}

class LocalSpot(BaseModel):
    name: str = Field(description="Place name")
    type: str = Field(description="Type of place")
    neighborhood: str = Field(description="Neighborhood")
    why_special: str = Field(description="What makes it special")
    best_time: str = Field(description="Best time to visit")
    local_tip: str = Field(description="Insider tip")

class LocalGuide(BaseModel):
    city: str = Field(description="City")
    local_vibe: str = Field(description="City vibe description")
    hidden_gems: list[LocalSpot] = Field(description="Hidden gems")
    neighborhoods: list[str] = Field(description="Best neighborhoods to explore")
    local_customs: list[str] = Field(description="Local customs and etiquette")
    phrases: list[str] = Field(description="Useful local phrases")
    scams_to_avoid: list[str] = Field(description="Tourist scams to avoid")
    best_local_experiences: list[str] = Field(description="Authentic experiences")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Local Guide",
        instructions=[
            "You are a knowledgeable local guide.",
            f"Share insider knowledge about {cfg['city']}",
            f"Focus on {cfg['interest']} experiences",
            "Reveal hidden gems tourists don't know",
            "Provide cultural context and etiquette",
            "Warn about common tourist traps",
        ],
        output_schema=LocalGuide,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Local Guide Agent - Demo")
    print("=" * 60)
    query = f"""Be my local guide for:
- City: {config['city']}
- Interests: {config['interest']}

Share hidden gems and insider knowledge."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, LocalGuide):
        print(f"\n📍 {result.city}")
        print(f"🌆 Vibe: {result.local_vibe}")
        print(f"\n💎 Hidden Gems:")
        for spot in result.hidden_gems[:3]:
            print(f"  • {spot.name} ({spot.type}) - {spot.neighborhood}")
            print(f"    ✨ {spot.why_special}")
            print(f"    💡 Tip: {spot.local_tip}")
        print(f"\n🗣️ Useful Phrases:")
        for phrase in result.phrases[:3]:
            print(f"  • {phrase}")
        print(f"\n⚠️ Watch Out:")
        for scam in result.scams_to_avoid[:2]:
            print(f"  • {scam}")

def main():
    parser = argparse.ArgumentParser(description="Local Guide Agent")
    parser.add_argument("--city", "-c", default=DEFAULT_CONFIG["city"])
    parser.add_argument("--interest", "-i", default=DEFAULT_CONFIG["interest"])
    args = parser.parse_args()
    config = {"city": args.city, "interest": args.interest}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
