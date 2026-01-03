#!/usr/bin/env python3
"""Example: HackerNews Agent
Category: outskill_cohort3/custom_tools

Demonstrates creating a custom function tool that the agent can call.
Fetches and summarizes top stories from Hacker News.
"""

import argparse
import json
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section

DEFAULT_CONFIG = {
    "num_stories": 5,
}


def get_top_hackernews_stories(num_stories: int = 10) -> str:
    """Fetch top stories from Hacker News.
    
    Args:
        num_stories: Number of stories to return. Defaults to 10.
    
    Returns:
        JSON string of top stories with title, url, score, and author.
    """
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()
    
    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        story.pop("text", None)
        story.pop("kids", None)
        stories.append(story)
    
    return json.dumps(stories)


def create_agent(model):
    return Agent(
        name="HackerNewsAgent",
        model=model,
        tools=[get_top_hackernews_stories],
        instructions=[
            "Use the HackerNews tool to fetch stories",
            "Summarize each story with its title, score, and a brief description",
            "Include the URL for each story",
        ],
        markdown=True,
    )


def get_agent(model=None):
    if model is None:
        model = get_model()
    return create_agent(model)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch and summarize top HackerNews stories"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--num-stories",
        type=int,
        default=DEFAULT_CONFIG["num_stories"],
        help="Number of stories to fetch"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="",
        help="Optional: filter for specific topic"
    )
    
    args = parser.parse_args()
    
    print_header("HackerNews Agent")
    
    print_section("Request")
    print(f"  Stories: {args.num_stories}")
    if args.topic:
        print(f"  Topic filter: {args.topic}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model)
    
    if args.topic:
        prompt = f"Get the top {args.num_stories} HackerNews stories and highlight any related to: {args.topic}"
    else:
        prompt = f"Summarize the top {args.num_stories} stories on HackerNews right now"
    
    print_section("Fetching...")
    
    try:
        response = agent.run(prompt)
        
        print_section("Top Stories")
        print(response.content)
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
