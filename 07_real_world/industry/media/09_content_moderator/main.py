"""
Example #169: Content Moderator Agent
Category: industry/media
DESCRIPTION: Moderates user-generated content for policy violations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"platform_type": "social_media", "content_type": "comments", "strictness": "moderate"}

class ContentReview(BaseModel):
    content_id: str = Field(description="Content identifier")
    content_preview: str = Field(description="Content preview")
    decision: str = Field(description="approve/flag/remove")
    violation_types: list[str] = Field(description="Types of violations if any")
    confidence: int = Field(description="Confidence in decision 0-100")
    explanation: str = Field(description="Reason for decision")

class ModerationReport(BaseModel):
    total_reviewed: int = Field(description="Total items reviewed")
    approved: int = Field(description="Approved count")
    flagged: int = Field(description="Flagged for review")
    removed: int = Field(description="Removed count")
    reviews: list[ContentReview] = Field(description="Individual reviews")
    common_violations: list[str] = Field(description="Most common violation types")
    trend_alerts: list[str] = Field(description="Concerning trends")
    policy_recommendations: list[str] = Field(description="Policy update suggestions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Content Moderator",
        instructions=[
            "You are an expert content moderation specialist.",
            f"Moderate {cfg['content_type']} on {cfg['platform_type']} platforms",
            f"Apply {cfg['strictness']} strictness level",
            "Check for hate speech, harassment, spam, and inappropriate content",
            "Balance free expression with community safety",
            "Provide clear explanations for decisions",
        ],
        output_schema=ModerationReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Content Moderator Agent - Demo")
    print("=" * 60)
    sample_content = """Sample comments for review:
1. "Great product, really helped me!"
2. "This is absolute garbage, worst purchase ever!!!"
3. "Check out my site for FREE stuff: spam.example.com"
4. "Normal discussion about the topic"
5. "Some potentially concerning content here" """
    query = f"""Moderate this content:
{sample_content}

Apply {config['strictness']} moderation for {config['platform_type']} {config['content_type']}."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ModerationReport):
        print(f"\n📊 Moderation Summary:")
        print(f"  ✅ Approved: {result.approved}")
        print(f"  ⚠️ Flagged: {result.flagged}")
        print(f"  ❌ Removed: {result.removed}")
        print(f"\n📝 Reviews:")
        for r in result.reviews[:4]:
            icon = "✅" if r.decision == "approve" else "⚠️" if r.decision == "flag" else "❌"
            print(f"  {icon} [{r.decision}] {r.content_preview[:40]}...")
            if r.violation_types:
                print(f"     Violations: {', '.join(r.violation_types)}")
        print(f"\n⚠️ Common Issues: {', '.join(result.common_violations[:3])}")

def main():
    parser = argparse.ArgumentParser(description="Content Moderator Agent")
    parser.add_argument("--platform", "-p", default=DEFAULT_CONFIG["platform_type"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["content_type"])
    parser.add_argument("--strictness", "-s", default=DEFAULT_CONFIG["strictness"])
    args = parser.parse_args()
    config = {"platform_type": args.platform, "content_type": args.type, "strictness": args.strictness}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
