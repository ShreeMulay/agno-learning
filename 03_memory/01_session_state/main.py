#!/usr/bin/env python3
"""
Lesson 01: Session State - In-memory storage within a conversation.

Run: python main.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.run import RunContext

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section, check_openrouter_runcontext_error


def increment_counter(run_context: RunContext) -> str:
    """Increment the counter and return the new value."""
    run_context.session_state["counter"] += 1
    return f"Counter is now {run_context.session_state['counter']}"


def add_item(run_context: RunContext, item: str) -> str:
    """Add an item to the list."""
    run_context.session_state["items"].append(item)
    return f"Added '{item}'. Items: {run_context.session_state['items']}"


def get_state(run_context: RunContext) -> str:
    """Get the current state."""
    return f"Counter: {run_context.session_state['counter']}, Items: {run_context.session_state['items']}"



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        model=model,
        tools=[increment_counter, add_item, get_state],
        session_state={"counter": 0, "items": []},
        instructions=[
            "You can track a counter and a list of items.",
            "Current state: counter={counter}, items={items}",
        ],
        markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Session State Demo")
    add_model_args(parser)
    args = parser.parse_args()

    print_header("Lesson 01: Session State")
    
    # Warn about OpenRouter issues with RunContext tools
    provider = args.provider or "openrouter"
    check_openrouter_runcontext_error(provider)

    model = get_model(args.provider, args.model, temperature=args.temperature)

    agent = get_agent(model)

    queries = [
        "Increment the counter",
        "Add 'apple' to the items",
        "Increment again and add 'banana'",
        "What's the current state?",
    ]

    # session_id is required to persist session_state across multiple print_response calls
    session_id = "session-state-demo"
    for query in queries:
        print_section(f"User: {query}")
        agent.print_response(query, session_id=session_id)
        print()


if __name__ == "__main__":
    main()
