#!/usr/bin/env python3
"""Lesson 04: Collaborate Mode - Parallel execution."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.team import Team

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def main():
    parser = argparse.ArgumentParser(description="Collaborate Mode Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 04: Collaborate Mode")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    tech = Agent(name="Tech", role="Technical reviewer", model=model)
    legal = Agent(name="Legal", role="Legal reviewer", model=model)
    finance = Agent(name="Finance", role="Financial reviewer", model=model)

    team = Team(
        name="Review Team",
        agents=[tech, legal, finance],
        model=model,
        delegate_to_all_members=True,  # Collaborate mode
        show_tool_calls=True,
        markdown=True,
    )

    print_section("Parallel Review")
    team.print_response("Review this contract proposal from all perspectives.")


if __name__ == "__main__":
    main()
