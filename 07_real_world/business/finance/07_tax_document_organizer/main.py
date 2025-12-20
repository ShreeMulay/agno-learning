"""
Example #037: Tax Document Organizer
Category: business/finance

DESCRIPTION:
Categorizes and organizes tax-related documents, extracts key information,
and prepares for filing. Identifies missing documents.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "documents": """
    Tax Documents Received:
    1. W-2 from Primary Employer - $85,000 wages
    2. 1099-INT from Bank - $342 interest
    3. 1099-DIV from Brokerage - $1,250 dividends
    4. Mortgage Interest Statement (1098) - $12,400
    5. Property Tax Receipt - $4,200
    6. Charitable Donation Receipts - $2,500 total
    7. HSA Contributions Statement - $3,650
    
    Missing: 1099-B for stock sales (expected)
    """,
}

class TaxDocument(BaseModel):
    form_type: str = Field(description="IRS form type")
    source: str = Field(description="Document source")
    amount: float = Field(description="Key amount")
    category: str = Field(description="income/deduction/credit")
    schedule: str = Field(description="Tax schedule it feeds")

class TaxOrganization(BaseModel):
    tax_year: str = Field(description="Tax year")
    documents_received: list[TaxDocument] = Field(description="Organized docs")
    total_income: float = Field(description="Total income")
    total_deductions: float = Field(description="Total deductions")
    missing_documents: list[str] = Field(description="Missing items")
    filing_readiness: str = Field(description="ready/incomplete")
    next_steps: list[str] = Field(description="Required actions")
    itemize_recommendation: str = Field(description="Itemize vs standard")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Tax Document Organizer",
        instructions=[
            "You are a tax preparation specialist.",
            "Organize documents by category and schedule.",
            "Identify missing documents.",
            "Recommend itemizing vs standard deduction.",
        ],
        output_schema=TaxOrganization,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Tax Document Organizer - Demo")
    print("=" * 60)
    data = config.get("documents", DEFAULT_CONFIG["documents"])
    response = agent.run(f"Organize tax documents:\n\n{data}")
    result = response.content
    if isinstance(result, TaxOrganization):
        print(f"\n📋 Tax Year: {result.tax_year}")
        print(f"Status: {result.filing_readiness.upper()}")
        print(f"\n💵 Income: ${result.total_income:,.2f}")
        print(f"📉 Deductions: ${result.total_deductions:,.2f}")
        print(f"\n📄 Documents:")
        for doc in result.documents_received:
            print(f"  • {doc.form_type}: ${doc.amount:,.2f} [{doc.category}]")
        if result.missing_documents:
            print(f"\n⚠️ Missing: {', '.join(result.missing_documents)}")
        print(f"\n💡 Recommendation: {result.itemize_recommendation}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Tax Document Organizer")
    parser.add_argument("--docs", "-d", type=str, default=DEFAULT_CONFIG["documents"])
    args = parser.parse_args()
    agent = get_agent()
    run_demo(agent, {"documents": args.docs})

if __name__ == "__main__":
    main()
