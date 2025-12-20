#!/usr/bin/env python3
"""Lesson 03: Route Mode - Direct member responses.

Route mode (respond_directly=True) lets the selected member respond directly
to the user without the team leader summarizing or reformatting the response.

Run: python main.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.team import Team

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def get_agent(model=None):
    """Create a routed team for the API."""
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    
    # Create specialized agents
    support = Agent(
        name="Support",
        role="Customer support specialist",
        model=model,
        instructions=[
            "You handle technical issues and troubleshooting.",
            "Be helpful, patient, and thorough.",
            "Escalate complex issues when needed.",
        ],
    )
    
    sales = Agent(
        name="Sales",
        role="Sales representative",
        model=model,
        instructions=[
            "You handle pricing, plans, and purchasing questions.",
            "Be friendly and informative about product options.",
            "Focus on understanding customer needs.",
        ],
    )
    
    return Team(
        name="Customer Team",
        members=[support, sales],
        model=model,
        # Route mode - selected member responds directly to user
        respond_directly=True,
        instructions=[
            "Route customer queries to the appropriate team member.",
            "Support handles technical issues, Sales handles pricing/purchasing.",
        ],
        markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Route Mode Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 03: Route Mode")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    team = get_agent(model)

    print_section("Route Mode Query")
    print("Query: I have a question about pricing.\n")
    team.print_response("I have a question about pricing.")


if __name__ == "__main__":
    main()
