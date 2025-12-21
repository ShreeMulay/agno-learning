"""
Example #203: Poem Composer Agent
Category: personal/creative
DESCRIPTION: Composes poetry in various styles and forms based on themes and emotions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"style": "free_verse"}

class Poem(BaseModel):
    title: str = Field(description="Poem title")
    style: str = Field(description="Poetry style/form")
    poem_text: str = Field(description="The complete poem")
    themes: list[str] = Field(description="Central themes")
    imagery: list[str] = Field(description="Key images used")
    mood: str = Field(description="Overall emotional tone")
    literary_devices: list[str] = Field(description="Devices used: metaphor, alliteration, etc")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Poem Composer",
        instructions=[
            f"You compose poetry in {cfg['style']} style.",
            "Use vivid imagery and sensory language.",
            "Employ literary devices effectively.",
            "Create emotional resonance with readers.",
            "Follow form conventions when applicable.",
        ],
        output_schema=Poem,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Poem Composer - Demo")
    print("=" * 60)
    query = """Write a poem about:
    Theme: The passage of time and changing seasons
    Mood: Nostalgic but hopeful
    Include imagery of autumn transitioning to winter"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, Poem):
        print(f"\n🎭 {result.title}")
        print(f"   Style: {result.style} | Mood: {result.mood}")
        print(f"\n{result.poem_text}")
        print(f"\n✨ Literary Devices: {', '.join(result.literary_devices)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", "-s", default=DEFAULT_CONFIG["style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"style": args.style}), {"style": args.style})

if __name__ == "__main__": main()
