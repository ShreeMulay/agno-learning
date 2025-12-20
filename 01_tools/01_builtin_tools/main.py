#!/usr/bin/env python3
"""
Lesson 01: Built-in Tools

Concepts covered:
- Adding pre-built tools to agents
- DuckDuckGoTools for web search
- Calculator for math
- How agents decide when to use tools

Run: python main.py --search "latest AI news"
     python main.py --calculate "What is 25% of 1200?"
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_search_agent(model):
    """Create an agent with web search capabilities."""
    return Agent(
        model=model,
        tools=[DuckDuckGoTools()],
        instructions=[
            "You are a research assistant with web search capabilities.",
            "When asked about current events or facts, search the web first.",
            "Always cite your sources.",
            "Be concise but thorough.",
        ],
        markdown=True,
    )


def create_calculator_agent(model):
    """Create an agent with calculation capabilities."""
    # Note: For simple math, most LLMs can do it directly
    # This demonstrates the pattern of giving agents tools
    return Agent(
        model=model,
        instructions=[
            "You are a helpful math assistant.",
            "Show your work step by step.",
            "Always verify calculations.",
        ],
        markdown=True,
    )


def create_multi_tool_agent(model):
    """Create an agent with multiple tool capabilities."""
    return Agent(
        model=model,
        tools=[
            DuckDuckGoTools(),
        ],
        instructions=[
            "You are a versatile assistant with multiple capabilities.",
            "You can search the web for current information.",
            "Choose the appropriate tool based on the question.",
            "Be helpful and thorough.",
        ],
        markdown=True,
    )



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_search_agent(model)


def main():
    """Demonstrate built-in tools."""
    parser = argparse.ArgumentParser(
        description="Built-in tools demonstration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--search",
        type=str,
        help="Search query (uses DuckDuckGo)",
    )
    parser.add_argument(
        "--calculate",
        type=str,
        help="Math question",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="General query (uses all available tools)",
    )
    args = parser.parse_args()

    # Default query if nothing specified
    if not args.search and not args.calculate and not args.query:
        args.search = "What are the latest developments in AI agents?"

    print_header("Lesson 01: Built-in Tools")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Provider: {args.provider}")
    print(f"Model: {args.model or 'default'}")

    if args.search:
        print_section("Web Search with DuckDuckGoTools")
        print(f"Query: {args.search}\n")
        
        agent = create_search_agent(model)
        print("Searching and analyzing results...\n")
        agent.print_response(args.search)

    if args.calculate:
        print_section("Math with Calculator")
        print(f"Question: {args.calculate}\n")
        
        agent = create_calculator_agent(model)
        agent.print_response(args.calculate)

    if args.query:
        print_section("Multi-Tool Query")
        print(f"Query: {args.query}\n")
        
        agent = create_multi_tool_agent(model)
        print("Analyzing query and selecting tools...\n")
        agent.print_response(args.query)

    print()
    print_section("Key Takeaways")
    print("  1. Tools extend what agents can do")
    print("  2. LLMs automatically decide when to use tools")
    print("  3. Use debug_mode=True to see tool usage details")
    print("  4. Combine multiple tools for powerful agents")


if __name__ == "__main__":
    main()
