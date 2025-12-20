#!/usr/bin/env python3
"""Lesson 03: Parallel Steps - Concurrent execution."""

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


async def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        name="ParallelProcessor",
        model=model,
        instructions=["Process tasks in parallel."],
    )


async def run_parallel_tasks():
    """Run agents in parallel using asyncio."""
    model = get_model()
    
    # Create agents
    agent1 = Agent(name="Agent 1", model=model)
    agent2 = Agent(name="Agent 2", model=model)
    agent3 = Agent(name="Agent 3", model=model)

    print_section("Running in Parallel")

    # Run tasks concurrently
    tasks = [
        agent1.arun("Summarize AI in one sentence"),
        agent2.arun("Summarize cloud computing in one sentence"),
        agent3.arun("Summarize cybersecurity in one sentence"),
    ]

    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results, 1):
        print(f"Agent {i}: {result.content[:100]}...")


def main():
    parser = argparse.ArgumentParser(description="Parallel Steps Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 03: Parallel Steps")

    # Run the async function
    asyncio.run(run_parallel_tasks())


if __name__ == "__main__":
    main()
