"""
Example #074: Infrastructure Auditor
Category: engineering/devops
DESCRIPTION: Audits infrastructure for security, compliance, and best practices.
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"infra": "3 EC2 instances (public IPs, SSH port 22 open), S3 bucket (public read), RDS (no encryption)"}

class AuditFinding(BaseModel):
    resource: str = Field(description="Resource name")
    issue: str = Field(description="Security issue")
    severity: str = Field(description="critical/high/medium/low")
    remediation: str = Field(description="How to fix")

class InfraAudit(BaseModel):
    findings: list[AuditFinding] = Field(description="Audit findings")
    compliance_score: int = Field(ge=0, le=100)
    priority_fixes: list[str] = Field(description="Top fixes")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Infrastructure Auditor",
        instructions=["Audit infrastructure for security issues and compliance."],
        output_schema=InfraAudit, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Infrastructure Auditor - Demo\n" + "=" * 60)
    response = agent.run(f"Audit: {config.get('infra', DEFAULT_CONFIG['infra'])}")
    result = response.content
    if isinstance(result, InfraAudit):
        print(f"\n📊 Compliance: {result.compliance_score}%")
        for f in result.findings:
            print(f"  🔴 {f.resource}: {f.issue}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infra", "-i", default=DEFAULT_CONFIG["infra"])
    args = parser.parse_args()
    run_demo(get_agent(), {"infra": args.infra})

if __name__ == "__main__": main()
