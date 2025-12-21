"""
Example #177: Methodology Advisor Agent
Category: research/science
DESCRIPTION: Advises on appropriate research methodologies
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"research_question": "How does social media affect teen mental health?", "field": "psychology", "constraints": "limited budget, 6 months"}

class MethodologyOption(BaseModel):
    name: str = Field(description="Methodology name")
    approach: str = Field(description="qualitative/quantitative/mixed")
    description: str = Field(description="Brief description")
    strengths: list[str] = Field(description="Strengths for this study")
    weaknesses: list[str] = Field(description="Weaknesses/limitations")
    feasibility: int = Field(description="Feasibility score 0-100")

class MethodologyAdvice(BaseModel):
    research_question: str = Field(description="Research question")
    recommended_approach: str = Field(description="Recommended approach")
    methodology_options: list[MethodologyOption] = Field(description="Methodology options")
    top_recommendation: str = Field(description="Top recommendation with rationale")
    data_collection_methods: list[str] = Field(description="Data collection methods")
    sampling_strategy: str = Field(description="Sampling strategy")
    validity_considerations: list[str] = Field(description="Validity considerations")
    ethical_requirements: list[str] = Field(description="Ethical requirements")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Methodology Advisor",
        instructions=[
            "You are an expert research methodology advisor.",
            f"Advise on methodology for {cfg['field']} research",
            f"Consider constraints: {cfg['constraints']}",
            "Compare qualitative, quantitative, and mixed methods",
            "Consider validity and reliability",
            "Address ethical considerations",
        ],
        output_schema=MethodologyAdvice,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Methodology Advisor Agent - Demo")
    print("=" * 60)
    query = f"""Advise on methodology:
- Question: {config['research_question']}
- Field: {config['field']}
- Constraints: {config['constraints']}

Recommend appropriate research methodology."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, MethodologyAdvice):
        print(f"\n❓ Question: {result.research_question}")
        print(f"🎯 Recommended: {result.recommended_approach}")
        print(f"\n📐 Options:")
        for m in result.methodology_options[:3]:
            print(f"  • {m.name} ({m.approach}) - {m.feasibility}% feasible")
            print(f"    + {m.strengths[0]}")
            print(f"    - {m.weaknesses[0]}")
        print(f"\n⭐ Top Pick: {result.top_recommendation}")
        print(f"📊 Sampling: {result.sampling_strategy}")

def main():
    parser = argparse.ArgumentParser(description="Methodology Advisor Agent")
    parser.add_argument("--question", "-q", default=DEFAULT_CONFIG["research_question"])
    parser.add_argument("--field", "-f", default=DEFAULT_CONFIG["field"])
    parser.add_argument("--constraints", "-c", default=DEFAULT_CONFIG["constraints"])
    args = parser.parse_args()
    config = {"research_question": args.question, "field": args.field, "constraints": args.constraints}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
