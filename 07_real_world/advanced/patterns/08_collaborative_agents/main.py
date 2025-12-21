"""
Example #228: Collaborative Agents
Category: advanced/patterns
DESCRIPTION: Multiple peer agents that collaborate on tasks together
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"collaboration_style": "consensus"}

class AgentContribution(BaseModel):
    agent_name: str = Field(description="Contributing agent")
    contribution: str = Field(description="What they contributed")
    confidence: str = Field(description="Confidence in contribution")

class CollaborativeResult(BaseModel):
    task: str = Field(description="The collaborative task")
    contributions: list[AgentContribution] = Field(description="Each agent's input")
    consensus: str = Field(description="Points of agreement")
    disagreements: list[str] = Field(description="Points of divergence")
    final_output: str = Field(description="Synthesized result")
    collaboration_quality: int = Field(description="Quality score 1-10")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_creative_agent(model=None) -> Agent:
    return Agent(model=model or default_model(), name="Creative Agent",
        instructions=["You bring creative, innovative ideas.", "Think outside the box."], markdown=True)

def get_analytical_agent(model=None) -> Agent:
    return Agent(model=model or default_model(), name="Analytical Agent",
        instructions=["You provide logical, data-driven analysis.", "Focus on feasibility."], markdown=True)

def get_practical_agent(model=None) -> Agent:
    return Agent(model=model or default_model(), name="Practical Agent",
        instructions=["You focus on implementation and execution.", "Keep things realistic."], markdown=True)

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Collaboration Coordinator",
        instructions=[
            f"You facilitate {cfg['collaboration_style']} collaboration.",
            "Synthesize diverse agent perspectives.",
            "Identify areas of consensus and disagreement.",
            "Produce balanced, well-rounded outputs.",
        ],
        output_schema=CollaborativeResult,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Collaborative Agents - Demo")
    print("=" * 60)
    
    task = "Design a new feature for a task management app"
    print(f"\n🤝 Task: {task}")
    
    creative = get_creative_agent().run(task)
    analytical = get_analytical_agent().run(task)
    practical = get_practical_agent().run(task)
    
    collab_prompt = f"""
    Task: {task}
    
    Creative perspective: {creative.content}
    Analytical perspective: {analytical.content}
    Practical perspective: {practical.content}
    
    Synthesize these into a collaborative result."""
    
    response = agent.run(collab_prompt)
    
    if isinstance(response.content, CollaborativeResult):
        r = response.content
        print(f"\n👥 Contributions:")
        for c in r.contributions:
            print(f"  {c.agent_name}: {c.contribution[:80]}...")
        print(f"\n✅ Consensus: {r.consensus}")
        if r.disagreements:
            print(f"⚖️ Disagreements: {', '.join(r.disagreements[:2])}")
        print(f"\n📋 Final Output: {r.final_output[:200]}...")
        print(f"📊 Collaboration Quality: {r.collaboration_quality}/10")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--collaboration-style", "-c", default=DEFAULT_CONFIG["collaboration_style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"collaboration_style": args.collaboration_style}), {"collaboration_style": args.collaboration_style})

if __name__ == "__main__": main()
