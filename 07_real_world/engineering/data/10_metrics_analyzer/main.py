"""
Example #090: Metrics Analyzer
Category: engineering/data
DESCRIPTION: Analyzes business metrics - trends, correlations, drivers, forecasts
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"metric": "revenue"}

class TrendAnalysis(BaseModel):
    direction: str = Field(description="increasing, decreasing, stable")
    rate: str = Field(description="Rate of change")
    seasonality: str = Field(description="Seasonal patterns observed")

class DriverAnalysis(BaseModel):
    driver: str = Field(description="Contributing factor")
    correlation: str = Field(description="positive, negative, none")
    strength: str = Field(description="strong, moderate, weak")
    explanation: str = Field(description="How this drives the metric")

class MetricsReport(BaseModel):
    metric_name: str = Field(description="Metric analyzed")
    current_value: str = Field(description="Latest value")
    trend: TrendAnalysis = Field(description="Trend analysis")
    top_drivers: list[DriverAnalysis] = Field(description="Key drivers")
    forecast: str = Field(description="Next period forecast")
    risks: list[str] = Field(description="Risks to monitor")
    opportunities: list[str] = Field(description="Growth opportunities")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Metrics Analyzer",
        instructions=[
            "Perform deep analysis of business metrics",
            "Identify trends, seasonality, and inflection points",
            "Discover correlations with other metrics",
            "Determine key drivers and their impact",
            "Generate forecasts with confidence ranges"
        ],
        output_schema=MetricsReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Metrics Analyzer - Demo\n" + "=" * 60)
    query = f"""Analyze this {config['metric']} metric:

Monthly Revenue (Last 12 months):
Jan: $1.8M, Feb: $1.9M, Mar: $2.1M, Apr: $2.0M
May: $2.2M, Jun: $2.1M, Jul: $1.9M, Aug: $2.0M
Sep: $2.3M, Oct: $2.4M, Nov: $2.5M, Dec: $2.8M

Related metrics:
- Marketing spend: increased 20% in Q4
- New customers: up 15% YoY
- Avg order value: $125 (stable)
- Conversion rate: 3.2% (up from 2.8%)
- Customer churn: 5% monthly (stable)
- Website traffic: up 25% from SEO"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, MetricsReport):
        print(f"\nMetric: {result.metric_name}")
        print(f"Current Value: {result.current_value}")
        print(f"\nTrend: {result.trend.direction} ({result.trend.rate})")
        print(f"Seasonality: {result.trend.seasonality}")
        print(f"\nTop Drivers:")
        for d in result.top_drivers[:3]:
            print(f"  • {d.driver}: {d.correlation} ({d.strength})")
        print(f"\nForecast: {result.forecast}")
        print(f"\nRisks: {', '.join(result.risks[:3])}")
        print(f"Opportunities: {', '.join(result.opportunities[:3])}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metric", "-m", default=DEFAULT_CONFIG["metric"])
    args = parser.parse_args()
    run_demo(get_agent(), {"metric": args.metric})

if __name__ == "__main__": main()
