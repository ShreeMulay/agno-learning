"""
Example #224: Planning Agent
Category: advanced/patterns
DESCRIPTION: Agent that creates and executes multi-step plans
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"planning_depth": "detailed"}

class PlanStep(BaseModel):
    step_number: int = Field(description="Step sequence number")
    action: str = Field(description="What to do")
    dependencies: list[int] = Field(description="Steps that must complete first")
    expected_output: str = Field(description="What this step produces")
    estimated_time: str = Field(description="Time estimate")

class ExecutionPlan(BaseModel):
    goal: str = Field(description="The objective to achieve")
    steps: list[PlanStep] = Field(description="Ordered steps to execute")
    total_steps: int = Field(description="Total number of steps")
    critical_path: list[int] = Field(description="Steps on critical path")
    risks: list[str] = Field(description="Potential risks to plan")
    success_criteria: str = Field(description="How to know when done")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Planning Agent",
        instructions=[
            f"You create {cfg['planning_depth']} execution plans.",
            "Break complex goals into atomic, actionable steps.",
            "Identify dependencies between steps.",
            "Consider risks and mitigation strategies.",
            "Define clear success criteria.",
        ],
        output_schema=ExecutionPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Planning Agent - Demo")
    print("=" * 60)
    
    goal = "Deploy a new microservice to production with zero downtime"
    print(f"\n🎯 Goal: {goal}")
    
    response = agent.run(f"Create an execution plan for: {goal}")
    
    if isinstance(response.content, ExecutionPlan):
        r = response.content
        print(f"\n📋 Plan: {r.total_steps} steps")
        print(f"\n🔢 Steps:")
        for step in r.steps:
            deps = f" (after steps {step.dependencies})" if step.dependencies else ""
            print(f"  {step.step_number}. {step.action}{deps}")
            print(f"     → {step.expected_output} ({step.estimated_time})")
        print(f"\n⚠️ Risks: {', '.join(r.risks[:3])}")
        print(f"✅ Success: {r.success_criteria}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--planning-depth", "-p", default=DEFAULT_CONFIG["planning_depth"])
    args = parser.parse_args()
    run_demo(get_agent(config={"planning_depth": args.planning_depth}), {"planning_depth": args.planning_depth})

if __name__ == "__main__": main()
