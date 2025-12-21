"""
Example #069: Security Scanner
Category: engineering/code

DESCRIPTION:
Scans code for security vulnerabilities and suggests fixes.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('users.db')
    cursor = conn.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return str(cursor.fetchone())

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f'/uploads/{file.filename}')
    return 'OK'

@app.route('/run')
def run_cmd():
    cmd = request.args.get('cmd')
    return os.popen(cmd).read()
''',
}

class Vulnerability(BaseModel):
    line: int = Field(description="Line number")
    vuln_type: str = Field(description="CWE type")
    severity: str = Field(description="critical/high/medium/low")
    description: str = Field(description="What's vulnerable")
    exploit: str = Field(description="How it could be exploited")
    fix: str = Field(description="How to fix it")
    fixed_code: str = Field(description="Secure version")

class SecurityReport(BaseModel):
    vulnerabilities: list[Vulnerability] = Field(description="Found vulnerabilities")
    security_score: int = Field(ge=0, le=100, description="Security score")
    critical_count: int = Field(description="Critical issues")
    recommendations: list[str] = Field(description="General recommendations")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Security Scanner",
        instructions=[
            "You are a security researcher scanning for vulnerabilities.",
            "Look for: SQL injection, XSS, command injection, path traversal,",
            "insecure deserialization, hardcoded secrets, SSRF, etc.",
            "Reference CWE IDs when applicable.",
        ],
        output_schema=SecurityReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Security Scanner - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Scan for vulnerabilities:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, SecurityReport):
        print(f"\n🔒 Security Score: {result.security_score}/100")
        print(f"🚨 Critical: {result.critical_count}")
        for v in result.vulnerabilities:
            sev = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
            print(f"\n  {sev.get(v.severity, '?')} Line {v.line}: {v.vuln_type}")
            print(f"     {v.description}")
            print(f"     Exploit: {v.exploit}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Security Scanner")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
