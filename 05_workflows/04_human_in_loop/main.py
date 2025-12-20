#!/usr/bin/env python3
"""Lesson 04: Human in the Loop - Approval gates."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def main():
    parser = argparse.ArgumentParser(description="Human in the Loop Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 04: Human in the Loop")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    agent = Agent(name="Writer", model=model)

    print_section("Step 1: Generate Draft")
    draft = agent.run("Write a tweet about AI agents")
    print(f"Draft: {draft.content}")

    print_section("Human Approval")
    approval = input("\nApprove this draft? (y/n): ").strip().lower()

    if approval == "y":
        print("\n[Approved] Publishing tweet...")
    else:
        print("\n[Rejected] Generating revision...")
        revised = agent.run(f"Revise this tweet: {draft.content}")
        print(f"Revised: {revised.content}")


if __name__ == "__main__":
    main()
