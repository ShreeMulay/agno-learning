#!/usr/bin/env python3
"""Example #101: Movie Script Generator
Category: outskill_cohort3/structured_output

DESCRIPTION:
Generates creative movie scripts with structured output using Pydantic models.
Given a setting or theme, the agent creates a complete movie concept including
characters, storyline, genre, and ending.

PATTERNS:
- Structured Output (Pydantic response models)
- Creative Writing (generative content)

ARGUMENTS:
- setting (str): The movie setting or theme. Default: "New York"
- genre (str): Preferred genre hint. Default: ""
- num_characters (int): Number of main characters. Default: 5
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

DEFAULT_CONFIG = {
    "setting": "New York",
    "genre": "",
    "num_characters": 5,
}

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from pydantic import BaseModel, Field

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


class MovieScript(BaseModel):
    """Structured movie script output."""
    name: str = Field(description="Creative movie title")
    setting: str = Field(description="Detailed setting for the movie")
    genre: str = Field(description="Movie genre (action, thriller, comedy, drama, etc.)")
    characters: list[str] = Field(description="List of main character names")
    storyline: str = Field(description="3-5 sentence compelling storyline")
    ending: str = Field(description="How the movie ends")


def create_agent(model):
    """Create the movie script generator agent."""
    return Agent(
        name="MovieScriptGenerator",
        model=model,
        description="You are a creative Hollywood screenwriter.",
        instructions=[
            "Create compelling, original movie concepts.",
            "Make characters memorable and distinct.",
            "The storyline should have conflict and resolution.",
            "Match the genre to the setting appropriately.",
            "Endings should be satisfying and fit the genre.",
        ],
        response_model=MovieScript,
        markdown=True,
    )


def get_agent(model=None):
    """Get agent instance for GUI integration."""
    if model is None:
        model = get_model()
    return create_agent(model)


def main():
    parser = argparse.ArgumentParser(
        description="Generate creative movie scripts with AI"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--setting",
        type=str,
        default=DEFAULT_CONFIG["setting"],
        help="Movie setting or theme (e.g., 'Tokyo 2050', 'Medieval castle')"
    )
    parser.add_argument(
        "--genre",
        type=str,
        default=DEFAULT_CONFIG["genre"],
        help="Preferred genre (optional, AI will choose if not specified)"
    )
    parser.add_argument(
        "--num-characters",
        type=int,
        default=DEFAULT_CONFIG["num_characters"],
        help="Number of main characters to include"
    )
    
    args = parser.parse_args()
    
    print_header("Movie Script Generator")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model)
    
    prompt = f"Create a movie script set in: {args.setting}"
    if args.genre:
        prompt += f"\nPreferred genre: {args.genre}"
    prompt += f"\nInclude {args.num_characters} main characters."
    
    print_section("Input")
    print(f"  Setting: {args.setting}")
    if args.genre:
        print(f"  Genre: {args.genre}")
    print(f"  Characters: {args.num_characters}")
    print()
    
    print_section("Generating...")
    
    try:
        response = agent.run(prompt)
        script = response.content
        
        print_section(f"🎬 {script.name}")
        print(f"\n  Genre: {script.genre}")
        print(f"  Setting: {script.setting}")
        
        print_section("Characters")
        for i, char in enumerate(script.characters, 1):
            print(f"  {i}. {char}")
        
        print_section("Storyline")
        print(f"  {script.storyline}")
        
        print_section("Ending")
        print(f"  {script.ending}")
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
