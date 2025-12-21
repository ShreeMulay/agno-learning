"""
Example #079: Disaster Recovery Planner
Category: engineering/devops
DESCRIPTION: Creates disaster recovery plans with RTO/RPO analysis.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"system": "E-commerce platform: 3 web servers, 1 primary + 1 replica database, file storage on S3"}

class DRPlan(BaseModel):
    system: str = Field(description="System description")
    rto: str = Field(description="Recovery Time Objective")
    rpo: str = Field(description="Recovery Point Objective")
    backup_strategy: list[str] = Field(description="Backup approach")
    recovery_steps: list[str] = Field(description="Recovery procedure")
    test_schedule: str = Field(description="Testing frequency")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="DR Planner",
        instructions=["Create comprehensive disaster recovery plans."],
        output_schema=DRPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Disaster Recovery Planner - Demo\n" + "=" * 60)
    response = agent.run(f"Create DR plan: {config.get('system', DEFAULT_CONFIG['system'])}")
    result = response.content
    if isinstance(result, DRPlan):
        print(f"\n⏱️ RTO: {result.rto} | RPO: {result.rpo}")
        for s in result.recovery_steps: print(f"  • {s}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--system", "-s", default=DEFAULT_CONFIG["system"])
    args = parser.parse_args()
    run_demo(get_agent(), {"system": args.system})

if __name__ == "__main__": main()
