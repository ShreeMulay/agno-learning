"""
Example #077: Runbook Generator
Category: engineering/devops
DESCRIPTION: Generates operational runbooks from incident patterns.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"scenario": "Database failover procedure when primary becomes unresponsive"}

class RunbookStep(BaseModel):
    step_number: int = Field(description="Step number")
    action: str = Field(description="Action to take")
    verification: str = Field(description="How to verify")
    rollback: str = Field(description="Rollback if fails")

class Runbook(BaseModel):
    title: str = Field(description="Runbook title")
    trigger: str = Field(description="When to use")
    steps: list[RunbookStep] = Field(description="Procedure steps")
    escalation: str = Field(description="When to escalate")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Runbook Generator",
        instructions=["Generate clear, actionable operational runbooks."],
        output_schema=Runbook, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Runbook Generator - Demo\n" + "=" * 60)
    response = agent.run(f"Create runbook: {config.get('scenario', DEFAULT_CONFIG['scenario'])}")
    result = response.content
    if isinstance(result, Runbook):
        print(f"\n📖 {result.title}")
        for s in result.steps: print(f"  {s.step_number}. {s.action}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", "-s", default=DEFAULT_CONFIG["scenario"])
    args = parser.parse_args()
    run_demo(get_agent(), {"scenario": args.scenario})

if __name__ == "__main__": main()
