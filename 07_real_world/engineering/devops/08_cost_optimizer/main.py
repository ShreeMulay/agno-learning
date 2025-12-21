"""
Example #078: Cost Optimizer
Category: engineering/devops
DESCRIPTION: Analyzes cloud spending and recommends cost optimizations.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"spending": "EC2: $5000/mo (20 instances, avg 30% utilization), RDS: $2000/mo, S3: $500/mo"}

class CostOptimization(BaseModel):
    resource: str = Field(description="Resource")
    current_cost: str = Field(description="Current cost")
    optimization: str = Field(description="Suggested change")
    savings: str = Field(description="Estimated savings")

class CostReport(BaseModel):
    total_monthly: str = Field(description="Total monthly spend")
    optimizations: list[CostOptimization] = Field(description="Optimization opportunities")
    total_savings: str = Field(description="Total potential savings")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Cost Optimizer",
        instructions=["Identify cloud cost optimization opportunities."],
        output_schema=CostReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Cost Optimizer - Demo\n" + "=" * 60)
    response = agent.run(f"Optimize: {config.get('spending', DEFAULT_CONFIG['spending'])}")
    result = response.content
    if isinstance(result, CostReport):
        print(f"\n💰 Current: {result.total_monthly} | Potential Savings: {result.total_savings}")
        for o in result.optimizations: print(f"  • {o.resource}: {o.savings}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spending", "-s", default=DEFAULT_CONFIG["spending"])
    args = parser.parse_args()
    run_demo(get_agent(), {"spending": args.spending})

if __name__ == "__main__": main()
