#!/usr/bin/env python3
"""
Lesson 04: Streaming Responses

Concepts covered:
- Using print_response() for streaming output
- Manual streaming with stream=True
- Async streaming with arun()
- Comparing streaming vs non-streaming UX

Run: python main.py
     python main.py --compare
     python main.py --async
"""

import argparse
import asyncio
import sys
import time
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


def demo_print_response(agent: Agent, prompt: str) -> None:
    """Demonstrate the simplest streaming method."""
    print_section("Method 1: print_response() - Simplest")
    print(f"Prompt: {prompt}\n")
    print("Response:")
    print("-" * 40)
    agent.print_response(prompt)
    print("\n" + "-" * 40)


def demo_manual_streaming(agent: Agent, prompt: str) -> None:
    """Demonstrate manual streaming with stream=True."""
    print_section("Method 2: Manual Streaming")
    print(f"Prompt: {prompt}\n")
    print("Response:")
    print("-" * 40)
    
    # Run with streaming enabled
    response = agent.run(prompt, stream=True)
    
    # Process events as they arrive
    for event in response:
        # Events have different types; content events have the text
        if hasattr(event, 'content') and event.content:
            print(event.content, end="", flush=True)
    
    print("\n" + "-" * 40)


async def demo_async_streaming(agent: Agent, prompt: str) -> None:
    """Demonstrate async streaming with arun()."""
    print_section("Method 3: Async Streaming")
    print(f"Prompt: {prompt}\n")
    print("Response:")
    print("-" * 40)
    
    # Use async run with streaming
    async for event in agent.arun(prompt, stream=True):
        if hasattr(event, 'content') and event.content:
            print(event.content, end="", flush=True)
    
    print("\n" + "-" * 40)


def compare_streaming_modes(agent: Agent, prompt: str) -> None:
    """Compare streaming vs non-streaming performance and UX."""
    print_section("Comparison: Streaming vs Non-Streaming")
    print(f"Prompt: {prompt}\n")
    
    # Non-streaming
    print("Non-Streaming Mode:")
    print("  Waiting for complete response...", end=" ", flush=True)
    start = time.time()
    response = agent.run(prompt, stream=False)
    elapsed_non_stream = time.time() - start
    print(f"done! ({elapsed_non_stream:.2f}s)")
    print(f"  First token visible after: {elapsed_non_stream:.2f}s")
    print()
    
    # Streaming
    print("Streaming Mode:")
    print("  Response: ", end="", flush=True)
    start = time.time()
    first_token_time = None
    char_count = 0
    
    response = agent.run(prompt, stream=True)
    for event in response:
        if hasattr(event, 'content') and event.content:
            if first_token_time is None:
                first_token_time = time.time() - start
            # Show first 50 chars then truncate
            if char_count < 50:
                print(event.content, end="", flush=True)
                char_count += len(event.content)
            elif char_count == 50:
                print("...", end="", flush=True)
                char_count += 1
    
    elapsed_stream = time.time() - start
    print(f" ({elapsed_stream:.2f}s)")
    print(f"  First token visible after: {first_token_time:.2f}s")
    print()
    
    # Analysis
    print("Analysis:")
    print(f"  Total time (non-streaming): {elapsed_non_stream:.2f}s")
    print(f"  Total time (streaming):     {elapsed_stream:.2f}s")
    print(f"  Time to first token:        {first_token_time:.2f}s")
    print()
    print("  Streaming provides better UX by showing content immediately,")
    print("  even though total time is similar.")



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return Agent(
        model=model,
instructions="You are a creative writer. Be expressive but concise.",
markdown=True,
    )


def main():
    """Demonstrate streaming responses."""
    parser = argparse.ArgumentParser(
        description="Streaming responses with Agno",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--prompt",
        type=str,
        default="Write a short poem about artificial intelligence (4 lines).",
        help="Prompt to send to the agent",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare streaming vs non-streaming",
    )
    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Demonstrate async streaming",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Show all streaming methods",
    )
    args = parser.parse_args()

    print_header("Lesson 04: Streaming Responses")

    try:
        model = get_model(
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
        )
    except EnvironmentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    agent = get_agent(model)

    print(f"Provider: {args.provider}")
    print(f"Model: {args.model or 'default'}")

    if args.compare:
        compare_streaming_modes(agent, args.prompt)
    elif args.use_async:
        asyncio.run(demo_async_streaming(agent, args.prompt))
    elif args.all:
        demo_print_response(agent, args.prompt)
        demo_manual_streaming(agent, "Write another short poem about code.")
        asyncio.run(demo_async_streaming(agent, "One more poem about debugging."))
    else:
        # Default: just show print_response
        demo_print_response(agent, args.prompt)

    print()
    print("Tip: Try --compare to see streaming vs non-streaming difference!")
    print("     Try --all to see all streaming methods!")


if __name__ == "__main__":
    main()
