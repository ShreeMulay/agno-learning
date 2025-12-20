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
    
    # Create specialized agents
    researcher = Agent(
        name="Researcher",
        role="Research specialist",
        model=model,
        instructions=[
            "You research topics and provide detailed, accurate facts.",
            "Present findings in a clear, organized format.",
            "Include key statistics or evidence when available.",
        ],
    )

    writer = Agent(
        name="Writer",
        role="Content writer",
        model=model,
        instructions=[
            "You write engaging content based on provided research.",
            "Make content accessible to a general audience.",
            "Return ONLY the final written content, no meta-commentary.",
        ],
    )

    # Return the team (which behaves like an agent)
    return Team(
        members=[researcher, writer],
        name="Content Team",
        model=model,
        instructions=[
            "You coordinate the researcher and writer to produce quality content.",
            "First delegate research, then delegate writing based on that research.",
        ],
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
        instructions=[
            "You research topics and provide detailed, accurate facts.",
            "Present findings in a clear, organized format.",
            "Include key statistics or evidence when available.",
        ],
    )

    writer = Agent(
        name="Writer",
        role="Content writer",
        model=model,
        instructions=[
            "You write engaging, polished content based on provided research.",
            "Make content accessible to a general audience.",
            "Return ONLY the final written content, no meta-commentary.",
        ],
    )

    # Create a team (note: 'members' is the new parameter name, not 'agents')
    team = Team(
        members=[researcher, writer],
        name="Content Team",
        model=model,
        instructions=[
            "You coordinate the researcher and writer to produce quality content.",
            "First delegate research, then delegate writing based on that research.",
            "IMPORTANT: Your final response must include the ACTUAL content produced.",
            "Do not just describe what was done - show the final written output.",
        ],
        markdown=True,
    )

    print_section("Team Query")
    query = "Write a short paragraph about the benefits of exercise."
    print(f"Query: {query}\n")
    
    team.print_response(query)


if __name__ == "__main__":
    main()
