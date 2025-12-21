"""
Example #062: Bug Detector
Category: engineering/code

DESCRIPTION:
Analyzes code to detect potential bugs, edge cases, and runtime errors.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
def divide_numbers(a, b):
    return a / b

def get_first_item(items):
    return items[0]

def parse_config(config_str):
    import json
    return json.loads(config_str)

def read_file(path):
    with open(path) as f:
        return f.read()
''',
}

class Bug(BaseModel):
    location: str = Field(description="Function/line where bug exists")
    bug_type: str = Field(description="null/index/type/resource/logic/race")
    description: str = Field(description="What could go wrong")
    trigger: str = Field(description="Input that would trigger this bug")
    fix: str = Field(description="How to fix it")
    severity: str = Field(description="critical/high/medium/low")

class BugReport(BaseModel):
    bugs_found: list[Bug] = Field(description="Bugs detected")
    risk_score: int = Field(ge=0, le=100, description="Overall risk")
    recommendations: list[str] = Field(description="General recommendations")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Bug Detector",
        instructions=[
            "You are a bug-hunting specialist analyzing code for potential issues.",
            "Look for: null/undefined access, index out of bounds, type errors,",
            "resource leaks, unhandled exceptions, race conditions, logic errors.",
            "Provide specific inputs that would trigger each bug.",
        ],
        output_schema=BugReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Bug Detector - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Find bugs in:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, BugReport):
        print(f"\n🐛 Bugs Found: {len(result.bugs_found)} | Risk: {result.risk_score}/100")
        for b in result.bugs_found:
            sev = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
            print(f"\n  {sev.get(b.severity, '?')} {b.location} [{b.bug_type}]")
            print(f"     {b.description}")
            print(f"     Trigger: {b.trigger}")
            print(f"     Fix: {b.fix}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Bug Detector")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
