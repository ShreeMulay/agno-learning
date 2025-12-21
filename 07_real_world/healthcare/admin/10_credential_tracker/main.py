"""
Example #110: Credential Tracker
Category: healthcare/admin
DESCRIPTION: Tracks provider credentials - licenses, certifications, privileges
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"provider_type": "physician"}

class Credential(BaseModel):
    credential_type: str = Field(description="License, certification, etc.")
    name: str = Field(description="Credential name")
    issuing_body: str = Field(description="Issuing organization")
    expiration: str = Field(description="Expiration date")
    status: str = Field(description="current, expiring_soon, expired")
    days_until_expiry: int = Field(description="Days until expiration")

class CredentialReport(BaseModel):
    provider_name: str = Field(description="Provider name")
    provider_type: str = Field(description="Physician, NP, PA, etc.")
    npi: str = Field(description="NPI number")
    credentials: list[Credential] = Field(description="All credentials")
    expired_count: int = Field(description="Expired credentials")
    expiring_soon: int = Field(description="Expiring in 90 days")
    action_items: list[str] = Field(description="Required actions")
    privileging_status: str = Field(description="Active, provisional, suspended")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Credential Tracker",
        instructions=[
            "Track all provider credentials and certifications",
            "Alert on expiring and expired credentials",
            "Ensure compliance with privileging requirements",
            "Generate renewal action items with timelines",
            "Maintain credentialing documentation"
        ],
        output_schema=CredentialReport, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Credential Tracker - Demo\n" + "=" * 60)
    query = f"""Track credentials for {config['provider_type']}:
Provider: Dr. Jennifer Adams, MD
NPI: 1234567890
Specialty: Internal Medicine

Current credentials:
- State Medical License (CA): Expires 06/30/2025
- DEA Registration: Expires 03/31/2025
- Board Certification (ABIM): Expires 12/31/2027
- BLS: Expires 02/15/2025
- ACLS: Expired 11/30/2024
- Hospital Privileges (General): Expires 12/31/2025
- Malpractice Insurance: Current through 2025"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CredentialReport):
        print(f"\nProvider: {result.provider_name}")
        print(f"Type: {result.provider_type} | NPI: {result.npi}")
        print(f"Privileging Status: {result.privileging_status}")
        print(f"\n⚠️ Expired: {result.expired_count} | Expiring Soon: {result.expiring_soon}")
        print(f"\nCredentials ({len(result.credentials)}):")
        for c in result.credentials:
            status_icon = "✅" if c.status == "current" else "⚠️" if c.status == "expiring_soon" else "❌"
            print(f"  {status_icon} {c.name}: {c.expiration} ({c.days_until_expiry} days)")
        print(f"\nAction Items:")
        for action in result.action_items[:3]:
            print(f"  → {action}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider-type", "-p", default=DEFAULT_CONFIG["provider_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"provider_type": args.provider_type})

if __name__ == "__main__": main()
