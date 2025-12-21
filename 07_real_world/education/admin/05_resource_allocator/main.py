"""
Example #125: Resource Allocator
Category: education/admin
DESCRIPTION: Allocates educational resources across departments
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"resource_type": "budget"}

class Allocation(BaseModel):
    department: str = Field(description="Department name")
    amount: float = Field(description="Allocated amount")
    percentage: float = Field(description="Percentage of total")
    justification: str = Field(description="Allocation rationale")

class AllocationPlan(BaseModel):
    resource_type: str = Field(description="Type of resource")
    total_available: float = Field(description="Total resources")
    allocations: list[Allocation] = Field(description="Department allocations")
    priorities: list[str] = Field(description="Allocation priorities")
    trade_offs: list[str] = Field(description="Trade-offs made")
    recommendations: list[str] = Field(description="Recommendations")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Resource Allocator",
        instructions=["Allocate resources fairly and efficiently", "Consider departmental needs", "Balance competing priorities", "Document rationale"],
        output_schema=AllocationPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Resource Allocator - Demo\n" + "=" * 60)
    response = agent.run(f"Allocate {config['resource_type']}: $500,000 total for Science (needs lab equipment), Math (textbook refresh), English (technology), Arts (supplies). Science enrollment up 20%")
    result = response.content
    if isinstance(result, AllocationPlan):
        print(f"\nResource: {result.resource_type} | Total: ${result.total_available:,.0f}")
        print(f"\nAllocations:")
        for a in result.allocations:
            print(f"  {a.department}: ${a.amount:,.0f} ({a.percentage:.1f}%)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource-type", "-t", default=DEFAULT_CONFIG["resource_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"resource_type": args.resource_type})

if __name__ == "__main__": main()
