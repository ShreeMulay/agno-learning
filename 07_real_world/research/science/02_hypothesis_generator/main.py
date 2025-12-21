"""
Example #172: Hypothesis Generator Agent
Category: research/science
DESCRIPTION: Generates testable research hypotheses based on observations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"field": "neuroscience", "observation": "sleep deprivation affects memory", "approach": "experimental"}

class Hypothesis(BaseModel):
    statement: str = Field(description="Hypothesis statement")
    null_hypothesis: str = Field(description="Null hypothesis")
    variables: dict = Field(description="Independent and dependent variables")
    testability: int = Field(description="Testability score 0-100")
    novelty: int = Field(description="Novelty score 0-100")
    potential_impact: str = Field(description="Potential research impact")

class HypothesisGeneration(BaseModel):
    observation: str = Field(description="Initial observation")
    field: str = Field(description="Research field")
    hypotheses: list[Hypothesis] = Field(description="Generated hypotheses")
    recommended_hypothesis: str = Field(description="Most promising hypothesis")
    theoretical_framework: str = Field(description="Relevant theoretical framework")
    key_assumptions: list[str] = Field(description="Key assumptions")
    potential_confounds: list[str] = Field(description="Potential confounding variables")
    next_steps: list[str] = Field(description="Recommended next steps")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Hypothesis Generator",
        instructions=[
            "You are an expert research hypothesis generator.",
            f"Generate hypotheses in the field of {cfg['field']}",
            f"Use {cfg['approach']} research approach",
            "Create specific, testable hypotheses",
            "Consider theoretical frameworks and confounds",
            "Ensure scientific rigor",
        ],
        output_schema=HypothesisGeneration,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Hypothesis Generator Agent - Demo")
    print("=" * 60)
    query = f"""Generate research hypotheses:
- Field: {config['field']}
- Observation: {config['observation']}
- Approach: {config['approach']}

Create testable hypotheses with variables defined."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, HypothesisGeneration):
        print(f"\n🔬 Field: {result.field}")
        print(f"👁️ Observation: {result.observation}")
        print(f"\n📊 Hypotheses:")
        for h in result.hypotheses[:3]:
            print(f"\n  H: {h.statement}")
            print(f"  H0: {h.null_hypothesis}")
            print(f"  Testability: {h.testability}% | Novelty: {h.novelty}%")
        print(f"\n⭐ Recommended: {result.recommended_hypothesis}")
        print(f"\n📚 Framework: {result.theoretical_framework}")

def main():
    parser = argparse.ArgumentParser(description="Hypothesis Generator Agent")
    parser.add_argument("--field", "-f", default=DEFAULT_CONFIG["field"])
    parser.add_argument("--observation", "-o", default=DEFAULT_CONFIG["observation"])
    parser.add_argument("--approach", "-a", default=DEFAULT_CONFIG["approach"])
    args = parser.parse_args()
    config = {"field": args.field, "observation": args.observation, "approach": args.approach}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
