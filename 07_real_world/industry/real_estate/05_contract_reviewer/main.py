"""
Example #135: Contract Reviewer Agent
Category: industry/real_estate
DESCRIPTION: Reviews real estate contracts and identifies issues
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"contract_type": "purchase_agreement", "party": "buyer"}

class ContractIssue(BaseModel):
    section: str = Field(description="Contract section with issue")
    severity: str = Field(description="high/medium/low severity")
    issue: str = Field(description="Description of the issue")
    recommendation: str = Field(description="Suggested action or amendment")

class ContractReview(BaseModel):
    contract_summary: str = Field(description="Brief summary of contract terms")
    key_terms: list[str] = Field(description="Important terms to note")
    issues_found: list[ContractIssue] = Field(description="Issues identified")
    missing_clauses: list[str] = Field(description="Recommended missing clauses")
    negotiation_points: list[str] = Field(description="Suggested negotiation items")
    overall_assessment: str = Field(description="Overall contract assessment")
    proceed_recommendation: str = Field(description="Proceed/revise/reject recommendation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Contract Reviewer",
        instructions=[
            "You are an expert real estate contract analyst.",
            f"Review contracts from the {cfg['party']}'s perspective",
            f"Focus on {cfg['contract_type']} specific terms and risks",
            "Identify unfavorable terms, missing protections, and legal issues",
            "Suggest specific amendments and negotiation strategies",
            "Note: This is not legal advice - recommend attorney review for complex issues",
        ],
        output_schema=ContractReview,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Contract Reviewer Agent - Demo")
    print("=" * 60)
    sample_contract = """Purchase Agreement for 123 Main St. Price: $450,000.
    Earnest money: $5,000. Closing: 30 days. Financing contingency: 21 days.
    Inspection contingency: 10 days. Property sold AS-IS. Seller pays 2% closing costs.
    No home warranty included. Possession at closing."""
    query = f"""Review this {config['contract_type']} from the {config['party']}'s perspective:

{sample_contract}

Identify issues and provide recommendations."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ContractReview):
        print(f"\n📋 Summary: {result.contract_summary}")
        print(f"\n⚠️ Issues Found ({len(result.issues_found)}):")
        for issue in result.issues_found[:3]:
            print(f"  [{issue.severity.upper()}] {issue.section}: {issue.issue}")
        print(f"\n📝 Missing Clauses: {', '.join(result.missing_clauses[:3])}")
        print(f"\n🎯 Assessment: {result.overall_assessment}")
        print(f"\n✅ Recommendation: {result.proceed_recommendation}")

def main():
    parser = argparse.ArgumentParser(description="Contract Reviewer Agent")
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["contract_type"])
    parser.add_argument("--party", "-p", default=DEFAULT_CONFIG["party"], choices=["buyer", "seller"])
    args = parser.parse_args()
    config = {"contract_type": args.type, "party": args.party}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
