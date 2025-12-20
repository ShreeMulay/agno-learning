#!/usr/bin/env python3
"""
Lesson 03: Agentic Memory - Agent-controlled memory management.

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
    parser = argparse.ArgumentParser(description="Agentic Memory Demo")
    add_model_args(parser)
    parser.add_argument("--user", default="demo_user", help="User ID")
    args = parser.parse_args()

    print_header("Lesson 03: Agentic Memory")

    project_root = Path(__file__).parent.parent.parent
    db_path = project_root / "agno.db"

    model = get_model(args.provider, args.model, temperature=args.temperature)

    agent = get_agent(model)),
        enable_agentic_memory=True,  # Agent controls memory
        instructions=[
            "You have tools to manage memories.",
            "Remember important user information.",
            "Update or delete memories as needed.",
        ],
        show_tool_calls=True,
        markdown=True,
    )

    print(f"User ID: {args.user}")

    queries = [
        "Remember that I'm allergic to peanuts - this is important!",
        "Actually, I'm also allergic to shellfish.",
        "What allergies do you have recorded for me?",
    ]

    for query in queries:
        print_section(f"User: {query}")
        agent.print_response(query, user_id=args.user)
        print()

    print_section("Agentic vs Automatic Memory")
    print("enable_user_memories: Agent remembers after every response")
    print("enable_agentic_memory: Agent decides when to remember")


if __name__ == "__main__":
    main()
