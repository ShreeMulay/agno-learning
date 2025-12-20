"""
Example #035: Audit Trail Documenter
Category: business/finance

DESCRIPTION:
Documents changes to financial records with proper audit trails.
Tracks who changed what, when, and why for compliance purposes.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "change_data": """
    Change Request:
    - Record: Invoice #INV-2024-0456
    - Field Changed: Total Amount
    - Old Value: $15,000
    - New Value: $14,250
    - Changed By: Sarah Johnson (Accounts Payable)
    - Timestamp: 2024-12-15 14:32:00 UTC
    - Reason: Customer discount applied per sales agreement SA-2024-089
    - Approver: Mike Chen (AP Manager)
    """,
}

class AuditEntry(BaseModel):
    record_id: str = Field(description="Record identifier")
    change_type: str = Field(description="create/update/delete")
    field_changed: str = Field(description="Field that was changed")
    old_value: str = Field(description="Previous value")
    new_value: str = Field(description="New value")
    changed_by: str = Field(description="User who made change")
    timestamp: str = Field(description="When change occurred")
    reason: str = Field(description="Business justification")
    approver: Optional[str] = Field(default=None, description="Who approved")
    compliance_flags: list[str] = Field(description="Compliance considerations")
    risk_level: str = Field(description="low/medium/high")
    documentation_complete: bool = Field(description="All required info present")
    missing_items: list[str] = Field(description="What's missing if any")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Audit Trail Documenter",
        instructions=[
            "You are a compliance and audit specialist.",
            "Document all changes with complete audit trails.",
            "Flag any compliance concerns.",
            "Ensure SOX and regulatory compliance.",
        ],
        output_schema=AuditEntry,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Audit Trail Documenter - Demo")
    print("=" * 60)
    data = config.get("change_data", DEFAULT_CONFIG["change_data"])
    response = agent.run(f"Document this change:\n\n{data}")
    result = response.content
    if isinstance(result, AuditEntry):
        print(f"\n📝 Record: {result.record_id}")
        print(f"Type: {result.change_type.upper()}")
        print(f"Field: {result.field_changed}")
        print(f"Change: {result.old_value} → {result.new_value}")
        print(f"By: {result.changed_by} @ {result.timestamp}")
        print(f"Reason: {result.reason}")
        print(f"Approved by: {result.approver or 'N/A'}")
        print(f"\n🔒 Risk: {result.risk_level.upper()}")
        print(f"Documentation: {'✅ Complete' if result.documentation_complete else '❌ Incomplete'}")
        if result.compliance_flags:
            print(f"⚠️ Flags: {', '.join(result.compliance_flags)}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Audit Trail Documenter")
    parser.add_argument("--data", "-d", type=str, default=DEFAULT_CONFIG["change_data"])
    args = parser.parse_args()
    agent = get_agent()
    run_demo(agent, {"change_data": args.data})

if __name__ == "__main__":
    main()
