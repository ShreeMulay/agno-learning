"""
Example #080: Config Validator
Category: engineering/devops
DESCRIPTION: Validates configuration files for errors and best practices.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"config": "server:\n  port: 8080\n  timeout: 30\n  max_connections: 1000\ndatabase:\n  host: localhost\n  password: admin123"}

class ConfigIssue(BaseModel):
    location: str = Field(description="Config location")
    issue: str = Field(description="Problem found")
    severity: str = Field(description="error/warning/info")
    fix: str = Field(description="How to fix")

class ConfigValidation(BaseModel):
    valid: bool = Field(description="Is config valid?")
    issues: list[ConfigIssue] = Field(description="Issues found")
    security_concerns: list[str] = Field(description="Security issues")
    recommendations: list[str] = Field(description="Best practices")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Config Validator",
        instructions=["Validate configuration files for errors and security issues."],
        output_schema=ConfigValidation, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Config Validator - Demo\n" + "=" * 60)
    response = agent.run(f"Validate:\n{config.get('config', DEFAULT_CONFIG['config'])}")
    result = response.content
    if isinstance(result, ConfigValidation):
        print(f"\n{'✅' if result.valid else '❌'} Valid: {result.valid}")
        for i in result.issues: print(f"  ⚠️ {i.location}: {i.issue}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", default=DEFAULT_CONFIG["config"])
    args = parser.parse_args()
    run_demo(get_agent(), {"config": args.config})

if __name__ == "__main__": main()
