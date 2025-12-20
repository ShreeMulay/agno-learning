"""
Example #051: Contract Reviewer
Category: business/legal

DESCRIPTION:
Analyzes contracts to identify key clauses, flag risks,
and highlight terms that need negotiation.

PATTERNS:
- Knowledge (contract law basics)
- Structured Output (ContractReview)
- Reasoning (risk assessment)

ARGUMENTS:
- contract_text (str): Contract to review
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "contract_text": """
    MASTER SERVICES AGREEMENT
    
    This Agreement is entered into as of December 1, 2024 between:
    TechVendor Inc. ("Provider") and Acme Corp ("Client")
    
    1. SERVICES
    Provider shall deliver software development services as described in 
    Statement of Work documents. Client shall pay within 45 days of invoice.
    
    2. INTELLECTUAL PROPERTY
    All work product created shall be owned exclusively by Provider. Client
    receives a non-exclusive, non-transferable license to use the work product.
    Provider retains rights to reuse code, methodologies, and tools.
    
    3. CONFIDENTIALITY
    Both parties agree to protect confidential information for 5 years.
    Confidential information excludes publicly available information.
    
    4. LIABILITY
    Provider's total liability shall not exceed fees paid in the prior 12 months.
    IN NO EVENT SHALL PROVIDER BE LIABLE FOR INDIRECT, CONSEQUENTIAL, OR 
    PUNITIVE DAMAGES.
    
    5. INDEMNIFICATION
    Client shall indemnify Provider against all claims arising from Client's
    use of the deliverables. Provider offers no indemnification to Client.
    
    6. TERMINATION
    Either party may terminate with 30 days written notice. Upon termination,
    Client shall pay for all work completed. No refunds for prepaid fees.
    
    7. GOVERNING LAW
    This Agreement shall be governed by the laws of Delaware. Any disputes
    shall be resolved through binding arbitration in Wilmington, DE.
    
    8. AUTO-RENEWAL
    This Agreement automatically renews for successive 1-year terms unless
    cancelled 90 days before expiration.
    """,
}


class ContractClause(BaseModel):
    clause_name: str = Field(description="Name of the clause")
    summary: str = Field(description="What the clause says")
    risk_level: str = Field(description="low/medium/high/critical")
    risk_explanation: str = Field(description="Why this is risky")
    negotiation_suggestion: Optional[str] = Field(default=None, description="Suggested changes")


class ContractReview(BaseModel):
    contract_type: str = Field(description="Type of contract")
    parties: list[str] = Field(description="Parties involved")
    effective_date: str = Field(description="Contract start date")
    key_terms: list[str] = Field(description="Most important terms")
    clauses_reviewed: list[ContractClause] = Field(description="Clause-by-clause analysis")
    red_flags: list[str] = Field(description="Critical issues")
    missing_clauses: list[str] = Field(description="Standard clauses not present")
    overall_risk_score: int = Field(ge=1, le=10, description="1=low, 10=high")
    recommendation: str = Field(description="sign/negotiate/reject")
    executive_summary: str = Field(description="Summary for decision makers")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Contract Reviewer",
        instructions=[
            "You are an experienced contract attorney reviewing agreements.",
            "Identify risks and suggest improvements for the client's benefit.",
            "",
            "Key Areas to Review:",
            "- IP ownership (should client own work product?)",
            "- Liability caps (are they reasonable?)",
            "- Indemnification (is it mutual?)",
            "- Termination rights (flexibility?)",
            "- Payment terms (reasonable?)",
            "- Auto-renewal traps",
            "- Venue and governing law",
            "",
            "Provide actionable recommendations.",
            "Highlight anything unusual or one-sided.",
        ],
        output_schema=ContractReview,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Contract Reviewer - Demo")
    print("=" * 60)
    
    contract = config.get("contract_text", DEFAULT_CONFIG["contract_text"])
    
    response = agent.run(f"Review this contract:\n\n{contract}")
    result = response.content
    
    if isinstance(result, ContractReview):
        print(f"\n📄 {result.contract_type}")
        print(f"Parties: {', '.join(result.parties)}")
        print(f"Effective: {result.effective_date}")
        
        print(f"\n📋 Key Terms:")
        for t in result.key_terms:
            print(f"   • {t}")
        
        print(f"\n🔍 Clause Analysis:")
        for c in result.clauses_reviewed:
            risk_icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
            print(f"\n   {risk_icon.get(c.risk_level, '⚪')} {c.clause_name} [{c.risk_level}]")
            print(f"   {c.summary}")
            if c.risk_level in ["high", "critical"]:
                print(f"   ⚠️ {c.risk_explanation}")
            if c.negotiation_suggestion:
                print(f"   💡 Suggest: {c.negotiation_suggestion}")
        
        if result.red_flags:
            print(f"\n🚨 Red Flags:")
            for f in result.red_flags:
                print(f"   • {f}")
        
        if result.missing_clauses:
            print(f"\n❓ Missing Standard Clauses:")
            for m in result.missing_clauses:
                print(f"   • {m}")
        
        rec_icon = {"sign": "✅", "negotiate": "🔄", "reject": "❌"}
        print(f"\n{rec_icon.get(result.recommendation, '?')} Recommendation: {result.recommendation.upper()}")
        print(f"📊 Risk Score: {result.overall_risk_score}/10")
        print(f"\n📝 Summary: {result.executive_summary}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Contract Reviewer")
    parser.add_argument("--contract", "-c", type=str, default=DEFAULT_CONFIG["contract_text"])
    args = parser.parse_args()
    agent = get_agent(config={"contract_text": args.contract})
    run_demo(agent, {"contract_text": args.contract})


if __name__ == "__main__":
    main()
