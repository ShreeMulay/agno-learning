"""
Example #024: CSAT Analyzer
Category: business/customer_success

DESCRIPTION:
Analyzes customer satisfaction survey responses to extract themes, identify
trends, and surface actionable insights. Processes both quantitative scores
and qualitative feedback to understand customer sentiment drivers.

PATTERNS:
- Knowledge (sentiment analysis)
- Structured Output (CSATAnalysis with themes)

ARGUMENTS:
- responses (str): CSAT survey responses. Default: sample data
- period (str): Analysis period. Default: "last 30 days"
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "responses": """
    CSAT Survey Responses (Last 30 Days):
    
    Response 1: Score 5/5
    "Absolutely love the new dashboard! The team was super helpful when I had questions."
    
    Response 2: Score 2/5
    "Support took 3 days to respond. By then I had already figured it out myself."
    
    Response 3: Score 4/5
    "Great product, just wish the mobile app was better."
    
    Response 4: Score 1/5
    "Billing issues for the 3rd month in a row. Nobody can fix it."
    
    Response 5: Score 5/5
    "Sarah from support was amazing. Resolved my issue in 10 minutes!"
    
    Response 6: Score 3/5
    "Product is okay. Nothing special but gets the job done."
    
    Response 7: Score 2/5
    "The new update broke half my workflows. Had to spend hours fixing them."
    
    Response 8: Score 4/5
    "Good value for money. Onboarding could be smoother though."
    
    Response 9: Score 5/5
    "Best decision we made switching from [Competitor]. Integration was seamless."
    
    Response 10: Score 1/5
    "Keep getting logged out randomly. Very frustrating."
    """,
    "period": "last 30 days",
}


# =============================================================================
# Output Schema
# =============================================================================

class ThemeAnalysis(BaseModel):
    """Analysis of a recurring theme."""
    
    theme: str = Field(description="Theme name")
    sentiment: str = Field(description="positive/negative/mixed")
    frequency: int = Field(description="Number of mentions")
    sample_quotes: list[str] = Field(description="Representative quotes")
    impact_on_score: str = Field(description="Impact on overall CSAT")
    actionable_insight: str = Field(description="What to do about it")


class ScoreDistribution(BaseModel):
    """CSAT score distribution."""
    
    promoters: int = Field(description="Scores 4-5 count")
    passives: int = Field(description="Score 3 count")
    detractors: int = Field(description="Scores 1-2 count")
    average_score: float = Field(description="Average CSAT score")
    nps_equivalent: int = Field(description="NPS-style score")


class TrendIndicator(BaseModel):
    """Trend in CSAT metrics."""
    
    metric: str = Field(description="What's trending")
    direction: str = Field(description="improving/declining/stable")
    magnitude: str = Field(description="Slight/moderate/significant")
    driver: str = Field(description="What's causing this trend")


class CSATAnalysis(BaseModel):
    """Complete CSAT analysis."""
    
    period: str = Field(description="Analysis period")
    total_responses: int = Field(description="Number of responses analyzed")
    distribution: ScoreDistribution = Field(description="Score distribution")
    positive_themes: list[ThemeAnalysis] = Field(description="What's working well")
    negative_themes: list[ThemeAnalysis] = Field(description="Pain points")
    trends: list[TrendIndicator] = Field(description="Identified trends")
    top_performers: list[str] = Field(description="Team members mentioned positively")
    priority_issues: list[str] = Field(description="Issues to address immediately")
    quick_wins: list[str] = Field(description="Easy improvements")
    strategic_recommendations: list[str] = Field(description="Long-term improvements")
    executive_summary: str = Field(description="One-paragraph summary for leadership")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the CSAT Analyzer agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for CSAT analysis
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="CSAT Analyzer",
        instructions=[
            "You are an expert customer experience analyst.",
            "Analyze CSAT data to extract meaningful insights and trends.",
            "",
            f"Analysis Period: {cfg['period']}",
            "",
            "CSAT Score Interpretation:",
            "- 5: Promoter - Highly satisfied, likely to recommend",
            "- 4: Satisfied - Generally happy, some room for improvement",
            "- 3: Passive - Neutral, at risk of churn",
            "- 2: Dissatisfied - Has issues, needs attention",
            "- 1: Detractor - Very unhappy, high churn risk",
            "",
            "Theme Extraction:",
            "- Look for recurring topics in feedback",
            "- Identify product areas, team performance, processes",
            "- Note competitive mentions",
            "- Extract specific feature feedback",
            "",
            "Analysis Approach:",
            "- Quantify themes by frequency and impact",
            "- Correlate themes with scores",
            "- Identify patterns and root causes",
            "- Prioritize by business impact",
            "",
            "Focus on actionable insights, not just observations.",
        ],
        output_schema=CSATAnalysis,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of CSAT analysis."""
    print("\n" + "=" * 60)
    print("  CSAT Analyzer - Demo")
    print("=" * 60)
    
    responses = config.get("responses", DEFAULT_CONFIG["responses"])
    period = config.get("period", DEFAULT_CONFIG["period"])
    
    query = f"""
    Analyze these CSAT survey responses:
    
    Period: {period}
    
    {responses}
    
    Extract themes, identify trends, and provide actionable recommendations.
    """
    
    print(f"\nPeriod: {period}")
    print("-" * 40)
    print("Analyzing CSAT responses...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, CSATAnalysis):
        print(f"\n{'='*50}")
        print(f"CSAT ANALYSIS REPORT")
        print(f"{'='*50}")
        
        d = result.distribution
        print(f"\n📊 Score Distribution ({result.total_responses} responses):")
        print(f"  Average Score: {d.average_score:.1f}/5")
        print(f"  NPS Equivalent: {d.nps_equivalent}")
        print(f"  Promoters (4-5): {d.promoters} | Passives (3): {d.passives} | Detractors (1-2): {d.detractors}")
        
        print(f"\n✅ What's Working Well:")
        for theme in result.positive_themes[:3]:
            print(f"\n  {theme.theme} ({theme.frequency} mentions)")
            print(f"    \"{theme.sample_quotes[0][:60]}...\"")
            print(f"    💡 {theme.actionable_insight}")
        
        print(f"\n❌ Pain Points:")
        for theme in result.negative_themes[:3]:
            print(f"\n  {theme.theme} ({theme.frequency} mentions)")
            print(f"    \"{theme.sample_quotes[0][:60]}...\"")
            print(f"    💡 {theme.actionable_insight}")
        
        print(f"\n📈 Trends:")
        for trend in result.trends[:3]:
            arrow = "↑" if trend.direction == "improving" else "↓" if trend.direction == "declining" else "→"
            print(f"  {arrow} {trend.metric}: {trend.direction} ({trend.magnitude})")
            print(f"    Driver: {trend.driver}")
        
        if result.top_performers:
            print(f"\n⭐ Top Performers: {', '.join(result.top_performers)}")
        
        print(f"\n🚨 Priority Issues:")
        for issue in result.priority_issues[:3]:
            print(f"  • {issue}")
        
        print(f"\n⚡ Quick Wins:")
        for win in result.quick_wins[:3]:
            print(f"  • {win}")
        
        print(f"\n🎯 Strategic Recommendations:")
        for rec in result.strategic_recommendations[:3]:
            print(f"  • {rec}")
        
        print(f"\n📋 Executive Summary:")
        print(f"  {result.executive_summary}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CSAT Analyzer - Extract insights from satisfaction surveys"
    )
    
    parser.add_argument(
        "--responses", "-r",
        type=str,
        default=DEFAULT_CONFIG["responses"],
        help="CSAT responses data"
    )
    parser.add_argument(
        "--period", "-p",
        type=str,
        default=DEFAULT_CONFIG["period"],
        help="Analysis period"
    )
    
    args = parser.parse_args()
    
    config = {
        "responses": args.responses,
        "period": args.period,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
