"""
Example #201: Story Generator Agent
Category: personal/creative
DESCRIPTION: Generates creative short stories based on prompts, themes, and genres
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"genre": "fantasy"}

class Story(BaseModel):
    title: str = Field(description="Story title")
    genre: str = Field(description="Story genre")
    setting: str = Field(description="Time and place")
    protagonist: str = Field(description="Main character description")
    conflict: str = Field(description="Central conflict")
    story_text: str = Field(description="The complete short story")
    themes: list[str] = Field(description="Underlying themes")
    word_count: int = Field(description="Approximate word count")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Story Generator",
        instructions=[
            f"You generate compelling short stories in the {cfg['genre']} genre.",
            "Create vivid characters and immersive settings.",
            "Develop clear conflict and resolution arcs.",
            "Use descriptive, engaging prose.",
            "Keep stories between 500-1000 words.",
        ],
        output_schema=Story,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Story Generator - Demo")
    print("=" * 60)
    query = """Write a short story with these elements:
    - A reluctant hero
    - A mysterious forest
    - A lost artifact
    - Theme of self-discovery"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, Story):
        print(f"\n📖 {result.title}")
        print(f"   Genre: {result.genre} | Words: ~{result.word_count}")
        print(f"   Setting: {result.setting}")
        print(f"\n{result.story_text[:500]}...")
        print(f"\n🎭 Themes: {', '.join(result.themes)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--genre", "-g", default=DEFAULT_CONFIG["genre"])
    args = parser.parse_args()
    run_demo(get_agent(config={"genre": args.genre}), {"genre": args.genre})

if __name__ == "__main__": main()
