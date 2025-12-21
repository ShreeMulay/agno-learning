"""
Example #089: Dashboard Builder
Category: engineering/data
DESCRIPTION: Designs dashboard layouts - chart selection, metrics, filters, drill-downs
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"dashboard_type": "executive_kpi"}

class ChartSpec(BaseModel):
    title: str = Field(description="Chart title")
    chart_type: str = Field(description="bar, line, pie, table, KPI card, etc.")
    metric: str = Field(description="Primary metric")
    dimensions: list[str] = Field(description="Breakdown dimensions")
    position: str = Field(description="Grid position: top-left, center, etc.")

class FilterSpec(BaseModel):
    name: str = Field(description="Filter name")
    field: str = Field(description="Data field to filter")
    filter_type: str = Field(description="dropdown, date-range, search")
    default_value: str = Field(description="Default selection")

class DashboardDesign(BaseModel):
    title: str = Field(description="Dashboard title")
    purpose: str = Field(description="Dashboard purpose")
    audience: str = Field(description="Target users")
    charts: list[ChartSpec] = Field(description="Chart specifications")
    filters: list[FilterSpec] = Field(description="Filter controls")
    refresh_rate: str = Field(description="Data refresh frequency")
    layout_notes: str = Field(description="Layout and UX notes")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Dashboard Builder",
        instructions=[
            "Design effective dashboards for specific audiences",
            "Select appropriate chart types for each metric",
            "Create logical layouts with visual hierarchy",
            "Define useful filters and drill-down paths",
            "Balance information density with clarity"
        ],
        output_schema=DashboardDesign, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Dashboard Builder - Demo\n" + "=" * 60)
    query = f"""Design a {config['dashboard_type']} dashboard:

Available metrics:
- Revenue (total, by region, by product)
- Orders (count, avg value)
- Customers (new, returning, churn)
- Conversion rate
- Customer satisfaction (NPS)
- Inventory levels
- Shipping times

Requirements:
- C-level executives need quick overview
- Ability to filter by date range and region
- Compare to prior period
- Mobile-friendly"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DashboardDesign):
        print(f"\n{result.title}")
        print(f"Audience: {result.audience}")
        print(f"Refresh: {result.refresh_rate}")
        print(f"\nCharts ({len(result.charts)}):")
        for c in result.charts:
            print(f"  [{c.position}] {c.title} ({c.chart_type})")
        print(f"\nFilters ({len(result.filters)}):")
        for f in result.filters:
            print(f"  - {f.name}: {f.filter_type}")
        print(f"\nLayout Notes: {result.layout_notes[:200]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dashboard-type", "-t", default=DEFAULT_CONFIG["dashboard_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"dashboard_type": args.dashboard_type})

if __name__ == "__main__": main()
