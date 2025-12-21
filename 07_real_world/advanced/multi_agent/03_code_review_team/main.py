"""
Example #213: Code Review Team Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Multiple specialized reviewers analyze code for different quality aspects
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"strictness": "standard"}

class ReviewFinding(BaseModel):
    category: str = Field(description="security, performance, style, logic")
    severity: str = Field(description="critical, major, minor, suggestion")
    location: str = Field(description="Where in the code")
    issue: str = Field(description="What the problem is")
    suggestion: str = Field(description="How to fix it")

class CodeReviewReport(BaseModel):
    overall_quality: str = Field(description="Overall assessment")
    score: int = Field(description="Quality score 1-10")
    findings: list[ReviewFinding] = Field(description="All review findings")
    critical_issues: int = Field(description="Count of critical issues")
    approval_status: str = Field(description="approved, needs_changes, rejected")
    summary: str = Field(description="Review summary")
    positive_notes: list[str] = Field(description="What's done well")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_security_reviewer(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Security Reviewer",
        instructions=[
            "You review code for security vulnerabilities.",
            "Check for injection, authentication, authorization issues.",
            "Identify sensitive data exposure risks.",
        ],
        markdown=True,
    )

def get_performance_reviewer(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Performance Reviewer",
        instructions=[
            "You review code for performance issues.",
            "Identify inefficient algorithms and memory leaks.",
            "Check for unnecessary operations and optimizations.",
        ],
        markdown=True,
    )

def get_lead_reviewer(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Lead Code Reviewer",
        instructions=[
            "You synthesize feedback from multiple code reviewers.",
            "Prioritize issues by severity and impact.",
            "Make final approval decisions.",
            "Provide constructive, actionable feedback.",
        ],
        output_schema=CodeReviewReport,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_lead_reviewer(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Code Review Team - Demo")
    print("=" * 60)
    
    code_sample = '''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = db.execute(query)
    users = []
    for row in result:
        users.append(row)
    return users[0] if users else None
'''
    
    security_agent = get_security_reviewer()
    perf_agent = get_performance_reviewer()
    lead = agent
    
    print(f"\n💻 Reviewing code sample...")
    
    sec_review = security_agent.run(f"Security review this code:\n{code_sample}")
    perf_review = perf_agent.run(f"Performance review this code:\n{code_sample}")
    
    synthesis_prompt = f"""
    Code to review:
    {code_sample}
    
    Security Review: {sec_review.content}
    Performance Review: {perf_review.content}
    
    Provide final code review report."""
    
    result = lead.run(synthesis_prompt)
    
    if isinstance(result.content, CodeReviewReport):
        r = result.content
        status_emoji = "✅" if r.approval_status == "approved" else "⚠️" if r.approval_status == "needs_changes" else "❌"
        print(f"\n{status_emoji} Status: {r.approval_status.upper()} (Score: {r.score}/10)")
        print(f"\n📋 Summary: {r.summary}")
        print(f"\n🔴 Critical Issues: {r.critical_issues}")
        print(f"\n📝 Findings:")
        for f in r.findings[:4]:
            sev_emoji = "🔴" if f.severity == "critical" else "🟡" if f.severity == "major" else "🔵"
            print(f"  {sev_emoji} [{f.category}] {f.issue}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strictness", "-s", default=DEFAULT_CONFIG["strictness"])
    args = parser.parse_args()
    run_demo(get_agent(), {"strictness": args.strictness})

if __name__ == "__main__": main()
