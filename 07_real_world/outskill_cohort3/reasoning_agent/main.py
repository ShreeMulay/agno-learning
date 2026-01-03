#!/usr/bin/env python3
"""Example: Reasoning Agent
Category: outskill_cohort3/reasoning

Demonstrates Agno's reasoning mode for solving complex logic puzzles.
The agent shows its step-by-step thinking process when solving problems.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section

PUZZLES = {
    "missionaries": (
        "Three missionaries and three cannibals need to cross a river. "
        "They have a boat that can carry up to two people at a time. "
        "If, at any time, the cannibals outnumber the missionaries on either side "
        "of the river, the cannibals will eat the missionaries. "
        "How can all six people get across the river safely? "
        "Provide a step-by-step solution."
    ),
    "towers": (
        "Solve the Tower of Hanoi puzzle with 3 disks. "
        "You have 3 pegs: A, B, and C. All disks start on peg A. "
        "Move all disks to peg C. You can only move one disk at a time, "
        "and you cannot place a larger disk on top of a smaller one. "
        "Show each move."
    ),
    "knights": (
        "On a 3x3 chessboard, place the maximum number of knights "
        "such that no knight attacks another. "
        "Show the board configuration and explain why this is the maximum."
    ),
}


def create_agent(model):
    return Agent(
        name="ReasoningAgent",
        model=model,
        reasoning=True,
        markdown=True,
        structured_outputs=True,
    )


def get_agent(model=None):
    if model is None:
        model = get_model()
    return create_agent(model)


def main():
    parser = argparse.ArgumentParser(
        description="Solve logic puzzles with reasoning mode"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--puzzle",
        type=str,
        choices=list(PUZZLES.keys()) + ["custom"],
        default="missionaries",
        help="Puzzle to solve"
    )
    parser.add_argument(
        "--custom",
        type=str,
        default="",
        help="Custom puzzle description (use with --puzzle custom)"
    )
    
    args = parser.parse_args()
    
    print_header("Reasoning Agent")
    
    if args.puzzle == "custom":
        if not args.custom:
            print("Error: --custom required when using --puzzle custom")
            sys.exit(1)
        puzzle = args.custom
    else:
        puzzle = PUZZLES[args.puzzle]
    
    print_section("Puzzle")
    print(f"  {puzzle[:100]}..." if len(puzzle) > 100 else f"  {puzzle}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model)
    
    print_section("Solving with Reasoning Mode...")
    
    try:
        response = agent.run(puzzle)
        
        print_section("Solution")
        print(response.content)
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
