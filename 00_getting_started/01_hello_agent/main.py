#!/usr/bin/env python3
"""
Lesson 01: Hello Agent - Your first Agno agent

Concepts covered:
- Creating an Agent with a model
- Setting instructions
- Running the agent with run()
- Using print_response() for formatted output

Run: python main.py [--provider openai] [--message "Your message"]
"""

import argparse
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        model=model,
instructions=[
"You are a friendly and helpful AI assistant.",
"Keep your responses concise but informative.",
"Always be encouraging and positive.",
],
markdown=True,  # Format responses as markdown
    )


def main():
    """Run the Hello Agent example."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Your first Agno agent - Hello World!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--message", "-msg",
        type=str,
        default="Hello! Please introduce yourself and tell me one interesting fact.",
        help="Message to send to the agent",
    )
    args = parser.parse_args()

    # Display header
    print_header("Lesson 01: Hello Agent")

    # Step 1: Get the model from our unified config
    print(f"Provider: {args.provider}")
    print(f"Model: {args.model or 'default'}")
    print(f"Temperature: {args.temperature}")
    print()

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        print("\nTip: Copy .env.example to .env and add your API keys")
        sys.exit(1)

    # Step 2: Create the agent with instructions
    agent = get_agent(model)

    # Step 3: Run the agent and display response
    print(f"User: {args.message}")
    print()
    print("Agent:")
    print("-" * 40)

    # print_response() is a convenience method that handles streaming
    agent.print_response(args.message)

    print("-" * 40)
    print()

    # Bonus: Show that agents are stateless by default
    print("Note: Agents are stateless by default.")
    print("Each run() call is independent - the agent doesn't remember previous messages.")
    print("We'll learn about memory in Module 3!")


if __name__ == "__main__":
    main()
