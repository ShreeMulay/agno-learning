#!/usr/bin/env python3
"""Lesson 01: AgentOS Runtime - Deploy agents as production APIs.

This example shows how to create an AgentOS instance that exposes
agents through a FastAPI application.

Run with:
    python main.py

Then visit:
    http://localhost:7777/docs - API documentation
    http://localhost:7777/config - Configuration
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.os import AgentOS
from agno.db.sqlite import AsyncSqliteDb

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_agent_os(model):
    """Create an AgentOS with example agents."""
    
    # Database for session persistence
    db = AsyncSqliteDb(
        id="agno_learning_db",
        db_file="tmp/agno_learning.db"
    )
    
    # Create agents
    assistant = Agent(
        name="Assistant",
        model=model,
        db=db,
        instructions=["You are a helpful AI assistant."],
        markdown=True,
        add_history_to_context=True,
        num_history_runs=5,
    )
    
    researcher = Agent(
        name="Researcher",
        model=model,
        db=db,
        instructions=[
            "You are a research assistant.",
            "Provide thorough, well-cited information.",
        ],
        markdown=True,
    )
    
    # Create AgentOS
    agent_os = AgentOS(
        id="agno-learning-os",
        description="Agno Learning Hub - Example AgentOS",
        agents=[assistant, researcher],
    )
    
    return agent_os


def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_agent_os(model).agents[0]


def main():
    parser = argparse.ArgumentParser(description="AgentOS Demo")
    add_model_args(parser)
    parser.add_argument(
        "--port", type=int, default=7777,
        help="Port to run the server on (default: 7777)"
    )
    args = parser.parse_args()

    print_header("Lesson 01: AgentOS Runtime")
    
    print_section("Configuration")
    print(f"  Provider: {args.provider}")
    print(f"  Model: {args.model or 'default'}")
    print(f"  Port: {args.port}")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    
    # Create AgentOS
    agent_os = create_agent_os(model)
    
    print_section("Starting AgentOS")
    print(f"  ID: {agent_os.id}")
    print(f"  Agents: {[a.name for a in agent_os.agents]}")
    print()
    print("  Endpoints:")
    print(f"    - http://localhost:{args.port}/docs")
    print(f"    - http://localhost:{args.port}/config")
    print()
    
    # Get the FastAPI app and serve
    app = agent_os.get_app()
    agent_os.serve(
        app="06_production.01_agent_os.main:app",
        port=args.port,
        reload=True
    )


# Export app for uvicorn
def get_app():
    """Factory function for uvicorn."""
    import os
    # Use default OpenRouter model for standalone running
    os.environ.setdefault("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
    
    from shared.model_config import get_model
    model = get_model("openrouter")
    agent_os = create_agent_os(model)
    return agent_os.get_app()


# This is used when running with: uvicorn main:app
app = None
try:
    app = get_app()
except Exception:
    pass  # Will be created when main() is called


if __name__ == "__main__":
    main()
