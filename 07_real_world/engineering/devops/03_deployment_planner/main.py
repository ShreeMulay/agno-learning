"""
Example #073: Deployment Planner
Category: engineering/devops
DESCRIPTION: Plans deployments with rollback strategies and risk assessment.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"deployment": "Deploy v2.5.0 with database migration, new API endpoints, and breaking change to auth flow"}

class DeploymentPlan(BaseModel):
    risk_level: str = Field(description="high/medium/low")
    strategy: str = Field(description="blue-green/canary/rolling/recreate")
    pre_deployment: list[str] = Field(description="Steps before deploy")
    deployment_steps: list[str] = Field(description="Deployment steps")
    rollback_plan: list[str] = Field(description="Rollback steps")
    monitoring_checklist: list[str] = Field(description="What to monitor")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Deployment Planner",
        instructions=["Plan safe deployments with proper rollback strategies."],
        output_schema=DeploymentPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Deployment Planner - Demo\n" + "=" * 60)
    response = agent.run(f"Plan: {config.get('deployment', DEFAULT_CONFIG['deployment'])}")
    result = response.content
    if isinstance(result, DeploymentPlan):
        print(f"\n⚠️ Risk: {result.risk_level} | Strategy: {result.strategy}")
        print("\n📋 Steps:")
        for s in result.deployment_steps: print(f"  • {s}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deployment", "-d", default=DEFAULT_CONFIG["deployment"])
    args = parser.parse_args()
    run_demo(get_agent(), {"deployment": args.deployment})

if __name__ == "__main__": main()
