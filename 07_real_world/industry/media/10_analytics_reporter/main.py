"""
Example #170: Analytics Reporter Agent
Category: industry/media
DESCRIPTION: Generates comprehensive analytics reports for media performance
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"report_type": "weekly", "platform": "all", "focus": "engagement"}

class MetricHighlight(BaseModel):
    metric: str = Field(description="Metric name")
    value: str = Field(description="Current value")
    change: str = Field(description="Change from previous period")
    trend: str = Field(description="up/down/stable")
    insight: str = Field(description="Key insight")

class AnalyticsReport(BaseModel):
    report_period: str = Field(description="Reporting period")
    executive_summary: str = Field(description="Executive summary")
    key_metrics: list[MetricHighlight] = Field(description="Key metric highlights")
    top_performing_content: list[str] = Field(description="Best performing content")
    underperforming_areas: list[str] = Field(description="Areas needing attention")
    audience_insights: str = Field(description="Audience behavior insights")
    recommendations: list[str] = Field(description="Action recommendations")
    goals_progress: dict = Field(description="Progress toward goals")
    next_period_focus: list[str] = Field(description="Focus areas for next period")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Analytics Reporter",
        instructions=[
            "You are an expert media analytics specialist.",
            f"Generate {cfg['report_type']} reports for {cfg['platform']} platforms",
            f"Focus analysis on {cfg['focus']} metrics",
            "Translate data into actionable insights",
            "Highlight wins and areas for improvement",
            "Provide clear recommendations",
        ],
        output_schema=AnalyticsReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Analytics Reporter Agent - Demo")
    print("=" * 60)
    query = f"""Generate analytics report:
- Report Type: {config['report_type']}
- Platform: {config['platform']}
- Focus: {config['focus']}

Create comprehensive performance analysis."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, AnalyticsReport):
        print(f"\n📊 {result.report_period} Analytics Report")
        print(f"\n📝 Summary: {result.executive_summary}")
        print(f"\n📈 Key Metrics:")
        for m in result.key_metrics[:4]:
            icon = "📈" if m.trend == "up" else "📉" if m.trend == "down" else "➡️"
            print(f"  {icon} {m.metric}: {m.value} ({m.change})")
        print(f"\n🏆 Top Content:")
        for c in result.top_performing_content[:3]:
            print(f"  • {c}")
        print(f"\n💡 Recommendations:")
        for r in result.recommendations[:3]:
            print(f"  • {r}")
        print(f"\n🎯 Next Period Focus: {', '.join(result.next_period_focus[:3])}")

def main():
    parser = argparse.ArgumentParser(description="Analytics Reporter Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["report_type"])
    parser.add_argument("--platform", "-p", default=DEFAULT_CONFIG["platform"])
    parser.add_argument("--focus", "-f", default=DEFAULT_CONFIG["focus"])
    args = parser.parse_args()
    config = {"report_type": args.type, "platform": args.platform, "focus": args.focus}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
