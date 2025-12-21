"""
Example #221: Tool-Using Agent
Category: advanced/patterns
DESCRIPTION: Demonstrates agents that can use external tools and functions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools import tool
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"tools_enabled": True}

# Define custom tools
@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        # Simple safe eval for basic math
        allowed = set("0123456789+-*/.(). ")
        if all(c in allowed for c in expression):
            result = eval(expression)
            return f"Result: {result}"
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_current_time() -> str:
    """Get the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def word_count(text: str) -> str:
    """Count words in the provided text."""
    count = len(text.split())
    return f"Word count: {count}"

class ToolResponse(BaseModel):
    query: str = Field(description="Original user query")
    tools_used: list[str] = Field(description="Tools that were invoked")
    result: str = Field(description="Final answer")
    reasoning: str = Field(description="How tools helped answer")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    tools = [calculate, get_current_time, word_count] if cfg.get("tools_enabled") else []
    return Agent(
        model=model or default_model(),
        name="Tool-Using Agent",
        instructions=[
            "You are an agent that uses tools to answer questions.",
            "Use the calculate tool for math operations.",
            "Use get_current_time for time-related queries.",
            "Use word_count for text analysis.",
            "Always explain which tools you used and why.",
        ],
        tools=tools,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Tool-Using Agent - Demo")
    print("=" * 60)
    queries = [
        "What is 15% of 250?",
        "What time is it right now?",
        "How many words are in: 'The quick brown fox jumps over the lazy dog'?"
    ]
    for query in queries:
        print(f"\n❓ Query: {query}")
        response = agent.run(query)
        print(f"✅ Response: {response.content[:200]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tools-enabled", "-t", action="store_true", default=True)
    args = parser.parse_args()
    run_demo(get_agent(config={"tools_enabled": args.tools_enabled}), {"tools_enabled": args.tools_enabled})

if __name__ == "__main__": main()
