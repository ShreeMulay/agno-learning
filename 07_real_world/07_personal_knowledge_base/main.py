#!/usr/bin/env python3
"""Example 07: Personal Knowledge Base - Agent that learns about users.

An agent that remembers user information and provides personalized responses.

Run with:
    python main.py --user alice
"""

import argparse
import sys
from pathlib import Path
import uuid

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import AgentMemory

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_personal_agent(model, user_id: str):
    """Create an agent with personal memory capabilities."""
    
    # Ensure tmp directory exists
    Path("tmp").mkdir(exist_ok=True)
    
    # Database for persistence
    db = SqliteDb(
        id=f"personal_kb_{user_id}",
        db_file=f"tmp/personal_{user_id}.db",
    )
    
    # Create agent with memory features
    agent = get_agent(model)
    
    return agent



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        name="PersonalAssistant",
model=model,
db=db,
# Enable conversation history
add_history_to_context=True,
num_history_runs=10,
# Enable user memories
add_memories_to_context=True,
create_user_memories=True,  # Automatically create memories
update_user_memories_after_run=True,
instructions=[
"You are a personal assistant that remembers user information.",
"Pay attention to personal details shared by the user.",
"Use what you know about the user to personalize responses.",
"When asked what you know, summarize stored information.",
"Be conversational and build rapport over time.",
],
markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Personal Knowledge Base")
    add_model_args(parser)
    parser.add_argument(
        "--user", "-u", type=str, default=None,
        help="User ID for memory persistence"
    )
    args = parser.parse_args()

    print_header("Personal Knowledge Base")
    
    # User identification
    user_id = args.user or f"user_{uuid.uuid4().hex[:6]}"
    session_id = f"session_{user_id}"
    
    print_section("User Profile")
    print(f"  User ID: {user_id}")
    print(f"  Session: {session_id}")
    print(f"  Database: tmp/personal_{user_id}.db")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_personal_agent(model, user_id)
    
    print_section("Interactive Mode")
    print("  Share information about yourself!")
    print("  The agent will remember details over time.")
    print()
    print("  Try:")
    print("  - 'My name is [your name]'")
    print("  - 'I work as a [job]'")
    print("  - 'My favorite [thing] is [value]'")
    print("  - 'What do you know about me?'")
    print()
    print("  Type 'quit' to exit, 'clear' to forget\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! I'll remember our conversation.")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("Goodbye! I'll remember our conversation.")
            break
        
        if user_input.lower() == 'clear':
            # Note: Actual memory clearing would require DB operations
            print("  (Memory clearing not implemented in this demo)")
            continue
        
        if user_input.lower() == 'memories':
            # Show what the agent knows
            response = agent.run(
                "List everything you remember about me in bullet points.",
                session_id=session_id,
                user_id=user_id,
            )
            print(f"\n{response.content}\n")
            continue
        
        # Regular interaction with memory
        response = agent.run(
            user_input,
            session_id=session_id,
            user_id=user_id,
        )
        print(f"\nAssistant: {response.content}\n")


if __name__ == "__main__":
    main()
