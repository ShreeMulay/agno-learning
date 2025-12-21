"""
Example #179: Peer Reviewer Agent
Category: research/science
DESCRIPTION: Provides constructive peer review feedback
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"paper_type": "empirical", "journal_tier": "top", "review_focus": "comprehensive"}

class ReviewSection(BaseModel):
    section: str = Field(description="Paper section")
    strengths: list[str] = Field(description="Section strengths")
    weaknesses: list[str] = Field(description="Section weaknesses")
    suggestions: list[str] = Field(description="Improvement suggestions")

class PeerReview(BaseModel):
    overall_assessment: str = Field(description="Overall assessment")
    recommendation: str = Field(description="accept/minor/major/reject")
    summary: str = Field(description="Review summary")
    major_issues: list[str] = Field(description="Major issues")
    minor_issues: list[str] = Field(description="Minor issues")
    section_reviews: list[ReviewSection] = Field(description="Section-by-section review")
    methodology_assessment: str = Field(description="Methodology assessment")
    contribution_assessment: str = Field(description="Contribution to field")
    constructive_suggestions: list[str] = Field(description="Constructive suggestions")
    questions_for_authors: list[str] = Field(description="Questions for authors")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Peer Reviewer",
        instructions=[
            "You are an expert scientific peer reviewer.",
            f"Review {cfg['paper_type']} papers for {cfg['journal_tier']}-tier journals",
            f"Provide {cfg['review_focus']} review",
            "Be constructive and specific",
            "Identify both strengths and weaknesses",
            "Suggest concrete improvements",
        ],
        output_schema=PeerReview,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Peer Reviewer Agent - Demo")
    print("=" * 60)
    sample = """Study examines remote work productivity using survey of 500 employees.
Results show 23% increase in self-reported productivity. Limitations include
self-selection bias and lack of objective measures."""
    query = f"""Review this paper:
{sample}

Type: {config['paper_type']}
Journal Tier: {config['journal_tier']}
Focus: {config['review_focus']}"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, PeerReview):
        print(f"\n📊 Overall: {result.overall_assessment}")
        print(f"📋 Recommendation: {result.recommendation.upper()}")
        print(f"\n📝 Summary: {result.summary}")
        print(f"\n❌ Major Issues:")
        for issue in result.major_issues[:2]:
            print(f"  • {issue}")
        print(f"\n⚠️ Minor Issues:")
        for issue in result.minor_issues[:2]:
            print(f"  • {issue}")
        print(f"\n💡 Suggestions:")
        for s in result.constructive_suggestions[:2]:
            print(f"  • {s}")

def main():
    parser = argparse.ArgumentParser(description="Peer Reviewer Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["paper_type"])
    parser.add_argument("--tier", default=DEFAULT_CONFIG["journal_tier"])
    parser.add_argument("--focus", "-f", default=DEFAULT_CONFIG["review_focus"])
    args = parser.parse_args()
    config = {"paper_type": args.type, "journal_tier": args.tier, "review_focus": args.focus}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
