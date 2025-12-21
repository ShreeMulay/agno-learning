"""
Example #061: Code Reviewer
Category: engineering/code

DESCRIPTION:
Reviews code for quality, best practices, potential bugs, and suggests improvements.

PATTERNS:
- Knowledge (coding standards)
- Structured Output (CodeReview)
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
def get_user_data(user_id):
    import requests
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    data = resp.json()
    return data

def process_users():
    users = []
    for i in range(1, 100):
        try:
            user = get_user_data(i)
            if user['status'] == 'active':
                users.append(user)
        except:
            pass
    return users
''',
    "language": "python",
}

class CodeIssue(BaseModel):
    line: Optional[int] = Field(default=None, description="Line number")
    severity: str = Field(description="critical/warning/suggestion")
    category: str = Field(description="bug/security/performance/style/maintainability")
    issue: str = Field(description="What's wrong")
    fix: str = Field(description="How to fix it")

class CodeReview(BaseModel):
    overall_quality: str = Field(description="poor/fair/good/excellent")
    score: int = Field(ge=0, le=100, description="Quality score")
    issues: list[CodeIssue] = Field(description="Issues found")
    positives: list[str] = Field(description="Good practices observed")
    refactored_code: str = Field(description="Improved version")
    summary: str = Field(description="Brief summary")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Code Reviewer",
        instructions=[
            f"You are a senior {cfg['language']} developer reviewing code.",
            "Identify bugs, security issues, performance problems, and style issues.",
            "Provide constructive feedback with specific fixes.",
            "Include a refactored version demonstrating best practices.",
        ],
        output_schema=CodeReview,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Code Reviewer - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Review this code:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, CodeReview):
        print(f"\n📊 Quality: {result.overall_quality.upper()} ({result.score}/100)")
        print(f"\n🔍 Issues ({len(result.issues)}):")
        for i in result.issues:
            sev = {"critical": "🔴", "warning": "🟡", "suggestion": "🟢"}
            print(f"  {sev.get(i.severity, '?')} Line {i.line or '?'}: {i.issue}")
            print(f"     Fix: {i.fix}")
        print(f"\n✅ Positives:")
        for p in result.positives:
            print(f"  • {p}")
        print(f"\n📝 {result.summary}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Code Reviewer")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
