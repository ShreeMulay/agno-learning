"""
Example #208: Plot Outliner Agent
Category: personal/creative
DESCRIPTION: Creates structured story outlines with plot points, arcs, and pacing
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"structure": "three_act"}

class PlotPoint(BaseModel):
    name: str = Field(description="Plot point name")
    description: str = Field(description="What happens")
    purpose: str = Field(description="Why this matters to the story")
    chapter_estimate: str = Field(description="Approximate chapter/section")

class PlotOutline(BaseModel):
    title: str = Field(description="Working title")
    logline: str = Field(description="One-sentence summary")
    genre: str = Field(description="Story genre")
    structure: str = Field(description="Story structure used")
    plot_points: list[PlotPoint] = Field(description="Key plot points")
    subplots: list[str] = Field(description="Secondary storylines")
    theme: str = Field(description="Central theme")
    climax: str = Field(description="The climactic moment")
    resolution: str = Field(description="How it ends")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Plot Outliner",
        instructions=[
            f"You create plot outlines using {cfg['structure']} structure.",
            "Build tension through well-paced plot points.",
            "Include meaningful subplots that support the main story.",
            "Create satisfying climaxes and resolutions.",
            "Ensure thematic consistency throughout.",
        ],
        output_schema=PlotOutline,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Plot Outliner - Demo")
    print("=" * 60)
    query = """Create a plot outline:
    Premise: A burned-out teacher discovers one of her students 
    is a time traveler trying to prevent a disaster
    Genre: Sci-fi drama
    Target length: Novel (~80k words)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PlotOutline):
        print(f"\n📖 {result.title}")
        print(f"   {result.logline}")
        print(f"\n🎭 Genre: {result.genre} | Structure: {result.structure}")
        print(f"\n📋 Plot Points:")
        for pp in result.plot_points:
            print(f"\n  🔹 {pp.name} ({pp.chapter_estimate})")
            print(f"     {pp.description}")
        print(f"\n⚡ Climax: {result.climax}")
        print(f"🎯 Theme: {result.theme}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--structure", "-s", default=DEFAULT_CONFIG["structure"])
    args = parser.parse_args()
    run_demo(get_agent(config={"structure": args.structure}), {"structure": args.structure})

if __name__ == "__main__": main()
