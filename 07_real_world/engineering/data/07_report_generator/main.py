"""
Example #087: Report Generator
Category: engineering/data
DESCRIPTION: Generates business reports from data - executive summaries, insights, visualizations
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"report_type": "monthly_sales"}

class KeyMetric(BaseModel):
    name: str = Field(description="Metric name")
    value: str = Field(description="Current value")
    change: str = Field(description="Change from prior period")
    trend: str = Field(description="up, down, stable")

class Insight(BaseModel):
    finding: str = Field(description="Key finding")
    impact: str = Field(description="Business impact")
    action: str = Field(description="Recommended action")

class BusinessReport(BaseModel):
    title: str = Field(description="Report title")
    period: str = Field(description="Reporting period")
    executive_summary: str = Field(description="2-3 sentence summary")
    key_metrics: list[KeyMetric] = Field(description="Top metrics")
    insights: list[Insight] = Field(description="Key insights")
    chart_recommendations: list[str] = Field(description="Suggested visualizations")
    next_steps: list[str] = Field(description="Action items")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Report Generator",
        instructions=[
            "Generate executive-friendly business reports from data",
            "Summarize key metrics with period-over-period comparisons",
            "Extract actionable insights from trends",
            "Recommend appropriate visualizations",
            "Write in clear, non-technical language"
        ],
        output_schema=BusinessReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Report Generator - Demo\n" + "=" * 60)
    query = f"""Generate a {config['report_type']} report from this data:

Period: November 2024
Total Revenue: $2.4M (vs $2.1M last month)
Orders: 18,500 (vs 16,200)
Avg Order Value: $130 (vs $130)
New Customers: 3,200 (vs 2,800)
Customer Retention: 78% (vs 82%)
Top Product: Widget Pro (25% of sales)
Top Region: West Coast (40% of sales)
Returns: 4.2% (vs 3.8%)
Marketing Spend: $180K
Customer Acquisition Cost: $56"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, BusinessReport):
        print(f"\n{result.title}")
        print(f"Period: {result.period}")
        print(f"\nExecutive Summary:\n{result.executive_summary}")
        print(f"\nKey Metrics:")
        for m in result.key_metrics:
            arrow = "↑" if m.trend == "up" else "↓" if m.trend == "down" else "→"
            print(f"  {arrow} {m.name}: {m.value} ({m.change})")
        print(f"\nInsights:")
        for i in result.insights[:3]:
            print(f"  • {i.finding}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-type", "-t", default=DEFAULT_CONFIG["report_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"report_type": args.report_type})

if __name__ == "__main__": main()
