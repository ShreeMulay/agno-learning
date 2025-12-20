"""
Example #049: Exit Interview Analyzer
Category: business/hr

DESCRIPTION:
Analyzes exit interview responses to extract themes, sentiment,
and actionable insights for improving retention.

PATTERNS:
- Reasoning (theme extraction)
- Structured Output (ExitAnalysis)
- Knowledge (retention factors)

ARGUMENTS:
- interviews (str): Exit interview transcripts/notes
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "interviews": """
    EXIT INTERVIEW 1 - Software Engineer, 2.5 years tenure
    Reason for leaving: Better opportunity
    "I loved my team and manager, but there wasn't a clear path to senior engineer.
    I asked about promotion criteria three times and never got a straight answer.
    The new company offered me a senior title and 25% raise."
    
    EXIT INTERVIEW 2 - Product Manager, 1 year tenure
    Reason for leaving: Culture fit
    "The work was interesting but the hours were unsustainable. I was regularly
    working until 9pm and expected to respond to Slack on weekends. My manager
    said that's just how startups are. I need better work-life balance."
    
    EXIT INTERVIEW 3 - Senior Engineer, 4 years tenure
    Reason for leaving: Career growth
    "After 4 years I'm still doing the same type of work. I asked to lead a team
    or work on new technologies but there was never budget. Meanwhile we keep
    hiring from outside for leadership roles. I felt stuck."
    
    EXIT INTERVIEW 4 - Marketing Manager, 1.5 years tenure
    Reason for leaving: Compensation
    "My market research showed I was 20% below market. HR said they couldn't
    adjust outside of annual reviews. I got a competing offer and they still
    wouldn't match. Felt undervalued."
    """,
}


class ThemeInsight(BaseModel):
    theme: str = Field(description="Identified theme")
    frequency: int = Field(description="How many mentioned this")
    severity: str = Field(description="critical/high/medium/low")
    sample_quotes: list[str] = Field(description="Representative quotes")
    root_cause: str = Field(description="Underlying issue")
    recommended_action: str = Field(description="What to do about it")


class ExitAnalysis(BaseModel):
    total_interviews: int = Field(description="Number of interviews analyzed")
    avg_tenure_months: float = Field(description="Average tenure")
    top_departure_reasons: list[str] = Field(description="Top reasons for leaving")
    themes: list[ThemeInsight] = Field(description="Key themes identified")
    sentiment_breakdown: dict = Field(description="positive/neutral/negative counts")
    retention_risk_areas: list[str] = Field(description="Areas with highest risk")
    quick_wins: list[str] = Field(description="Easy fixes to implement")
    strategic_recommendations: list[str] = Field(description="Longer-term changes")
    executive_summary: str = Field(description="2-3 sentence summary for leadership")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Exit Interview Analyzer",
        instructions=[
            "You are an HR analytics expert specializing in employee retention.",
            "Analyze exit interviews to extract actionable insights.",
            "",
            "Analysis Approach:",
            "- Identify recurring themes across interviews",
            "- Assess severity based on frequency and impact",
            "- Look for systemic issues vs individual cases",
            "- Prioritize recommendations by impact and effort",
            "",
            "Common Retention Factors:",
            "- Career growth and development",
            "- Compensation and benefits",
            "- Work-life balance",
            "- Management quality",
            "- Company culture and values",
            "- Recognition and appreciation",
        ],
        output_schema=ExitAnalysis,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Exit Interview Analyzer - Demo")
    print("=" * 60)
    
    interviews = config.get("interviews", DEFAULT_CONFIG["interviews"])
    
    response = agent.run(f"Analyze these exit interviews:\n\n{interviews}")
    result = response.content
    
    if isinstance(result, ExitAnalysis):
        print(f"\n📊 Analysis of {result.total_interviews} Exit Interviews")
        print(f"Average Tenure: {result.avg_tenure_months:.1f} months")
        
        print(f"\n🚪 Top Departure Reasons:")
        for r in result.top_departure_reasons:
            print(f"   • {r}")
        
        print(f"\n🔍 Key Themes:")
        for t in result.themes:
            sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
            print(f"\n   {sev_icon.get(t.severity, '⚪')} {t.theme} ({t.frequency} mentions)")
            print(f"   Root Cause: {t.root_cause}")
            print(f"   Action: {t.recommended_action}")
        
        print(f"\n⚠️ High-Risk Areas:")
        for r in result.retention_risk_areas:
            print(f"   • {r}")
        
        print(f"\n✨ Quick Wins:")
        for w in result.quick_wins:
            print(f"   • {w}")
        
        print(f"\n📈 Strategic Recommendations:")
        for r in result.strategic_recommendations:
            print(f"   • {r}")
        
        print(f"\n📝 Executive Summary:")
        print(f"   {result.executive_summary}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Exit Interview Analyzer")
    parser.add_argument("--interviews", "-i", type=str, default=DEFAULT_CONFIG["interviews"])
    args = parser.parse_args()
    agent = get_agent(config={"interviews": args.interviews})
    run_demo(agent, {"interviews": args.interviews})


if __name__ == "__main__":
    main()
