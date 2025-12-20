"""
Example #032: Expense Categorizer
Category: business/finance

DESCRIPTION:
Categorizes expenses from receipts, validates against policy, and flags
potential compliance issues. Supports multi-currency and various expense types.

PATTERNS:
- Tools (calculations)
- Structured Output (ExpenseReport)
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "expense_data": """
    Expense Report - John Smith (Sales)
    Trip: Client Meeting - Chicago
    Dates: Dec 10-12, 2024
    
    Expenses:
    1. Flight: NYC → Chicago roundtrip - $485
    2. Hotel: Marriott Downtown (2 nights) - $378
    3. Uber to airport - $45
    4. Client dinner (4 people) - $287
    5. Coffee meeting - $18
    6. Uber to client office - $22
    7. Office supplies (emergency) - $35
    8. Personal items from hotel gift shop - $52
    """,
    "policy": "Travel: Economy flights, hotels under $200/night, meals under $100/person",
}


class ExpenseItem(BaseModel):
    description: str = Field(description="Expense description")
    amount: float = Field(description="Amount")
    category: str = Field(description="Category (travel/meals/lodging/transport/supplies/other)")
    subcategory: str = Field(description="Subcategory")
    policy_compliant: bool = Field(description="Meets policy")
    flag_reason: Optional[str] = Field(default=None, description="Why flagged")
    reimbursable: bool = Field(description="Should be reimbursed")


class ExpenseReport(BaseModel):
    employee: str = Field(description="Employee name")
    department: str = Field(description="Department")
    trip_purpose: str = Field(description="Business purpose")
    expenses: list[ExpenseItem] = Field(description="Categorized expenses")
    total_amount: float = Field(description="Total expenses")
    reimbursable_amount: float = Field(description="Approved for reimbursement")
    non_reimbursable_amount: float = Field(description="Not approved")
    policy_violations: list[str] = Field(description="Policy violations")
    approval_recommendation: str = Field(description="approve/partial/reject")
    notes: str = Field(description="Additional notes")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Expense Categorizer",
        instructions=[
            "You are an expense management specialist.",
            "Categorize expenses and check policy compliance.",
            "",
            f"Company Policy: {cfg['policy']}",
            "",
            "Categories:",
            "- travel: Flights, trains, car rentals",
            "- lodging: Hotels, Airbnb",
            "- meals: Business meals, client entertainment",
            "- transport: Uber, taxi, parking",
            "- supplies: Office supplies, equipment",
            "- other: Miscellaneous",
            "",
            "Reimbursement Rules:",
            "- Personal items: NOT reimbursable",
            "- Over-policy amounts: Flag for review",
            "- Missing receipts: Flag required",
        ],
        output_schema=ExpenseReport,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Expense Categorizer - Demo")
    print("=" * 60)
    
    data = config.get("expense_data", DEFAULT_CONFIG["expense_data"])
    response = agent.run(f"Categorize and validate:\n\n{data}")
    result = response.content
    
    if isinstance(result, ExpenseReport):
        print(f"\n👤 {result.employee} ({result.department})")
        print(f"📌 Purpose: {result.trip_purpose}")
        
        print(f"\n📋 Expenses:")
        for exp in result.expenses:
            icon = "✅" if exp.policy_compliant else "⚠️"
            reimb = "💰" if exp.reimbursable else "❌"
            print(f"  {icon}{reimb} {exp.description}: ${exp.amount:.2f} [{exp.category}]")
            if exp.flag_reason:
                print(f"      Flag: {exp.flag_reason}")
        
        print(f"\n💵 Summary:")
        print(f"  Total: ${result.total_amount:,.2f}")
        print(f"  Reimbursable: ${result.reimbursable_amount:,.2f}")
        print(f"  Non-reimbursable: ${result.non_reimbursable_amount:,.2f}")
        
        if result.policy_violations:
            print(f"\n⚠️ Policy Violations:")
            for v in result.policy_violations:
                print(f"  • {v}")
        
        print(f"\n📝 Recommendation: {result.approval_recommendation.upper()}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="Expense Categorizer")
    parser.add_argument("--data", "-d", type=str, default=DEFAULT_CONFIG["expense_data"])
    args = parser.parse_args()
    agent = get_agent(config={"expense_data": args.data})
    run_demo(agent, {"expense_data": args.data})


if __name__ == "__main__":
    main()
