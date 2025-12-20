#!/usr/bin/env python3
"""
Lesson 03: Structured Output

Concepts covered:
- Using Pydantic models for type-safe responses
- The output_schema parameter (formerly response_model)
- Field descriptions for better LLM understanding
- Accessing structured data from responses

Note: Structured output works best with models that support JSON mode.
      OpenAI models (gpt-4o, gpt-4o-mini) have excellent structured output support.
      Claude via OpenRouter may not always return valid JSON.

Run: python main.py --movie "The Matrix"
     python main.py --recipe "chocolate cake"
     python main.py --provider openai --movie "The Matrix"  # Best results
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


# Define structured output models
class MovieReview(BaseModel):
    """A structured movie review."""
    
    title: str = Field(description="The movie title")
    year: Optional[int] = Field(description="Release year if known", default=None)
    genre: str = Field(description="Primary genre (action, comedy, drama, etc.)")
    rating: int = Field(description="Rating from 1-10", ge=1, le=10)
    summary: str = Field(description="Brief plot summary (2-3 sentences)")
    strengths: list[str] = Field(description="Top 3 strengths of the movie")
    weaknesses: list[str] = Field(description="Top 2 weaknesses or criticisms")
    recommendation: str = Field(description="Who would enjoy this movie")


class Recipe(BaseModel):
    """A cooking recipe."""
    
    name: str = Field(description="Name of the dish")
    cuisine: str = Field(description="Type of cuisine (Italian, Mexican, etc.)")
    difficulty: str = Field(description="easy, medium, or hard")
    prep_time_minutes: int = Field(description="Preparation time in minutes", ge=0)
    cook_time_minutes: int = Field(description="Cooking time in minutes", ge=0)
    servings: int = Field(description="Number of servings", ge=1)
    ingredients: list[str] = Field(description="List of ingredients with quantities")
    steps: list[str] = Field(description="Step-by-step cooking instructions")
    tips: Optional[str] = Field(description="Optional cooking tips", default=None)


from typing import Union


def analyze_movie(model, movie_name: str) -> Union[MovieReview, str]:
    """Analyze a movie and return structured review (or string if parsing fails)."""
    agent = get_movie_agent(model)
    
    response = agent.run(f"Please review the movie: {movie_name}")
    return response.content


def get_recipe(model, dish_name: str) -> Union[Recipe, str]:
    """Get a recipe and return structured output (or string if parsing fails)."""
    agent = get_recipe_agent(model)
    
    response = agent.run(f"Please give me a recipe for: {dish_name}")
    return response.content


def display_movie_review(review: MovieReview) -> None:
    """Display a movie review in a nice format."""
    print(f"\n  Title: {review.title}", end="")
    if review.year:
        print(f" ({review.year})")
    else:
        print()
    print(f"  Genre: {review.genre}")
    print(f"  Rating: {'*' * review.rating}{'.' * (10 - review.rating)} ({review.rating}/10)")
    print()
    print(f"  Summary:")
    print(f"    {review.summary}")
    print()
    print(f"  Strengths:")
    for strength in review.strengths:
        print(f"    + {strength}")
    print()
    print(f"  Weaknesses:")
    for weakness in review.weaknesses:
        print(f"    - {weakness}")
    print()
    print(f"  Recommended for: {review.recommendation}")


def display_recipe(recipe: Recipe) -> None:
    """Display a recipe in a nice format."""
    print(f"\n  {recipe.name}")
    print(f"  {recipe.cuisine} cuisine | {recipe.difficulty} | Serves {recipe.servings}")
    print(f"  Prep: {recipe.prep_time_minutes} min | Cook: {recipe.cook_time_minutes} min")
    print()
    print("  Ingredients:")
    for ingredient in recipe.ingredients:
        print(f"    - {ingredient}")
    print()
    print("  Instructions:")
    for i, step in enumerate(recipe.steps, 1):
        print(f"    {i}. {step}")
    if recipe.tips:
        print()
        print(f"  Chef's tip: {recipe.tips}")



def get_movie_agent(model):
    """Create an agent for movie reviews with structured output."""
    return Agent(
        model=model,
        instructions=[
            "You are a professional movie critic.",
            "Provide thoughtful, balanced reviews.",
            "Always respond with valid JSON matching the schema.",
        ],
        output_schema=MovieReview,
        use_json_mode=True,  # Helps ensure JSON output
    )


def get_recipe_agent(model):
    """Create an agent for recipes with structured output."""
    return Agent(
        model=model,
        instructions=[
            "You are a professional chef.",
            "Provide detailed, easy-to-follow recipes.",
            "Always respond with valid JSON matching the schema.",
        ],
        output_schema=Recipe,
        use_json_mode=True,  # Helps ensure JSON output
    )


def main():
    """Demonstrate structured output with Pydantic models."""
    parser = argparse.ArgumentParser(
        description="Get structured output from agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--movie",
        type=str,
        help="Movie to review (e.g., 'The Matrix')",
    )
    parser.add_argument(
        "--recipe",
        type=str,
        help="Dish to get recipe for (e.g., 'chocolate cake')",
    )
    args = parser.parse_args()

    # Default to movie if nothing specified
    if not args.movie and not args.recipe:
        args.movie = "Inception"

    print_header("Lesson 03: Structured Output")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.movie:
        print_section(f"Movie Review: {args.movie}")
        print("Analyzing (this may take a moment)...", flush=True)
        
        review = analyze_movie(model, args.movie)
        
        # Check if we got structured output or a string fallback
        if isinstance(review, MovieReview):
            display_movie_review(review)
            
            # Show the raw object too
            print()
            print_section("Raw Pydantic Object")
            print(f"  Type: {type(review).__name__}")
            print(f"  Fields: {list(review.model_fields.keys())}")
            print(f"  review.rating = {review.rating}")
            print(f"  review.strengths[0] = {review.strengths[0]!r}")
        else:
            # Fallback: the model returned plain text
            print("\n  Note: Model returned plain text instead of structured JSON.")
            print("  This can happen with some providers (e.g., Claude via OpenRouter).")
            print("  Try: python main.py --provider openai --movie \"Inception\"")
            print()
            print("  Response:")
            print("  " + "-" * 40)
            print(f"  {review[:500]}..." if len(str(review)) > 500 else f"  {review}")

    if args.recipe:
        print_section(f"Recipe: {args.recipe}")
        print("Generating recipe (this may take a moment)...", flush=True)
        
        recipe = get_recipe(model, args.recipe)
        
        if isinstance(recipe, Recipe):
            display_recipe(recipe)
        else:
            print("\n  Note: Model returned plain text instead of structured JSON.")
            print("  Try: python main.py --provider openai --recipe \"chocolate cake\"")
            print()
            print("  Response:")
            print("  " + "-" * 40)
            print(f"  {recipe[:500]}..." if len(str(recipe)) > 500 else f"  {recipe}")


if __name__ == "__main__":
    main()
