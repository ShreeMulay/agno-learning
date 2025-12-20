#!/usr/bin/env python3
"""
Lesson 01: Session State - Persistent storage within a conversation.

Session state allows tools to read and modify shared state during a session.
Key requirements for state persistence across multiple runs:
  1. Use SqliteDb (or another db) for persistence
  2. Use session_id to identify the session
  3. Initialize session_state with default values

Run: python main.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
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


# Database path for session persistence
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "tmp" / "session_state.db"


def get_agent(model=None, db_path=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    if db_path is None:
        db_path = DB_PATH
    
    # Ensure tmp directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    return Agent(
        model=model,
        # Database is REQUIRED for state to persist across print_response() calls
        db=SqliteDb(db_file=str(db_path)),
        tools=[increment_counter, add_item, get_state],
        # Default session state - this is the initial state for new sessions
        session_state={"counter": 0, "items": []},
        instructions=[
            "You can track a counter and a list of items.",
            "Use the tools to modify state. Current state: counter={counter}, items={items}",
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
