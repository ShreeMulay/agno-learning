"""
Example #076: Alert Tuner
Category: engineering/devops
DESCRIPTION: Analyzes alerting rules to reduce noise and improve signal.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"alerts": "CPU > 80% (fires 50x/day), Memory > 90% (fires 5x/day), Disk > 95% (fires 2x/week)"}

class AlertRecommendation(BaseModel):
    alert_name: str = Field(description="Alert name")
    current_threshold: str = Field(description="Current setting")
    recommendation: str = Field(description="Suggested change")
    reason: str = Field(description="Why change")

class AlertTuning(BaseModel):
    noisy_alerts: list[AlertRecommendation] = Field(description="Alerts to tune")
    missing_alerts: list[str] = Field(description="Alerts to add")
    overall_health: str = Field(description="Alert health assessment")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Alert Tuner",
        instructions=["Optimize alerting to reduce noise while maintaining coverage."],
        output_schema=AlertTuning, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Alert Tuner - Demo\n" + "=" * 60)
    response = agent.run(f"Tune alerts: {config.get('alerts', DEFAULT_CONFIG['alerts'])}")
    result = response.content
    if isinstance(result, AlertTuning):
        print(f"\n📊 {result.overall_health}")
        for a in result.noisy_alerts: print(f"  🔔 {a.alert_name}: {a.recommendation}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alerts", "-a", default=DEFAULT_CONFIG["alerts"])
    args = parser.parse_args()
    run_demo(get_agent(), {"alerts": args.alerts})

if __name__ == "__main__": main()
