"""
Example #070: Performance Optimizer
Category: engineering/code

DESCRIPTION:
Analyzes code for performance issues and suggests optimizations.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def process_data(data):
    results = []
    for item in data:
        result = expensive_transform(item)
        results.append(result)
    return results

def search_users(users, query):
    matching = []
    for user in users:
        if query.lower() in user['name'].lower():
            matching.append(user)
    return matching
''',
}

class Optimization(BaseModel):
    location: str = Field(description="Function/line")
    issue: str = Field(description="Performance problem")
    complexity: str = Field(description="Current time complexity")
    optimized_complexity: str = Field(description="After optimization")
    suggestion: str = Field(description="How to optimize")
    optimized_code: str = Field(description="Optimized version")
    speedup: str = Field(description="Expected improvement")

class PerformanceReport(BaseModel):
    optimizations: list[Optimization] = Field(description="Found optimizations")
    overall_impact: str = Field(description="Expected overall improvement")
    priority_order: list[str] = Field(description="Order to implement")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Performance Optimizer",
        instructions=[
            "You are a performance engineer optimizing code.",
            "Look for: O(n²) loops, repeated calculations, memory issues,",
            "I/O bottlenecks, missing caching, inefficient data structures.",
            "Suggest concrete optimizations with complexity analysis.",
        ],
        output_schema=PerformanceReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Performance Optimizer - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Optimize:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, PerformanceReport):
        print(f"\n⚡ Impact: {result.overall_impact}")
        for o in result.optimizations:
            print(f"\n  🔧 {o.location}")
            print(f"     Issue: {o.issue}")
            print(f"     {o.complexity} → {o.optimized_complexity}")
            print(f"     Speedup: {o.speedup}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Performance Optimizer")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
