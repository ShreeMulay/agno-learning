"""
Example #086: Anomaly Detector
Category: engineering/data
DESCRIPTION: Detects anomalies in data patterns - statistical outliers, trend breaks, missing data
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"metric": "daily_revenue"}

class Anomaly(BaseModel):
    timestamp: str = Field(description="When anomaly occurred")
    metric: str = Field(description="Affected metric")
    expected_value: float = Field(description="Expected value")
    actual_value: float = Field(description="Actual value")
    deviation_pct: float = Field(description="Percentage deviation")
    severity: str = Field(description="critical, warning, info")
    likely_cause: str = Field(description="Probable explanation")

class AnomalyReport(BaseModel):
    metric_name: str = Field(description="Metric analyzed")
    time_range: str = Field(description="Analysis period")
    anomalies: list[Anomaly] = Field(description="Detected anomalies")
    baseline_stats: str = Field(description="Normal range/pattern")
    trend_analysis: str = Field(description="Overall trend observation")
    recommendations: list[str] = Field(description="Actions to take")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Anomaly Detector",
        instructions=[
            "Analyze time series data for statistical anomalies",
            "Detect outliers using standard deviation and IQR methods",
            "Identify trend breaks and seasonal pattern violations",
            "Flag missing data periods and sudden changes",
            "Suggest likely causes based on patterns"
        ],
        output_schema=AnomalyReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Anomaly Detector - Demo\n" + "=" * 60)
    query = f"""Analyze this time series for anomalies:
Metric: {config['metric']}

Recent data (last 14 days):
Day 1: $125,000
Day 2: $118,000
Day 3: $132,000
Day 4: $127,000
Day 5: $15,000  <- Drop
Day 6: $8,000   <- Drop
Day 7: $145,000 <- Weekend spike
Day 8: $128,000
Day 9: $131,000
Day 10: $0      <- Missing?
Day 11: $126,000
Day 12: $490,000 <- Spike
Day 13: $129,000
Day 14: $124,000

Historical average: ~$125,000/day (weekdays), ~$140,000 (weekends)"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, AnomalyReport):
        print(f"\nMetric: {result.metric_name}")
        print(f"Period: {result.time_range}")
        print(f"Baseline: {result.baseline_stats}")
        print(f"\nAnomalies Found ({len(result.anomalies)}):")
        for a in result.anomalies:
            print(f"  [{a.severity.upper()}] {a.timestamp}: {a.deviation_pct:+.1f}%")
            print(f"    Expected: ${a.expected_value:,.0f}, Actual: ${a.actual_value:,.0f}")
            print(f"    Cause: {a.likely_cause}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metric", "-m", default=DEFAULT_CONFIG["metric"])
    args = parser.parse_args()
    run_demo(get_agent(), {"metric": args.metric})

if __name__ == "__main__": main()
