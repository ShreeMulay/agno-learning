"""
Example #072: Log Analyzer
Category: engineering/devops
DESCRIPTION: Analyzes logs to identify patterns, errors, and anomalies.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"logs": "2024-12-20 10:15:32 ERROR [api] Connection refused to db-primary\n2024-12-20 10:15:33 WARN [api] Retrying connection\n2024-12-20 10:15:35 ERROR [api] Max retries exceeded"}

class LogAnalysis(BaseModel):
    error_count: int = Field(description="Number of errors")
    warning_count: int = Field(description="Number of warnings")
    patterns: list[str] = Field(description="Identified patterns")
    root_cause: str = Field(description="Likely root cause")
    recommendations: list[str] = Field(description="Actions to take")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Log Analyzer",
        instructions=["Analyze logs for errors, patterns, and root causes."],
        output_schema=LogAnalysis, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Log Analyzer - Demo\n" + "=" * 60)
    response = agent.run(f"Analyze:\n{config.get('logs', DEFAULT_CONFIG['logs'])}")
    result = response.content
    if isinstance(result, LogAnalysis):
        print(f"\n📊 Errors: {result.error_count} | Warnings: {result.warning_count}")
        print(f"🔍 Root cause: {result.root_cause}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", "-l", default=DEFAULT_CONFIG["logs"])
    args = parser.parse_args()
    run_demo(get_agent(), {"logs": args.logs})

if __name__ == "__main__": main()
