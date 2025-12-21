"""
Example #211: Debate Team Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Multiple agents debate a topic from different perspectives to explore all angles
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"rounds": 2}

class DebateArgument(BaseModel):
    position: str = Field(description="pro or con")
    main_point: str = Field(description="Central argument")
    supporting_evidence: list[str] = Field(description="Evidence and examples")
    rebuttal_to_opponent: str = Field(description="Response to opposing view")

class DebateResult(BaseModel):
    topic: str = Field(description="The debate topic")
    pro_arguments: list[DebateArgument] = Field(description="Arguments for")
    con_arguments: list[DebateArgument] = Field(description="Arguments against")
    synthesis: str = Field(description="Balanced synthesis of both sides")
    key_insights: list[str] = Field(description="Important takeaways")
    recommendation: str = Field(description="Nuanced recommendation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_pro_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Pro Advocate",
        instructions=[
            "You argue IN FAVOR of the given proposition.",
            "Present strong, evidence-based arguments.",
            "Anticipate and address counterarguments.",
            "Be persuasive but intellectually honest.",
        ],
        markdown=True,
    )

def get_con_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Con Advocate",
        instructions=[
            "You argue AGAINST the given proposition.",
            "Present strong, evidence-based arguments.",
            "Challenge assumptions and highlight risks.",
            "Be persuasive but intellectually honest.",
        ],
        markdown=True,
    )

def get_moderator_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Debate Moderator",
        instructions=[
            "You synthesize arguments from both sides of a debate.",
            "Identify the strongest points from each position.",
            "Provide a balanced, nuanced conclusion.",
            "Extract key insights for decision-making.",
        ],
        output_schema=DebateResult,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Returns the moderator agent as the primary interface."""
    return get_moderator_agent(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Debate Team - Demo")
    print("=" * 60)
    topic = "Remote work should be the default for knowledge workers"
    
    # Simulate debate rounds
    pro_agent = get_pro_agent()
    con_agent = get_con_agent()
    moderator = agent
    
    print(f"\n📢 Topic: {topic}")
    print("\n🎭 Running debate simulation...")
    
    # Get arguments from both sides
    pro_response = pro_agent.run(f"Argue FOR: {topic}")
    con_response = con_agent.run(f"Argue AGAINST: {topic}")
    
    # Synthesize with moderator
    synthesis_prompt = f"""
    Topic: {topic}
    
    PRO arguments: {pro_response.content}
    
    CON arguments: {con_response.content}
    
    Synthesize these arguments into a balanced analysis."""
    
    result = moderator.run(synthesis_prompt)
    
    if isinstance(result.content, DebateResult):
        r = result.content
        print(f"\n✅ PRO Highlights:")
        for arg in r.pro_arguments[:2]:
            print(f"  • {arg.main_point}")
        print(f"\n❌ CON Highlights:")
        for arg in r.con_arguments[:2]:
            print(f"  • {arg.main_point}")
        print(f"\n⚖️ Synthesis: {r.synthesis[:200]}...")
        print(f"\n💡 Recommendation: {r.recommendation}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", "-r", type=int, default=DEFAULT_CONFIG["rounds"])
    args = parser.parse_args()
    run_demo(get_agent(), {"rounds": args.rounds})

if __name__ == "__main__": main()
