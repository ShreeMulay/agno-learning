"""
Example #038: Fraud Detection Agent
Category: business/finance

DESCRIPTION:
Analyzes transactions for fraud patterns, flags suspicious activity,
and provides risk scores with explanations.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "transactions": """
    Recent Transactions for Account #4567:
    1. Dec 15, 10:23 AM - Coffee Shop, NYC - $4.50
    2. Dec 15, 10:45 AM - Gas Station, Chicago - $85.00
    3. Dec 15, 11:30 AM - Electronics Store, Chicago - $2,499
    4. Dec 15, 11:35 AM - Electronics Store, Chicago - $1,899
    5. Dec 15, 12:00 PM - ATM Withdrawal, LA - $500
    6. Dec 15, 2:30 PM - Online Purchase, International - $3,200
    
    Account History: Typically NYC-based, avg transaction $150
    """,
}

class TransactionAnalysis(BaseModel):
    transaction_id: str = Field(description="Transaction reference")
    amount: float = Field(description="Amount")
    risk_score: int = Field(ge=0, le=100, description="Fraud risk 0-100")
    flags: list[str] = Field(description="Risk flags triggered")
    recommendation: str = Field(description="allow/review/block")

class FraudReport(BaseModel):
    account: str = Field(description="Account number")
    overall_risk: str = Field(description="low/medium/high/critical")
    transactions_analyzed: int = Field(description="Count")
    suspicious_count: int = Field(description="Flagged count")
    analysis: list[TransactionAnalysis] = Field(description="Per-transaction")
    patterns_detected: list[str] = Field(description="Fraud patterns")
    recommended_actions: list[str] = Field(description="What to do")
    customer_contact: bool = Field(description="Should contact customer")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Fraud Detection Agent",
        instructions=[
            "You are a fraud detection specialist.",
            "Analyze transactions for suspicious patterns.",
            "Flag: impossible travel, unusual amounts, velocity",
            "Provide clear explanations for flags.",
        ],
        output_schema=FraudReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Fraud Detection Agent - Demo")
    print("=" * 60)
    data = config.get("transactions", DEFAULT_CONFIG["transactions"])
    response = agent.run(f"Analyze for fraud:\n\n{data}")
    result = response.content
    if isinstance(result, FraudReport):
        risk_icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
        print(f"\n🔍 Account: {result.account}")
        print(f"{risk_icon.get(result.overall_risk, '⚪')} Risk: {result.overall_risk.upper()}")
        print(f"Analyzed: {result.transactions_analyzed} | Suspicious: {result.suspicious_count}")
        print(f"\n📊 Transaction Analysis:")
        for t in result.analysis:
            icon = "🔴" if t.risk_score > 70 else "🟡" if t.risk_score > 40 else "🟢"
            print(f"  {icon} {t.transaction_id}: ${t.amount:,.2f} - {t.recommendation.upper()}")
            if t.flags:
                print(f"      Flags: {', '.join(t.flags)}")
        if result.patterns_detected:
            print(f"\n⚠️ Patterns: {', '.join(result.patterns_detected)}")
        print(f"\n📞 Contact Customer: {'Yes' if result.customer_contact else 'No'}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Fraud Detection Agent")
    parser.add_argument("--data", "-d", type=str, default=DEFAULT_CONFIG["transactions"])
    args = parser.parse_args()
    agent = get_agent()
    run_demo(agent, {"transactions": args.data})

if __name__ == "__main__":
    main()
