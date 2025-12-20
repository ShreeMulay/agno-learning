#!/usr/bin/env python3
"""Lesson 01: Basic Workflow - Sequential steps."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.workflow import Workflow

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def main():
    parser = argparse.ArgumentParser(description="Basic Workflow Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 01: Basic Workflow")

    model = get_model(args.provider, args.model, temperature=args.temperature)

    # Create agents for each step
    researcher = Agent(name="Researcher", model=model)
    writer = Agent(name="Writer", model=model)

    print_section("Running Workflow")
    print("Step 1: Research")
    research = researcher.run("Research the benefits of meditation")
    print(f"  Result: {research.content[:100]}...")

    print("\nStep 2: Write")
    article = writer.run(f"Write a short article based on: {research.content}")
    print(f"  Result: {article.content[:200]}...")


if __name__ == "__main__":
    main()
