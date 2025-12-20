#!/usr/bin/env python3
"""
Lesson 04: Conversation History - Multi-turn context.

Run: python main.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def main():
    parser = argparse.ArgumentParser(description="Conversation History Demo")
    add_model_args(parser)
    parser.add_argument("--session", default="demo_session", help="Session ID")
    args = parser.parse_args()

    print_header("Lesson 04: Conversation History")

    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / "agno.db"

    model = get_model(args.provider, args.model, temperature=args.temperature)

    agent = Agent(
        model=model,
        db=SqliteDb(db_file=str(db_path)),
        add_history_to_context=True,
        num_history_runs=10,
        instructions=[
            "You maintain context across the conversation.",
            "Reference previous messages when relevant.",
        ],
        markdown=True,
    )

    print(f"Session ID: {args.session}")

    # Simulate a multi-turn conversation
    queries = [
        "I'm planning a trip to Japan.",
        "What's the best time to visit?",
        "What about the cherry blossoms?",
        "Summarize our conversation so far.",
    ]

    for query in queries:
        print_section(f"User: {query}")
        agent.print_response(query, session_id=args.session)
        print()

    print_section("History Features")
    print("- add_history_to_context: Include previous turns")
    print("- num_history_runs: Limit context window")
    print("- session_id: Separate conversation threads")


if __name__ == "__main__":
    main()
