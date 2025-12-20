"""
Example #048: PTO Balance Tracker
Category: business/hr

DESCRIPTION:
Tracks employee leave balances, processes time-off requests,
and provides availability forecasts for team planning.

PATTERNS:
- Structured Output (PTOStatus)
- Reasoning (balance calculations)

ARGUMENTS:
- employee_data (str): Employee leave data
- request (str): Time-off request to process
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "employee_data": """
    Employee: Jordan Lee
    Start Date: March 15, 2022 (2+ years)
    
    PTO Entitlement: 20 days/year (accrues 1.67 days/month)
    Sick Days: 10 days/year (no rollover)
    
    Current Balances (as of Dec 15, 2024):
    - PTO Available: 8.5 days
    - PTO Pending Requests: 3 days (Dec 23-25)
    - Sick Days Remaining: 4 days
    - Carryover from 2023: 2 days (expires Mar 31, 2025)
    
    Usage This Year:
    - PTO Used: 14.5 days
    - Sick Days Used: 6 days
    """,
    "request": "I'd like to take January 2-3, 2025 off for a long weekend after New Year's.",
}


class LeaveBalance(BaseModel):
    leave_type: str = Field(description="PTO/sick/carryover")
    available: float = Field(description="Days available")
    pending: float = Field(description="Days in pending requests")
    used_ytd: float = Field(description="Days used this year")
    expiring_soon: Optional[str] = Field(default=None, description="Expiration warning")


class PTOStatus(BaseModel):
    employee_name: str = Field(description="Employee name")
    request_summary: str = Field(description="What was requested")
    request_days: float = Field(description="Days requested")
    can_approve: bool = Field(description="Sufficient balance?")
    approval_recommendation: str = Field(description="approve/deny/partial")
    denial_reason: Optional[str] = Field(default=None, description="Why denied")
    balances_after: list[LeaveBalance] = Field(description="Balances if approved")
    upcoming_accrual: str = Field(description="When more PTO accrues")
    year_end_projection: str = Field(description="Projected year-end balance")
    suggestions: list[str] = Field(description="Recommendations")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    employee_data = cfg.get("employee_data", DEFAULT_CONFIG["employee_data"])
    
    return Agent(
        model=model or default_model(),
        name="PTO Balance Tracker",
        instructions=[
            "You are an HR leave management specialist.",
            "Process time-off requests and track balances accurately.",
            "",
            f"EMPLOYEE DATA:\n{employee_data}",
            "",
            "Rules:",
            "- Check sufficient balance before approving",
            "- PTO accrues monthly on the 1st",
            "- Carryover days should be used first",
            "- Flag if request leaves less than 2 days buffer",
            "- Consider blackout dates (year-end close, etc.)",
        ],
        output_schema=PTOStatus,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  PTO Balance Tracker - Demo")
    print("=" * 60)
    
    request = config.get("request", DEFAULT_CONFIG["request"])
    
    response = agent.run(f"Process this time-off request:\n{request}")
    result = response.content
    
    if isinstance(result, PTOStatus):
        print(f"\n👤 {result.employee_name}")
        print(f"📅 Request: {result.request_summary} ({result.request_days} days)")
        
        icon = "✅" if result.can_approve else "❌"
        print(f"\n{icon} Recommendation: {result.approval_recommendation.upper()}")
        if result.denial_reason:
            print(f"   Reason: {result.denial_reason}")
        
        print(f"\n💰 Balances After Approval:")
        for b in result.balances_after:
            exp = f" ⚠️ {b.expiring_soon}" if b.expiring_soon else ""
            print(f"   {b.leave_type}: {b.available} days available{exp}")
        
        print(f"\n📈 Next Accrual: {result.upcoming_accrual}")
        print(f"📊 Year-End Projection: {result.year_end_projection}")
        
        if result.suggestions:
            print(f"\n💡 Suggestions:")
            for s in result.suggestions:
                print(f"   • {s}")
    else:
        print(result)


def main():
    parser = argparse.ArgumentParser(description="PTO Balance Tracker")
    parser.add_argument("--request", "-r", type=str, default=DEFAULT_CONFIG["request"])
    args = parser.parse_args()
    agent = get_agent(config={"request": args.request})
    run_demo(agent, {"request": args.request})


if __name__ == "__main__":
    main()
