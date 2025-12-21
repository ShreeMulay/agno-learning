"""
Example #218: Editorial Board Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Publication editorial process with multiple reviewers and editors
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"publication": "tech_blog"}

class ReviewerFeedback(BaseModel):
    reviewer: str = Field(description="Reviewer role")
    rating: int = Field(description="Rating 1-5")
    strengths: list[str] = Field(description="Article strengths")
    improvements: list[str] = Field(description="Suggested improvements")
    recommendation: str = Field(description="publish, revise, reject")

class EditorialDecision(BaseModel):
    article_title: str = Field(description="Article title")
    decision: str = Field(description="publish, major_revision, minor_revision, reject")
    reviews: list[ReviewerFeedback] = Field(description="All reviewer feedback")
    publication_readiness: int = Field(description="Score 1-100")
    required_changes: list[str] = Field(description="Must-fix items before publication")
    suggested_changes: list[str] = Field(description="Nice-to-have improvements")
    publication_slot: str = Field(description="Recommended publication timing")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_content_reviewer(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Content Reviewer",
        instructions=[
            "You review articles for accuracy and depth.",
            "Check facts and claims.",
            "Evaluate argument structure.",
        ],
        markdown=True,
    )

def get_style_reviewer(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Style Reviewer",
        instructions=[
            "You review articles for readability and engagement.",
            "Check grammar, flow, and voice.",
            "Ensure audience appropriateness.",
        ],
        markdown=True,
    )

def get_editor_in_chief(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Editor in Chief",
        instructions=[
            "You make final publication decisions.",
            "Synthesize reviewer feedback.",
            "Balance quality with publication schedule.",
            "Provide clear direction for revisions.",
        ],
        output_schema=EditorialDecision,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_editor_in_chief(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Editorial Board - Demo")
    print("=" * 60)
    
    article = """
    Title: "The Future of Serverless Computing"
    Summary: Explores emerging trends in serverless architecture, including 
    edge computing integration, improved cold start performance, and 
    enterprise adoption patterns. Includes case studies from three 
    Fortune 500 companies.
    Word Count: 2,500
    Target Audience: Senior developers and architects"""
    
    content_rev = get_content_reviewer()
    style_rev = get_style_reviewer()
    editor = agent
    
    print(f"\n📰 Reviewing article submission...")
    
    content_review = content_rev.run(f"Review this article for content:\n{article}")
    style_review = style_rev.run(f"Review this article for style:\n{article}")
    
    decision_prompt = f"""
    Article Submission: {article}
    
    Content Review: {content_review.content}
    Style Review: {style_review.content}
    
    Make editorial decision for publication."""
    
    result = editor.run(decision_prompt)
    
    if isinstance(result.content, EditorialDecision):
        r = result.content
        dec_emoji = "✅" if r.decision == "publish" else "📝" if "revision" in r.decision else "❌"
        print(f"\n{dec_emoji} Decision: {r.decision.upper()}")
        print(f"📊 Publication Readiness: {r.publication_readiness}%")
        if r.required_changes:
            print(f"\n🔴 Required Changes:")
            for change in r.required_changes:
                print(f"  • {change}")
        if r.suggested_changes:
            print(f"\n🟡 Suggested Changes:")
            for change in r.suggested_changes[:3]:
                print(f"  • {change}")
        print(f"\n📅 Publication Slot: {r.publication_slot}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publication", "-p", default=DEFAULT_CONFIG["publication"])
    args = parser.parse_args()
    run_demo(get_agent(), {"publication": args.publication})

if __name__ == "__main__": main()
