"""
Example #XXX: Example Name
Category: category/subcategory

DESCRIPTION:
One paragraph explaining what this agent does, what problem it solves,
and when you would use it in the real world.

PATTERNS:
- Pattern 1 (e.g., Tools + Structured Output)
- Pattern 2 (e.g., Memory)

ARGUMENTS:
- param1 (str): Description of parameter. Default: "default_value"
- param2 (int): Description of parameter. Default: 10
"""

import argparse
import os
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel

# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "param1": "default_value",
    "param2": 10,
}


# =============================================================================
# Output Schema (if using structured output)
# =============================================================================

class ExampleOutput(BaseModel):
    """Structured output from the agent."""
    
    result: str
    confidence: float
    details: list[str]


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model. Override via get_agent(model=...)"""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the agent with optional configuration.
    
    Args:
        model: Override default model (for testing/portal integration)
        config: Dict of configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent instance ready to use
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Example Agent",
        instructions=[
            "You are a helpful agent.",
            f"Configuration: param1={cfg['param1']}, param2={cfg['param2']}",
        ],
        # Uncomment for structured output:
        # response_model=ExampleOutput,
        # 
        # Uncomment for tools:
        # tools=[SomeTool()],
        #
        # Uncomment for memory:
        # storage=SqliteDb(table_name="example", db_file="data.db"),
        # session_id=cfg.get("session_id", "default"),
        #
        # Uncomment for knowledge:
        # knowledge=PDFKnowledgeBase(path="./docs"),
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent):
    """Run a demonstration of the agent."""
    print("\n" + "=" * 60)
    print("Example Name - Demo")
    print("=" * 60)
    
    # Demo query
    query = "Hello, demonstrate your capabilities."
    print(f"\nQuery: {query}")
    print("-" * 40)
    
    response = agent.run(query)
    
    # Handle structured output if enabled
    if hasattr(response, 'parsed') and response.parsed:
        result = response.parsed
        print(f"Result: {result.result}")
        print(f"Confidence: {result.confidence}")
        print(f"Details: {result.details}")
    else:
        print(response.content)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Example Agent - Description of what it does"
    )
    
    # Add arguments matching DEFAULT_CONFIG
    parser.add_argument(
        "--param1",
        type=str,
        default=DEFAULT_CONFIG["param1"],
        help=f"Description of param1 (default: {DEFAULT_CONFIG['param1']})"
    )
    parser.add_argument(
        "--param2",
        type=int,
        default=DEFAULT_CONFIG["param2"],
        help=f"Description of param2 (default: {DEFAULT_CONFIG['param2']})"
    )
    
    # Parse args
    args = parser.parse_args()
    
    # Create agent with CLI config
    agent = get_agent(config=vars(args))
    
    # Run demo
    run_demo(agent)


if __name__ == "__main__":
    main()
