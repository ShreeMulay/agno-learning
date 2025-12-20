#!/usr/bin/env python3
"""Lesson 03: Route Mode - Direct member responses."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.team import Team

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def main():
    parser = argparse.ArgumentParser(description="Route Mode Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 03: Route Mode")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    support = Agent(name="Support", role="Customer support", model=model)
    sales = Agent(name="Sales", role="Sales representative", model=model)

    team = Team(
        name="Customer Team",
        agents=[support, sales],
        model=model,
        respond_directly=True,  # Route mode
        show_tool_calls=True,
        markdown=True,
    )

    print_section("Route Mode Query")
    team.print_response("I have a question about pricing.")


if __name__ == "__main__":
    main()
