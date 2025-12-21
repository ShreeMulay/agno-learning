"""
Example #225: Reflection Agent
Category: advanced/patterns
DESCRIPTION: Agent that reflects on and improves its own outputs
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"reflection_rounds": 2}

class ReflectionCritique(BaseModel):
    strengths: list[str] = Field(description="What works well")
    weaknesses: list[str] = Field(description="What could improve")
    suggestions: list[str] = Field(description="Specific improvements")
    quality_score: int = Field(description="Quality rating 1-10")

class ReflectedOutput(BaseModel):
    original_response: str = Field(description="First draft response")
    reflection: ReflectionCritique = Field(description="Self-critique")
    improved_response: str = Field(description="Refined response")
    improvements_made: list[str] = Field(description="What was changed")
    final_quality: int = Field(description="Final quality score 1-10")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Reflection Agent",
        instructions=[
            f"You improve responses through {cfg['reflection_rounds']} rounds of reflection.",
            "First generate an initial response.",
            "Then critically evaluate your own output.",
            "Finally, produce an improved version.",
            "Be honest about weaknesses to improve.",
        ],
        output_schema=ReflectedOutput,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Reflection Agent - Demo")
    print("=" * 60)
    
    task = "Explain quantum computing to a 10-year-old"
    print(f"\n📝 Task: {task}")
    
    response = agent.run(f"""
    Task: {task}
    
    Process:
    1. Write an initial response
    2. Critically reflect on it
    3. Produce an improved version
    """)
    
    if isinstance(response.content, ReflectedOutput):
        r = response.content
        print(f"\n📄 Original (Quality: {r.reflection.quality_score}/10):")
        print(f"   {r.original_response[:150]}...")
        print(f"\n🔍 Reflection:")
        print(f"   Strengths: {', '.join(r.reflection.strengths[:2])}")
        print(f"   Weaknesses: {', '.join(r.reflection.weaknesses[:2])}")
        print(f"\n✨ Improved (Quality: {r.final_quality}/10):")
        print(f"   {r.improved_response[:200]}...")
        print(f"\n🔧 Changes Made: {', '.join(r.improvements_made[:3])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reflection-rounds", "-r", type=int, default=DEFAULT_CONFIG["reflection_rounds"])
    args = parser.parse_args()
    run_demo(get_agent(config={"reflection_rounds": args.reflection_rounds}), {"reflection_rounds": args.reflection_rounds})

if __name__ == "__main__": main()
