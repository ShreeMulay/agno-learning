"""
Example #075: Capacity Planner
Category: engineering/devops
DESCRIPTION: Analyzes usage patterns and recommends capacity changes.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"metrics": "Current: 70% CPU, 85% memory, 60% disk. Traffic growing 15% monthly. Peak hours: 9am-11am."}

class CapacityPlan(BaseModel):
    current_utilization: str = Field(description="Current state")
    bottlenecks: list[str] = Field(description="Resource bottlenecks")
    recommendations: list[str] = Field(description="Scaling recommendations")
    timeline: str = Field(description="When to scale")
    cost_impact: str = Field(description="Cost estimate")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Capacity Planner",
        instructions=["Analyze capacity needs and recommend scaling strategies."],
        output_schema=CapacityPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Capacity Planner - Demo\n" + "=" * 60)
    response = agent.run(f"Plan capacity: {config.get('metrics', DEFAULT_CONFIG['metrics'])}")
    result = response.content
    if isinstance(result, CapacityPlan):
        print(f"\n📊 {result.current_utilization}")
        for r in result.recommendations: print(f"  • {r}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", "-m", default=DEFAULT_CONFIG["metrics"])
    args = parser.parse_args()
    run_demo(get_agent(), {"metrics": args.metrics})

if __name__ == "__main__": main()
