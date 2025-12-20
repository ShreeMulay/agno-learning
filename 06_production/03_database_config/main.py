#!/usr/bin/env python3
"""Lesson 03: Database Configuration - Persist sessions and memories.

This example demonstrates configuring database storage for
agent sessions, history, and user memories.

Run with:
    python main.py
"""

import argparse
import sys
from pathlib import Path
import uuid

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
        name="PersistentAssistant",
model=model,
db=db,
# Enable history from database
add_history_to_context=True,
num_history_runs=5,  # Include last 5 messages
# Enable user memories
add_memories_to_context=True,
markdown=True,
    )


def main():
    parser = argparse.ArgumentParser(description="Database Configuration Demo")
    add_model_args(parser)
    parser.add_argument(
        "--session-id", type=str, default=None,
        help="Session ID to continue (generates new if not provided)"
    )
    args = parser.parse_args()

    print_header("Lesson 03: Database Configuration")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    
    # Ensure tmp directory exists
    Path("tmp").mkdir(exist_ok=True)
    
    # Configure SQLite database
    db = SqliteDb(
        id="learning_db",
        db_file="tmp/agent_sessions.db",
        session_table="agent_sessions",  # Custom table name
    )
    
    print_section("Database Configuration")
    print(f"  Type: SQLite")
    print(f"  File: tmp/agent_sessions.db")
    print(f"  Table: agent_sessions")
    
    # Create agent with database and history
    agent = get_agent(model)
    
    # Use provided session_id or generate new
    session_id = args.session_id or f"session_{uuid.uuid4().hex[:8]}"
    
    print_section("Session")
    print(f"  Session ID: {session_id}")
    if args.session_id:
        print("  (Continuing existing session)")
    else:
        print("  (New session)")
    
    # First message
    print_section("Conversation")
    
    # Check if we have history
    try:
        session = agent.get_session(session_id=session_id)
        if session and hasattr(session, 'runs') and session.runs:
            print(f"  Found {len(session.runs)} previous messages")
        else:
            print("  No previous history found")
    except Exception:
        print("  Starting fresh session")
    
    # Interactive loop
    print("\nType 'quit' to exit, 'history' to show history\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
            
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            break
            
        if user_input.lower() == 'history':
            try:
                session = agent.get_session(session_id=session_id)
                if session and hasattr(session, 'runs'):
                    print(f"\n  Session has {len(session.runs)} runs")
                    for i, run in enumerate(session.runs[-5:], 1):
                        if hasattr(run, 'input'):
                            print(f"    {i}. User: {str(run.input)[:50]}...")
            except Exception as e:
                print(f"  Could not retrieve history: {e}")
            continue
        
        # Run agent with session persistence
        response = agent.run(user_input, session_id=session_id)
        print(f"Agent: {response.content}\n")
    
    print_section("Session Saved")
    print(f"  Re-run with: python main.py --session-id {session_id}")


if __name__ == "__main__":
    main()
