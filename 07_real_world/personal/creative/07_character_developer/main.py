"""
Example #207: Character Developer Agent
Category: personal/creative
DESCRIPTION: Creates detailed character profiles for fiction writing with depth and consistency
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"genre": "contemporary"}

class Character(BaseModel):
    name: str = Field(description="Character's full name")
    age: int = Field(description="Character's age")
    occupation: str = Field(description="Job or role")
    appearance: str = Field(description="Physical description")
    personality: str = Field(description="Core personality traits")
    backstory: str = Field(description="Relevant history")
    motivation: str = Field(description="What drives them")
    flaw: str = Field(description="Character flaw or weakness")
    strength: str = Field(description="Key strength or talent")
    speech_pattern: str = Field(description="How they talk")
    relationships: list[str] = Field(description="Key relationships")
    arc_potential: str = Field(description="How they might grow/change")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Character Developer",
        instructions=[
            f"You create characters for {cfg['genre']} fiction.",
            "Build multi-dimensional, believable characters.",
            "Balance strengths with meaningful flaws.",
            "Create backstories that inform present behavior.",
            "Design characters with growth potential.",
        ],
        output_schema=Character,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Character Developer - Demo")
    print("=" * 60)
    query = """Create a character:
    Role: Protagonist for a thriller
    Requirements: 
    - Mid-30s professional
    - Has a secret from their past
    - Reluctant to trust others
    - Must overcome fear to save someone"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, Character):
        print(f"\n👤 {result.name}, {result.age}")
        print(f"   {result.occupation}")
        print(f"\n📝 Appearance: {result.appearance}")
        print(f"\n🎭 Personality: {result.personality}")
        print(f"\n⚡ Motivation: {result.motivation}")
        print(f"💔 Flaw: {result.flaw}")
        print(f"💪 Strength: {result.strength}")
        print(f"\n📖 Arc Potential: {result.arc_potential}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--genre", "-g", default=DEFAULT_CONFIG["genre"])
    args = parser.parse_args()
    run_demo(get_agent(config={"genre": args.genre}), {"genre": args.genre})

if __name__ == "__main__": main()
