"""
Example #071: Incident Responder
Category: engineering/devops
DESCRIPTION: Analyzes incidents and guides response with runbooks.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"incident": "Database connection pool exhausted, API latency > 5s, error rate 40%"}

class IncidentResponse(BaseModel):
    severity: str = Field(description="P1/P2/P3/P4")
    summary: str = Field(description="Brief summary")
    root_cause_hypothesis: list[str] = Field(description="Likely causes")
    immediate_actions: list[str] = Field(description="Steps to take now")
    escalation_needed: bool = Field(description="Need to escalate?")
    communication_template: str = Field(description="Status update template")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Incident Responder",
        instructions=["You are an SRE expert handling production incidents.", "Prioritize by impact, suggest immediate mitigations."],
        output_schema=IncidentResponse, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Incident Responder - Demo\n" + "=" * 60)
    response = agent.run(f"Incident: {config.get('incident', DEFAULT_CONFIG['incident'])}")
    result = response.content
    if isinstance(result, IncidentResponse):
        print(f"\n🚨 Severity: {result.severity}\n📝 {result.summary}")
        for a in result.immediate_actions: print(f"  • {a}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--incident", "-i", default=DEFAULT_CONFIG["incident"])
    args = parser.parse_args()
    run_demo(get_agent(), {"incident": args.incident})

if __name__ == "__main__": main()
