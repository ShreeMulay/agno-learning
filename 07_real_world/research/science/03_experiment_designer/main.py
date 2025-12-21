"""
Example #173: Experiment Designer Agent
Category: research/science
DESCRIPTION: Designs rigorous research experiments
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"hypothesis": "caffeine improves cognitive performance", "field": "psychology", "resources": "moderate"}

class ExperimentDesign(BaseModel):
    hypothesis: str = Field(description="Hypothesis being tested")
    design_type: str = Field(description="Experimental design type")
    sample_size: int = Field(description="Recommended sample size")
    sample_criteria: list[str] = Field(description="Inclusion/exclusion criteria")
    variables: dict = Field(description="Variables and operationalization")
    procedure: list[str] = Field(description="Step-by-step procedure")
    controls: list[str] = Field(description="Control measures")
    materials: list[str] = Field(description="Required materials")
    analysis_plan: str = Field(description="Statistical analysis plan")
    ethical_considerations: list[str] = Field(description="Ethical considerations")
    timeline: str = Field(description="Estimated timeline")
    limitations: list[str] = Field(description="Design limitations")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Experiment Designer",
        instructions=[
            "You are an expert research experiment designer.",
            f"Design experiments in {cfg['field']}",
            f"Work within {cfg['resources']} resource constraints",
            "Ensure rigorous methodology",
            "Address validity and reliability",
            "Include ethical considerations",
        ],
        output_schema=ExperimentDesign,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Experiment Designer Agent - Demo")
    print("=" * 60)
    query = f"""Design an experiment:
- Hypothesis: {config['hypothesis']}
- Field: {config['field']}
- Resources: {config['resources']}

Create a rigorous experimental design."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ExperimentDesign):
        print(f"\n🔬 Hypothesis: {result.hypothesis}")
        print(f"📐 Design: {result.design_type}")
        print(f"👥 Sample: n={result.sample_size}")
        print(f"\n📋 Procedure:")
        for i, step in enumerate(result.procedure[:4], 1):
            print(f"  {i}. {step}")
        print(f"\n🎛️ Controls: {', '.join(result.controls[:3])}")
        print(f"📊 Analysis: {result.analysis_plan}")
        print(f"⏱️ Timeline: {result.timeline}")

def main():
    parser = argparse.ArgumentParser(description="Experiment Designer Agent")
    parser.add_argument("--hypothesis", "-h", default=DEFAULT_CONFIG["hypothesis"])
    parser.add_argument("--field", "-f", default=DEFAULT_CONFIG["field"])
    parser.add_argument("--resources", "-r", default=DEFAULT_CONFIG["resources"])
    args = parser.parse_args()
    config = {"hypothesis": args.hypothesis, "field": args.field, "resources": args.resources}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
