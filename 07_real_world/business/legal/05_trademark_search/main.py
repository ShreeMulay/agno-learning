"""
Example #055: Trademark Search Agent
Category: business/legal

DESCRIPTION:
Analyzes proposed brand names for potential trademark conflicts,
suggests alternatives, and provides registration guidance.

PATTERNS:
- Knowledge (trademark law)
- Structured Output (TrademarkAnalysis)
- Reasoning (conflict assessment)

ARGUMENTS:
- proposed_name (str): Brand name to check
- industry (str): Business category
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "proposed_name": "CloudSync Pro",
    "industry": "Cloud storage and file synchronization software",
    "geographic_scope": "United States",
}


class SimilarMark(BaseModel):
    mark: str = Field(description="Similar trademark")
    owner: str = Field(description="Mark owner")
    class_number: int = Field(description="Nice classification")
    status: str = Field(description="live/dead/pending")
    similarity_type: str = Field(description="identical/similar/phonetic/conceptual")
    risk_level: str = Field(description="high/medium/low")


class TrademarkAnalysis(BaseModel):
    proposed_mark: str = Field(description="The proposed name")
    industry: str = Field(description="Business category")
    distinctiveness: str = Field(description="generic/descriptive/suggestive/arbitrary/fanciful")
    registerability_score: int = Field(ge=0, le=100, description="Likelihood of registration")
    similar_marks_found: list[SimilarMark] = Field(description="Potentially conflicting marks")
    conflict_risk: str = Field(description="high/medium/low")
    recommended_classes: list[int] = Field(description="Nice classes to file in")
    strengths: list[str] = Field(description="What's good about this name")
    weaknesses: list[str] = Field(description="Concerns or issues")
    alternative_names: list[str] = Field(description="Suggested alternatives")
    next_steps: list[str] = Field(description="Recommended actions")
    summary: str = Field(description="Overall assessment")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Trademark Search Agent",
        instructions=[
            "You are a trademark attorney evaluating brand names.",
            "Assess registerability and potential conflicts.",
            "",
            "Distinctiveness Spectrum (weakest to strongest):",
            "- Generic: Cannot be registered (e.g., 'Computer Store')",
            "- Descriptive: Difficult, needs secondary meaning (e.g., 'Quick Delivery')",
            "- Suggestive: Registrable, suggests quality (e.g., 'Netflix')",
            "- Arbitrary: Strong, common word new context (e.g., 'Apple' for computers)",
            "- Fanciful: Strongest, invented word (e.g., 'Xerox')",
            "",
            "Conflict Analysis:",
            "- Check phonetic similarity",
            "- Check visual similarity",
            "- Check conceptual similarity",
            "- Consider related goods/services",
            "",
            "Common Nice Classes for Software:",
            "- Class 9: Software, apps",
            "- Class 35: Business services",
            "- Class 42: SaaS, cloud services",
        ],
        output_schema=TrademarkAnalysis,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Trademark Search Agent - Demo")
    print("=" * 60)
    
    name = config.get("proposed_name", DEFAULT_CONFIG["proposed_name"])
    industry = config.get("industry", DEFAULT_CONFIG["industry"])
    
    response = agent.run(f"Analyze trademark for: '{name}'\nIndustry: {industry}")
    result = response.content
    
    if isinstance(result, TrademarkAnalysis):
        print(f"\n🏷️ Proposed Mark: {result.proposed_mark}")
        print(f"Industry: {result.industry}")
        print(f"Distinctiveness: {result.distinctiveness}")
        print(f"Registerability Score: {result.registerability_score}%")
        
        risk_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        print(f"{risk_icon.get(result.conflict_risk, '?')} Conflict Risk: {result.conflict_risk}")
        
        if result.similar_marks_found:
            print(f"\n⚠️ Similar Marks Found:")
            for m in result.similar_marks_found:
                status = "🟢" if m.status == "dead" else "🔴"
                print(f"   {status} {m.mark} ({m.owner})")
                print(f"      Class {m.class_number} | {m.similarity_type} | Risk: {m.risk_level}")
        
        print(f"\n📋 Recommended Classes: {result.recommended_classes}")
        
        print(f"\n✅ Strengths:")
        for s in result.strengths:
            print(f"   • {s}")
        
        if result.weaknesses:
            print(f"\n⚠️ Weaknesses:")
            for w in result.weaknesses:
                print(f"   • {w}")
        
        print(f"\n💡 Alternative Names:")
        for a in result.alternative_names:
            print(f"   • {a}")
        
        print(f"\n➡️ Next Steps:")
        for n in result.next_steps:
            print(f"   • {n}")
        
        print(f"\n📝 {result.summary}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Trademark Search Agent")
    parser.add_argument("--name", "-n", type=str, default=DEFAULT_CONFIG["proposed_name"])
    parser.add_argument("--industry", "-i", type=str, default=DEFAULT_CONFIG["industry"])
    args = parser.parse_args()
    agent = get_agent(config={"proposed_name": args.name, "industry": args.industry})
    run_demo(agent, {"proposed_name": args.name, "industry": args.industry})


if __name__ == "__main__":
    main()
