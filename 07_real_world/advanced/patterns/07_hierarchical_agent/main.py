"""
Example #227: Hierarchical Agent
Category: advanced/patterns
DESCRIPTION: Manager agent that delegates to specialized sub-agents
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"delegation_style": "smart"}

class Delegation(BaseModel):
    sub_agent: str = Field(description="Which sub-agent to use")
    task: str = Field(description="Task assigned")
    result: str = Field(description="Result from sub-agent")

class HierarchicalResponse(BaseModel):
    original_task: str = Field(description="User's original request")
    delegations: list[Delegation] = Field(description="Tasks delegated")
    synthesis: str = Field(description="Combined final answer")
    coordination_notes: str = Field(description="How results were coordinated")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_research_agent(model=None) -> Agent:
    return Agent(model=model or default_model(), name="Research Sub-Agent",
        instructions=["You research and gather information.", "Focus on facts and sources."], markdown=True)

def get_analysis_agent(model=None) -> Agent:
    return Agent(model=model or default_model(), name="Analysis Sub-Agent",
        instructions=["You analyze data and draw conclusions.", "Focus on insights."], markdown=True)

def get_writing_agent(model=None) -> Agent:
    return Agent(model=model or default_model(), name="Writing Sub-Agent",
        instructions=["You write clear, engaging content.", "Focus on communication."], markdown=True)

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Manager Agent",
        instructions=[
            f"You coordinate sub-agents using {cfg['delegation_style']} delegation.",
            "Break complex tasks into sub-tasks for specialists.",
            "Synthesize results from multiple sub-agents.",
            "Ensure coherent, comprehensive final output.",
        ],
        output_schema=HierarchicalResponse,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Hierarchical Agent - Demo")
    print("=" * 60)
    
    task = "Create a brief report on the benefits of remote work"
    print(f"\n📋 Task: {task}")
    
    # Get sub-agent contributions
    research = get_research_agent().run(f"Research: {task}")
    analysis = get_analysis_agent().run(f"Analyze findings: {research.content}")
    
    manager_prompt = f"""
    Original task: {task}
    
    Research findings: {research.content}
    Analysis: {analysis.content}
    
    Coordinate these results into a final response."""
    
    response = agent.run(manager_prompt)
    
    if isinstance(response.content, HierarchicalResponse):
        r = response.content
        print(f"\n👥 Delegations Made:")
        for d in r.delegations:
            print(f"  → {d.sub_agent}: {d.task}")
        print(f"\n📝 Final Synthesis:")
        print(f"   {r.synthesis[:300]}...")
        print(f"\n🔗 Coordination: {r.coordination_notes}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delegation-style", "-d", default=DEFAULT_CONFIG["delegation_style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"delegation_style": args.delegation_style}), {"delegation_style": args.delegation_style})

if __name__ == "__main__": main()
