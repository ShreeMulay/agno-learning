"""
Example #036: Vendor Payment Scheduler
Category: business/finance

DESCRIPTION:
Optimizes vendor payment timing based on cash flow, discount opportunities,
and vendor relationships. Maximizes early payment discounts while managing liquidity.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "payment_data": """
    Pending Payments:
    1. Vendor A: $50,000 due Jan 15, 2/10 Net 30 (2% discount if paid in 10 days)
    2. Vendor B: $25,000 due Jan 20, Net 30
    3. Vendor C: $100,000 due Jan 10, 1/5 Net 30
    4. Vendor D: $15,000 due Jan 25, Net 45
    
    Cash Position: $120,000 available
    Expected Inflows: $80,000 by Jan 15, $50,000 by Jan 25
    """,
}

class PaymentRecommendation(BaseModel):
    vendor: str = Field(description="Vendor name")
    amount: float = Field(description="Payment amount")
    original_due: str = Field(description="Original due date")
    recommended_date: str = Field(description="Recommended pay date")
    discount_captured: float = Field(description="Discount amount saved")
    rationale: str = Field(description="Why this timing")

class PaymentSchedule(BaseModel):
    total_payable: float = Field(description="Total amount to pay")
    total_discounts: float = Field(description="Total discounts captured")
    net_payment: float = Field(description="Net amount after discounts")
    recommendations: list[PaymentRecommendation] = Field(description="Payment schedule")
    cash_flow_projection: dict = Field(description="Projected cash by date")
    risks: list[str] = Field(description="Cash flow risks")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Vendor Payment Scheduler",
        instructions=[
            "You are a treasury management specialist.",
            "Optimize payment timing for cash flow and discounts.",
            "Never recommend paying if it would cause cash shortage.",
            "Prioritize early payment discounts when beneficial.",
        ],
        output_schema=PaymentSchedule,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Vendor Payment Scheduler - Demo")
    print("=" * 60)
    data = config.get("payment_data", DEFAULT_CONFIG["payment_data"])
    response = agent.run(f"Optimize payment schedule:\n\n{data}")
    result = response.content
    if isinstance(result, PaymentSchedule):
        print(f"\n💰 Total Payable: ${result.total_payable:,.2f}")
        print(f"💵 Discounts: ${result.total_discounts:,.2f}")
        print(f"📊 Net Payment: ${result.net_payment:,.2f}")
        print(f"\n📅 Schedule:")
        for p in result.recommendations:
            print(f"  • {p.vendor}: ${p.amount:,.2f} on {p.recommended_date}")
            if p.discount_captured > 0:
                print(f"    💰 Discount: ${p.discount_captured:,.2f}")
        if result.risks:
            print(f"\n⚠️ Risks:")
            for r in result.risks:
                print(f"  • {r}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Vendor Payment Scheduler")
    parser.add_argument("--data", "-d", type=str, default=DEFAULT_CONFIG["payment_data"])
    args = parser.parse_args()
    agent = get_agent()
    run_demo(agent, {"payment_data": args.data})

if __name__ == "__main__":
    main()
