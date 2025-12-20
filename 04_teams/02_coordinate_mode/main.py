#!/usr/bin/env python3
"""Lesson 02: Coordinate Mode - Leader-coordinated teams.

Coordinate mode (default) uses a team leader to delegate tasks to members.
The leader decides which member to use for each subtask.

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
    """Create a coordinated team for the API."""
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    
    # Create specialized agents
    analyst = Agent(
        name="Analyst",
        role="Data analyst",
        model=model,
        instructions=[
            "You analyze data and market trends.",
            "Provide clear, data-driven insights.",
            "Include relevant statistics when available.",
        ],
    )
    
    strategist = Agent(
        name="Strategist",
        role="Business strategist",
        model=model,
        instructions=[
            "You develop business strategies based on analysis.",
            "Focus on actionable recommendations.",
            "Consider risks and opportunities.",
        ],
    )
    
    return Team(
        name="Strategy Team",
        members=[analyst, strategist],
        model=model,
        # Coordinate mode is the default - leader delegates to members
        instructions=[
            "You coordinate analysis and strategy development.",
            "First delegate research to the Analyst.",
            "Then have the Strategist develop recommendations based on analysis.",
            "Present the final strategy with supporting data.",
        ],
        markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Coordinate Mode Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 02: Coordinate Mode")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    team = get_agent(model)

    print_section("Coordinated Task")
    print("Query: Analyze the market for electric vehicles and suggest a strategy.\n")
    team.print_response("Analyze the market for electric vehicles and suggest a strategy.")


if __name__ == "__main__":
    main()
