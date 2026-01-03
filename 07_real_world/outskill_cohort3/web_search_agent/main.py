#!/usr/bin/env python3
"""Example: Web Search Agent
Category: outskill_cohort3/tools

Search the web using DuckDuckGo and get answers with source citations.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section

DEFAULT_CONFIG = {
    "query": "What are the latest developments in AI?",
}


def create_agent(model):
    return Agent(
        name="WebSearchAgent",
        model=model,
        tools=[DuckDuckGoTools()],
        instructions=["Always cite your sources with URLs"],
        markdown=True,
    )


def get_agent(model=None):
    if model is None:
        model = get_model()
    return create_agent(model)


def main():
    parser = argparse.ArgumentParser(
        description="Search the web with AI-powered summaries"
    )
    add_model_args(parser)
    
    parser.add_argument(
        "--query",
        type=str,
        default=DEFAULT_CONFIG["query"],
        help="Search query"
    )
    
    args = parser.parse_args()
    
    print_header("Web Search Agent")
    
    print_section("Query")
    print(f"  {args.query}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_agent(model)
    
    print_section("Searching...")
    
    try:
        response = agent.run(args.query)
        
        print_section("Results")
        print(response.content)
        
    except Exception as e:
        print(f"\n  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
