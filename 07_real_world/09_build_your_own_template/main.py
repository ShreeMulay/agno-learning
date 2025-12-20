#!/usr/bin/env python3
"""Example 09: Build Your Own - Template for your Agno application.

Use this as a starting point for your own agent project.

Run with:
    python main.py
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def create_your_agent(model):
    """Create your custom agent.
    
    Customize this function with:
    - Your own instructions
    - Tools you need
    - Knowledge bases
    - Memory settings
    """
    
    return Agent(
        name="YourAgent",
        model=model,
        instructions=[
            "You are a helpful assistant.",
            # Add your custom instructions here
            # "You specialize in..."
            # "Always remember to..."
        ],
        # tools=[YourTools()],  # Add your tools
        # knowledge=your_knowledge_base,  # Add knowledge
        # db=your_database,  # Add persistence
        markdown=True,
    )


def process_response(response):
    """Process the agent's response.
    
    Add your custom response handling here.
    """
    return response.content



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_your_agent(model)


def main():
    parser = argparse.ArgumentParser(description="Your Agent Application")
    add_model_args(parser)
    
    # Add your custom arguments
    parser.add_argument(
        "--interactive", "-i", action="store_true",
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()

    print_header("Your Agent Application")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_your_agent(model)
    
    print_section("Agent Ready")
    print(f"  Name: {agent.name}")
    print(f"  Provider: {args.provider}")
    print()
    
    if args.interactive:
        # Interactive mode
        print_section("Interactive Mode")
        print("  Type 'quit' to exit\n")
        
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
            
            response = agent.run(user_input)
            result = process_response(response)
            print(f"\nAgent: {result}\n")
    else:
        # Demo mode
        print_section("Demo")
        
        demo_prompts = [
            "Hello! What can you help me with?",
            "Give me a quick tip for productivity.",
        ]
        
        for prompt in demo_prompts:
            print(f"\nYou: {prompt}")
            response = agent.run(prompt)
            result = process_response(response)
            print(f"Agent: {result}")
    
    print_section("Done")
    print("  Customize this template for your own use case!")


if __name__ == "__main__":
    main()
