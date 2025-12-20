#!/usr/bin/env python3
"""Lesson 01: Basic Team - Multi-agent collaboration."""

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
        name="Content Team",
        agents=[researcher, writer],
        model=model,
        instructions="Coordinate research and writing tasks.",
        show_tool_calls=True,
        markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Basic Team Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 01: Basic Team")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    # Create specialized agents
    researcher = Agent(
        name="Researcher",
        role="Research specialist",
        model=model,
        instructions="You research topics and provide facts.",
    )

    writer = Agent(
        name="Writer",
        role="Content writer",
        model=model,
        instructions="You write engaging content based on research.",
    )

    # Create a team
    team = get_agent(model)

    print_section("Team Query")
    query = "Write a short paragraph about the benefits of exercise."
    print(f"Query: {query}\n")
    
    team.print_response(query)


if __name__ == "__main__":
    main()
