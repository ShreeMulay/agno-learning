"""
Example #109: Compliance Auditor
Category: healthcare/admin
DESCRIPTION: Audits healthcare compliance - HIPAA, documentation, billing
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"audit_type": "HIPAA"}

class AuditFinding(BaseModel):
    area: str = Field(description="Compliance area")
    finding: str = Field(description="Issue identified")
    severity: str = Field(description="critical, high, medium, low")
    regulation: str = Field(description="Applicable regulation")
    recommendation: str = Field(description="Corrective action")

class ComplianceAudit(BaseModel):
    audit_type: str = Field(description="Type of audit")
    audit_date: str = Field(description="Audit date")
    scope: str = Field(description="Audit scope")
    findings: list[AuditFinding] = Field(description="Audit findings")
    compliance_score: float = Field(description="Overall compliance %")
    critical_issues: int = Field(description="Critical issue count")
    corrective_actions: list[str] = Field(description="Required actions")
    timeline: str = Field(description="Remediation timeline")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Compliance Auditor",
        instructions=[
            "Audit against applicable healthcare regulations",
            "Identify compliance gaps and violations",
            "Classify findings by severity and risk",
            "Recommend specific corrective actions",
            "Establish remediation timelines"
        ],
        output_schema=ComplianceAudit, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Compliance Auditor - Demo\n" + "=" * 60)
    query = f"""Conduct {config['audit_type']} audit:
Organization: Downtown Medical Group
Audit areas reviewed:
- Access controls: 15 users with system access, 3 terminated
- PHI handling: 500 patient records sampled
- Training: Last HIPAA training 18 months ago
- Incident response: No documented policy found
- BAAs: 12 vendors, 10 with current agreements
- Encryption: EHR encrypted, emails not encrypted
- Physical security: Badge access, visitor logs incomplete"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ComplianceAudit):
        print(f"\nAudit Type: {result.audit_type}")
        print(f"Date: {result.audit_date}")
        print(f"Compliance Score: {result.compliance_score:.1f}%")
        print(f"Critical Issues: {result.critical_issues}")
        print(f"\nFindings ({len(result.findings)}):")
        for f in result.findings[:4]:
            severity_icon = "🔴" if f.severity == "critical" else "🟠" if f.severity == "high" else "🟡"
            print(f"  {severity_icon} [{f.severity}] {f.area}: {f.finding}")
        print(f"\nRemediation Timeline: {result.timeline}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-type", "-a", default=DEFAULT_CONFIG["audit_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"audit_type": args.audit_type})

if __name__ == "__main__": main()
