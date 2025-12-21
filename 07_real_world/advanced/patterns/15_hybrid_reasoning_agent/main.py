"""
Example #235: Hybrid Reasoning Agent
Category: advanced/patterns
DESCRIPTION: Agent combining multiple reasoning strategies for complex problems
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"reasoning_modes": ["deductive", "inductive", "analogical"]}

class ReasoningStep(BaseModel):
    mode: str = Field(description="Reasoning mode used")
    premise: str = Field(description="Starting point")
    inference: str = Field(description="Conclusion drawn")
    confidence: float = Field(description="Confidence 0-1")

class HybridReasoningResult(BaseModel):
    problem: str = Field(description="The problem being solved")
    reasoning_chain: list[ReasoningStep] = Field(description="Steps in reasoning")
    modes_used: list[str] = Field(description="Reasoning modes applied")
    conclusion: str = Field(description="Final conclusion")
    confidence: float = Field(description="Overall confidence")
    alternative_conclusions: list[str] = Field(description="Other possible answers")
    reasoning_quality: str = Field(description="Assessment of reasoning quality")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    modes = cfg.get("reasoning_modes", ["deductive", "inductive", "analogical"])
    return Agent(
        model=model or default_model(),
        name="Hybrid Reasoning Agent",
        instructions=[
            f"You combine multiple reasoning strategies: {modes}.",
            "Deductive: Apply general rules to specific cases.",
            "Inductive: Generalize from specific observations.",
            "Analogical: Draw parallels from similar situations.",
            "Use the most appropriate mode for each step.",
            "Show your reasoning chain explicitly.",
        ],
        output_schema=HybridReasoningResult,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Hybrid Reasoning Agent - Demo")
    print("=" * 60)
    
    problem = """
    A new social media platform is gaining users rapidly. 
    Based on patterns from Facebook, Twitter, and TikTok, 
    and given that user growth typically follows S-curves,
    will this platform reach 1 billion users within 5 years?
    """
    
    print(f"\n🧩 Problem: {problem.strip()}")
    print(f"🔧 Reasoning modes: {config.get('reasoning_modes', DEFAULT_CONFIG['reasoning_modes'])}")
    
    response = agent.run(f"Solve this problem using hybrid reasoning:\n{problem}")
    
    if isinstance(response.content, HybridReasoningResult):
        r = response.content
        print(f"\n🔗 Reasoning Chain:")
        for i, step in enumerate(r.reasoning_chain, 1):
            print(f"   {i}. [{step.mode.upper()}] {step.premise}")
            print(f"      → {step.inference} (confidence: {step.confidence:.0%})")
        print(f"\n🎯 Conclusion: {r.conclusion}")
        print(f"📊 Overall Confidence: {r.confidence:.0%}")
        print(f"🔍 Modes Used: {', '.join(r.modes_used)}")
        print(f"⚖️ Quality: {r.reasoning_quality}")
        if r.alternative_conclusions:
            print(f"🔀 Alternatives: {', '.join(r.alternative_conclusions[:2])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reasoning-modes", "-r", nargs="+", default=DEFAULT_CONFIG["reasoning_modes"])
    args = parser.parse_args()
    run_demo(get_agent(config={"reasoning_modes": args.reasoning_modes}), {"reasoning_modes": args.reasoning_modes})

if __name__ == "__main__": main()
