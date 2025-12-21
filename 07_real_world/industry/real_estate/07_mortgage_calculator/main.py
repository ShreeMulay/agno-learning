"""
Example #137: Mortgage Calculator Agent
Category: industry/real_estate
DESCRIPTION: Calculates mortgage payments and compares loan options
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"home_price": 400000, "down_payment_pct": 20, "credit_score": 750}

class LoanOption(BaseModel):
    loan_type: str = Field(description="Type of loan (conventional, FHA, VA, etc.)")
    interest_rate: float = Field(description="Annual interest rate percentage")
    term_years: int = Field(description="Loan term in years")
    monthly_payment: int = Field(description="Monthly P&I payment")
    total_interest: int = Field(description="Total interest over loan life")
    pmi_monthly: int = Field(description="Monthly PMI if applicable")

class MortgageAnalysis(BaseModel):
    home_price: int = Field(description="Home purchase price")
    down_payment: int = Field(description="Down payment amount")
    loan_amount: int = Field(description="Total loan amount")
    loan_options: list[LoanOption] = Field(description="Available loan options")
    recommended_option: str = Field(description="Recommended loan type")
    monthly_costs: dict = Field(description="Breakdown of monthly costs")
    affordability_assessment: str = Field(description="Affordability analysis")
    tips: list[str] = Field(description="Money-saving tips")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Mortgage Calculator",
        instructions=[
            "You are an expert mortgage advisor and financial analyst.",
            f"Calculate options for a ${cfg['home_price']:,} home",
            f"Assume credit score of {cfg['credit_score']}",
            "Compare different loan types and terms",
            "Include taxes, insurance, and PMI estimates",
            "Provide realistic current market rates",
        ],
        output_schema=MortgageAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Mortgage Calculator Agent - Demo")
    print("=" * 60)
    down_payment = int(config['home_price'] * config['down_payment_pct'] / 100)
    query = f"""Calculate mortgage options:
- Home Price: ${config['home_price']:,}
- Down Payment: {config['down_payment_pct']}% (${down_payment:,})
- Credit Score: {config['credit_score']}

Compare loan options and provide recommendations."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, MortgageAnalysis):
        print(f"\n🏠 Home Price: ${result.home_price:,}")
        print(f"💵 Down Payment: ${result.down_payment:,}")
        print(f"📊 Loan Amount: ${result.loan_amount:,}")
        print(f"\n💳 Loan Options:")
        for opt in result.loan_options[:3]:
            print(f"  {opt.loan_type} ({opt.term_years}yr @ {opt.interest_rate}%)")
            print(f"    Monthly: ${opt.monthly_payment:,} | Total Interest: ${opt.total_interest:,}")
        print(f"\n⭐ Recommended: {result.recommended_option}")
        print(f"📋 Assessment: {result.affordability_assessment}")

def main():
    parser = argparse.ArgumentParser(description="Mortgage Calculator Agent")
    parser.add_argument("--price", "-p", type=int, default=DEFAULT_CONFIG["home_price"])
    parser.add_argument("--down", "-d", type=int, default=DEFAULT_CONFIG["down_payment_pct"])
    parser.add_argument("--credit", "-c", type=int, default=DEFAULT_CONFIG["credit_score"])
    args = parser.parse_args()
    config = {"home_price": args.price, "down_payment_pct": args.down, "credit_score": args.credit}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
