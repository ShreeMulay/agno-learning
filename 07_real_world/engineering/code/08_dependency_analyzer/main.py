"""
Example #068: Dependency Analyzer
Category: engineering/code

DESCRIPTION:
Analyzes project dependencies for security, updates, and conflicts.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "dependencies": """
    {
      "dependencies": {
        "express": "^4.17.1",
        "lodash": "4.17.15",
        "moment": "2.29.1",
        "axios": "0.21.1",
        "jsonwebtoken": "8.5.1"
      },
      "devDependencies": {
        "jest": "^26.6.3",
        "eslint": "^7.20.0"
      }
    }
    """,
}

class Dependency(BaseModel):
    name: str = Field(description="Package name")
    current: str = Field(description="Current version")
    latest: str = Field(description="Latest version")
    security_issues: list[str] = Field(description="Known vulnerabilities")
    recommendation: str = Field(description="update/replace/keep")
    notes: str = Field(description="Additional notes")

class DependencyReport(BaseModel):
    total_deps: int = Field(description="Total dependencies")
    outdated: int = Field(description="Outdated count")
    vulnerable: int = Field(description="With security issues")
    dependencies: list[Dependency] = Field(description="Dependency analysis")
    update_commands: list[str] = Field(description="Commands to update")
    risk_assessment: str = Field(description="Overall risk level")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Dependency Analyzer",
        instructions=[
            "You are a security-focused dependency analyst.",
            "Check for outdated packages, known vulnerabilities,",
            "deprecated packages, and suggest replacements.",
        ],
        output_schema=DependencyReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Dependency Analyzer - Demo")
    print("=" * 60)
    deps = config.get("dependencies", DEFAULT_CONFIG["dependencies"])
    response = agent.run(f"Analyze:\n{deps}")
    result = response.content
    if isinstance(result, DependencyReport):
        print(f"\n📦 Total: {result.total_deps} | Outdated: {result.outdated} | Vulnerable: {result.vulnerable}")
        print(f"⚠️ Risk: {result.risk_assessment}")
        for d in result.dependencies[:5]:
            icon = {"update": "🔄", "replace": "❌", "keep": "✅"}
            print(f"\n  {icon.get(d.recommendation, '?')} {d.name}: {d.current} → {d.latest}")
            if d.security_issues:
                print(f"     🚨 {', '.join(d.security_issues)}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Dependency Analyzer")
    parser.add_argument("--deps", "-d", type=str, default=DEFAULT_CONFIG["dependencies"])
    args = parser.parse_args()
    agent = get_agent(config={"dependencies": args.deps})
    run_demo(agent, {"dependencies": args.deps})

if __name__ == "__main__":
    main()
