"""
Example #050: Diversity Metrics Reporter
Category: business/hr

DESCRIPTION:
Analyzes workforce demographics to generate DEI reports,
identify gaps, and recommend improvement initiatives.

PATTERNS:
- Structured Output (DEIReport)
- Reasoning (gap analysis)
- Knowledge (DEI benchmarks)

ARGUMENTS:
- demographics (str): Workforce demographic data
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "demographics": """
    WORKFORCE DEMOGRAPHICS - Q4 2024
    Total Employees: 250
    
    BY DEPARTMENT:
    Engineering (100): 78% male, 22% female, 2% non-binary
    Product (30): 55% male, 43% female, 2% non-binary
    Sales (50): 60% male, 40% female
    Marketing (25): 35% male, 65% female
    HR (15): 20% male, 80% female
    Finance (20): 50% male, 50% female
    Executive (10): 80% male, 20% female
    
    BY LEVEL:
    Individual Contributors (180): 58% male, 40% female, 2% non-binary
    Managers (50): 65% male, 35% female
    Directors (15): 75% male, 25% female
    VPs/C-Suite (5): 80% male, 20% female
    
    BY ETHNICITY (company-wide):
    White: 55%
    Asian: 28%
    Hispanic/Latino: 8%
    Black: 5%
    Other/Mixed: 4%
    
    HIRING THIS YEAR:
    Total Hires: 45
    Women: 42%
    Underrepresented minorities: 22%
    
    ATTRITION THIS YEAR:
    Total Departures: 30
    Women: 48% (higher than workforce %)
    Underrepresented minorities: 18%
    """,
    "company_name": "TechCorp Inc",
}


class DiversityMetric(BaseModel):
    category: str = Field(description="What's being measured")
    current_value: str = Field(description="Current percentage/number")
    benchmark: str = Field(description="Industry benchmark")
    gap: str = Field(description="Gap to benchmark")
    trend: str = Field(description="improving/stable/declining")


class DEIReport(BaseModel):
    company_name: str = Field(description="Company name")
    report_period: str = Field(description="Reporting period")
    total_headcount: int = Field(description="Total employees")
    executive_summary: str = Field(description="2-3 sentence summary")
    key_metrics: list[DiversityMetric] = Field(description="Key diversity metrics")
    strengths: list[str] = Field(description="Areas doing well")
    gaps: list[str] = Field(description="Areas needing improvement")
    risk_areas: list[str] = Field(description="Attrition/culture risks")
    recommendations: list[str] = Field(description="Prioritized actions")
    goals_for_next_year: list[str] = Field(description="Measurable goals")
    benchmark_sources: list[str] = Field(description="Industry benchmarks used")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Diversity Metrics Reporter",
        instructions=[
            "You are a DEI analytics expert.",
            "Analyze workforce demographics objectively and constructively.",
            "",
            "Industry Benchmarks (Tech):",
            "- Women in tech: 28-32%",
            "- Women in engineering: 20-25%",
            "- Women in leadership: 25-30%",
            "- URMs in tech: 15-20%",
            "",
            "Analysis Approach:",
            "- Compare to industry benchmarks",
            "- Look at pipeline vs leadership representation",
            "- Identify attrition disparities",
            "- Note intersectional patterns",
            "",
            "Keep recommendations specific and actionable.",
            "Focus on systemic changes, not just numbers.",
        ],
        output_schema=DEIReport,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Diversity Metrics Reporter - Demo")
    print("=" * 60)
    
    demographics = config.get("demographics", DEFAULT_CONFIG["demographics"])
    company = config.get("company_name", DEFAULT_CONFIG["company_name"])
    
    response = agent.run(f"Generate DEI report for {company}:\n\n{demographics}")
    result = response.content
    
    if isinstance(result, DEIReport):
        print(f"\n📊 DEI Report: {result.company_name}")
        print(f"Period: {result.report_period} | Headcount: {result.total_headcount}")
        
        print(f"\n📝 Summary:")
        print(f"   {result.executive_summary}")
        
        print(f"\n📈 Key Metrics:")
        for m in result.key_metrics:
            trend_icon = {"improving": "↗️", "stable": "➡️", "declining": "↘️"}
            print(f"   {trend_icon.get(m.trend, '?')} {m.category}")
            print(f"     Current: {m.current_value} | Benchmark: {m.benchmark} | Gap: {m.gap}")
        
        print(f"\n✅ Strengths:")
        for s in result.strengths:
            print(f"   • {s}")
        
        print(f"\n⚠️ Gaps:")
        for g in result.gaps:
            print(f"   • {g}")
        
        print(f"\n🚨 Risk Areas:")
        for r in result.risk_areas:
            print(f"   • {r}")
        
        print(f"\n🎯 Recommendations:")
        for i, r in enumerate(result.recommendations, 1):
            print(f"   {i}. {r}")
        
        print(f"\n📅 Goals for Next Year:")
        for g in result.goals_for_next_year:
            print(f"   • {g}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Diversity Metrics Reporter")
    parser.add_argument("--demographics", "-d", type=str, default=DEFAULT_CONFIG["demographics"])
    args = parser.parse_args()
    agent = get_agent(config={"demographics": args.demographics})
    run_demo(agent, {"demographics": args.demographics})


if __name__ == "__main__":
    main()
