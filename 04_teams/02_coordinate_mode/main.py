#!/usr/bin/env python3
"""Lesson 02: Coordinate Mode - Leader-coordinated teams."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.team import Team

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Team(
        name="Strategy Team",
        members=[analyst, strategist],
        model=model,
        # Coordinate mode is the default
        
        markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Coordinate Mode Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 02: Coordinate Mode")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    analyst = Agent(name="Analyst", role="Data analyst", model=model)
    strategist = Agent(name="Strategist", role="Business strategist", model=model)

    team = get_agent(model)

    print_section("Coordinated Task")
    team.print_response("Analyze the market for electric vehicles and suggest a strategy.")


if __name__ == "__main__":
    main()
