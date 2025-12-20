#!/usr/bin/env python3
"""Lesson 02: Conditional Flow - Branching logic."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def main():
    parser = argparse.ArgumentParser(description="Conditional Flow Demo")
    add_model_args(parser)
    parser.add_argument("--topic", default="technology", choices=["technology", "health", "sports"])
    args = parser.parse_args()

    print_header("Lesson 02: Conditional Flow")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    # Create specialized agents
    tech_agent = Agent(name="Tech Expert", model=model, instructions="You're a technology expert.")
    health_agent = Agent(name="Health Expert", model=model, instructions="You're a health expert.")
    sports_agent = Agent(name="Sports Expert", model=model, instructions="You're a sports expert.")

    # Conditional routing
    print_section(f"Topic: {args.topic}")
    
    if args.topic == "technology":
        agent = tech_agent
    elif args.topic == "health":
        agent = health_agent
    else:
        agent = sports_agent

    agent.print_response(f"Give me a tip about {args.topic}")


if __name__ == "__main__":
    main()
