"""
Example #196: Tax Estimator Agent
Category: personal/finance
DESCRIPTION: Estimates tax liability and suggests deductions and planning strategies
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"filing_status": "single"}

class Deduction(BaseModel):
    category: str = Field(description="Deduction category")
    amount: float = Field(description="Estimated deduction amount")
    documentation_needed: str = Field(description="Required documentation")

class TaxEstimate(BaseModel):
    gross_income: float = Field(description="Total gross income")
    adjusted_gross_income: float = Field(description="AGI after adjustments")
    total_deductions: float = Field(description="Total deductions")
    taxable_income: float = Field(description="Income subject to tax")
    estimated_tax: float = Field(description="Estimated tax liability")
    effective_tax_rate: float = Field(description="Effective tax rate percentage")
    deductions: list[Deduction] = Field(description="Available deductions")
    tax_saving_strategies: list[str] = Field(description="Ways to reduce tax")
    quarterly_estimate: float = Field(description="Quarterly payment if needed")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Tax Estimator",
        instructions=[
            f"You estimate taxes for {cfg['filing_status']} filing status.",
            "Identify potential deductions and credits.",
            "Use current tax brackets and standard deduction.",
            "Suggest tax planning strategies.",
            "This is for estimation only - recommend consulting a tax professional.",
        ],
        output_schema=TaxEstimate,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Tax Estimator - Demo")
    print("=" * 60)
    query = """Estimate my taxes:
    Filing status: Single
    W-2 Income: $85,000
    Freelance income: $15,000
    401k contributions: $10,000
    HSA contributions: $3,000
    Student loan interest: $1,200
    Charitable donations: $2,000
    Home office (freelance): Yes"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, TaxEstimate):
        print(f"\n💵 Gross Income: ${result.gross_income:,.0f}")
        print(f"📉 AGI: ${result.adjusted_gross_income:,.0f}")
        print(f"✂️ Deductions: ${result.total_deductions:,.0f}")
        print(f"📊 Taxable Income: ${result.taxable_income:,.0f}")
        print(f"\n🏛️ Estimated Tax: ${result.estimated_tax:,.0f}")
        print(f"📈 Effective Rate: {result.effective_tax_rate:.1f}%")
        print(f"\n💡 Tax Saving Tips:")
        for tip in result.tax_saving_strategies[:3]:
            print(f"  • {tip}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filing-status", "-f", default=DEFAULT_CONFIG["filing_status"])
    args = parser.parse_args()
    run_demo(get_agent(config={"filing_status": args.filing_status}), {"filing_status": args.filing_status})

if __name__ == "__main__": main()
