#!/usr/bin/env python3
"""
Lesson 02: Multi-Provider Support

Concepts covered:
- Switching between LLM providers
- Using the unified model_config
- Comparing provider responses

Run: python main.py [--provider openai] [--compare]
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import (
    get_model,
    add_model_args,
    list_providers,
    check_api_key,
    PROVIDER_CONFIGS,
)
from shared.utils import print_header, print_section


def run_with_provider(provider: str, model: str = None, prompt: str = "") -> tuple[str, float]:
    """
    Run a prompt with a specific provider and measure time.
    
    Returns:
        Tuple of (response_content, elapsed_seconds)
    """
    try:
        llm = get_model(provider, model)
        agent = Agent(
            model=llm,
            instructions="You are a helpful assistant. Be concise.",
        )
        
        start = time.time()
        response = agent.run(prompt)
        elapsed = time.time() - start
        
        return response.content, elapsed
    except Exception as e:
        return f"Error: {e}", 0.0


def main():
    """Demonstrate multi-provider support."""
    parser = argparse.ArgumentParser(
        description="Compare LLM providers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_model_args(parser)
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare all configured providers",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="What is the capital of France? Answer in one sentence.",
        help="Prompt to test with",
    )
    args = parser.parse_args()

    print_header("Lesson 02: Multi-Provider Support")

    # Show available providers
    print_section("Available Providers")
    for name, desc in list_providers().items():
        has_key, env_var = check_api_key(name)
        status = "[+] Configured" if has_key else "[-] Not configured"
        default_model = PROVIDER_CONFIGS[name]["default_model"]
        print(f"  {name:12} {status}")
        print(f"              Default model: {default_model}")
        if not has_key:
            print(f"              Set: {env_var}")
        print()

    if args.compare:
        # Compare all configured providers
        print_section("Provider Comparison")
        print(f"Prompt: {args.prompt}\n")

        results = []
        for provider in list_providers():
            has_key, _ = check_api_key(provider)
            if not has_key:
                continue

            print(f"Testing {provider}...", end=" ", flush=True)
            content, elapsed = run_with_provider(provider, prompt=args.prompt)
            results.append((provider, content, elapsed))
            print(f"done ({elapsed:.2f}s)")

        print_section("Results")
        for provider, content, elapsed in results:
            print(f"\n{provider.upper()} ({elapsed:.2f}s):")
            print("-" * 40)
            print(content[:500])  # Truncate long responses
            if len(content) > 500:
                print("... (truncated)")
            print()

    else:
        # Run with single provider
        print_section(f"Running with {args.provider}")
        
        has_key, env_var = check_api_key(args.provider)
        if not has_key:
            print(f"Error: {args.provider} is not configured.")
            print(f"Set {env_var} in your .env file.")
            sys.exit(1)

        print(f"Provider: {args.provider}")
        print(f"Model: {args.model or PROVIDER_CONFIGS[args.provider]['default_model']}")
        print(f"Prompt: {args.prompt}")
        print()

        content, elapsed = run_with_provider(
            args.provider,
            args.model,
            args.prompt,
        )

        print("Response:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        print(f"\nElapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
