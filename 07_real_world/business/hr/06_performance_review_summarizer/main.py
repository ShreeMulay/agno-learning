"""
Example #046: Performance Review Summarizer
Category: business/hr

DESCRIPTION:
Synthesizes 360-degree feedback from multiple reviewers into
actionable insights, themes, and development recommendations.

PATTERNS:
- Reasoning (theme extraction)
- Structured Output (ReviewSummary)
- Knowledge (performance frameworks)

ARGUMENTS:
- feedback (str): Multi-source feedback text
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "employee_name": "Jordan Lee",
    "role": "Product Manager",
    "review_period": "2024",
    "feedback": """
    MANAGER FEEDBACK (Sarah Chen, VP Product):
    Jordan has grown significantly this year. Led the checkout redesign that increased 
    conversion 15%. Strong stakeholder management and clear communication. Sometimes 
    takes on too much and could delegate more. Ready for senior PM role.
    Rating: Exceeds Expectations
    
    PEER FEEDBACK (Alex Kim, Engineering Lead):
    Great partner on the checkout project. Always prepared for sprint planning. 
    Could improve on technical understanding - sometimes proposes features without 
    understanding backend complexity. Very responsive to feedback though.
    
    PEER FEEDBACK (Maria Garcia, Designer):
    Jordan is a pleasure to work with. Respects design process and advocates for 
    user research. Excellent at synthesizing customer feedback. Meetings sometimes 
    run long - could be more concise.
    
    SKIP-LEVEL FEEDBACK (Tom Wilson, CPO):
    Impressed with Jordan's growth. Strategic thinking has improved. Recommend 
    investing in data analytics skills. Strong candidate for senior PM in 6-12 months.
    
    SELF ASSESSMENT (Jordan Lee):
    Proud of checkout redesign impact. Want to improve technical skills and 
    learn SQL for better data analysis. Goal: senior PM promotion by mid-2025.
    """,
}


class ThemeAnalysis(BaseModel):
    theme: str = Field(description="Identified theme")
    sentiment: str = Field(description="positive/neutral/developmental")
    frequency: int = Field(description="How many reviewers mentioned this")
    example_quote: str = Field(description="Representative quote")


class ReviewSummary(BaseModel):
    employee_name: str = Field(description="Employee name")
    role: str = Field(description="Current role")
    overall_rating: str = Field(description="Synthesized rating")
    executive_summary: str = Field(description="2-3 sentence summary")
    key_strengths: list[str] = Field(description="Top 3-5 strengths")
    development_areas: list[str] = Field(description="Areas for growth")
    themes: list[ThemeAnalysis] = Field(description="Recurring themes")
    promotion_readiness: str = Field(description="ready/almost ready/needs development")
    development_plan: list[str] = Field(description="Specific development actions")
    goals_for_next_period: list[str] = Field(description="Suggested goals")
    manager_talking_points: list[str] = Field(description="Key points for review meeting")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Performance Review Summarizer",
        instructions=[
            "You are an HR analytics expert specializing in performance reviews.",
            "Synthesize multi-source feedback into actionable insights.",
            "",
            "Analysis Approach:",
            "- Identify recurring themes across reviewers",
            "- Balance strengths with development areas",
            "- Look for patterns in feedback",
            "- Note alignment/misalignment with self-assessment",
            "",
            "Be constructive and specific in recommendations.",
            "Frame development areas as growth opportunities.",
            "Provide concrete, actionable development steps.",
        ],
        output_schema=ReviewSummary,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Performance Review Summarizer - Demo")
    print("=" * 60)
    
    feedback = config.get("feedback", DEFAULT_CONFIG["feedback"])
    name = config.get("employee_name", DEFAULT_CONFIG["employee_name"])
    
    response = agent.run(f"Summarize this 360 feedback for {name}:\n\n{feedback}")
    result = response.content
    
    if isinstance(result, ReviewSummary):
        print(f"\n👤 {result.employee_name} | {result.role}")
        print(f"⭐ Overall: {result.overall_rating}")
        
        print(f"\n📝 Summary:")
        print(f"   {result.executive_summary}")
        
        print(f"\n💪 Strengths:")
        for s in result.key_strengths:
            print(f"   ✅ {s}")
        
        print(f"\n📈 Development Areas:")
        for d in result.development_areas:
            print(f"   🔄 {d}")
        
        print(f"\n🔍 Themes Identified:")
        for t in result.themes:
            icon = {"positive": "🟢", "neutral": "🟡", "developmental": "🔵"}
            print(f"   {icon.get(t.sentiment, '⚪')} {t.theme} (mentioned by {t.frequency})")
        
        ready_icon = {"ready": "🚀", "almost ready": "📈", "needs development": "🌱"}
        print(f"\n{ready_icon.get(result.promotion_readiness, '?')} Promotion: {result.promotion_readiness.title()}")
        
        print(f"\n🎯 Development Plan:")
        for d in result.development_plan:
            print(f"   • {d}")
        
        print(f"\n💬 Manager Talking Points:")
        for p in result.manager_talking_points:
            print(f"   • {p}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Performance Review Summarizer")
    parser.add_argument("--feedback", "-f", type=str, default=DEFAULT_CONFIG["feedback"])
    parser.add_argument("--name", "-n", type=str, default=DEFAULT_CONFIG["employee_name"])
    args = parser.parse_args()
    config = {**DEFAULT_CONFIG, "feedback": args.feedback, "employee_name": args.name}
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
