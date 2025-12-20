#!/usr/bin/env python3
"""
Lesson 02: User Memories - Persist preferences across sessions.

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



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        model=model,
db=SqliteDb(db_file=str(db_path
    )


def main():
    parser = argparse.ArgumentParser(description="User Memories Demo")
    add_model_args(parser)
    parser.add_argument("--user", default="demo_user", help="User ID")
    parser.add_argument("--clear", action="store_true", help="Clear memories")
    args = parser.parse_args()

    print_header("Lesson 02: User Memories")

    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / "agno.db"

    model = get_model(args.provider, args.model, temperature=args.temperature)

    agent = get_agent(model)),
        enable_user_memories=True,
        instructions=[
            "You remember user preferences and facts.",
            "Reference what you know about the user when relevant.",
        ],
        markdown=True,
    )

    print(f"User ID: {args.user}")
    print(f"Database: {db_path}")

    queries = [
        "My name is Alex and I prefer dark mode.",
        "I work as a software engineer.",
        "What do you remember about me?",
    ]

    for query in queries:
        print_section(f"User: {query}")
        agent.print_response(query, user_id=args.user)
        print()

    print_section("Key Points")
    print("- Memories persist in SQLite database")
    print("- Use user_id to separate users")
    print("- Agent automatically recalls relevant memories")


if __name__ == "__main__":
    main()
