"""
Example #149: Return Processor Agent
Category: industry/ecommerce
DESCRIPTION: Processes product returns and generates RMA decisions
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"order_id": "ORD-2024-5678", "return_reason": "defective", "days_since_purchase": 12}

class ReturnDecision(BaseModel):
    rma_number: str = Field(description="Return authorization number")
    decision: str = Field(description="approved/denied/partial")
    refund_amount: float = Field(description="Refund amount")
    refund_method: str = Field(description="Refund method")
    return_shipping: str = Field(description="Who pays return shipping")
    restocking_fee: float = Field(description="Restocking fee if any")
    reason_category: str = Field(description="Categorized return reason")
    customer_fault: bool = Field(description="Is return due to customer error")
    quality_flag: bool = Field(description="Flag for quality team review")
    replacement_offered: bool = Field(description="Replacement offered")
    resolution_notes: str = Field(description="Notes for resolution")
    customer_message: str = Field(description="Message to send to customer")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Return Processor",
        instructions=[
            "You are an expert e-commerce returns and RMA specialist.",
            "Process return requests fairly and efficiently",
            "Apply return policy rules consistently",
            "Balance customer satisfaction with loss prevention",
            "Flag quality issues for product team review",
            "Generate appropriate customer communications",
        ],
        output_schema=ReturnDecision,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Return Processor Agent - Demo")
    print("=" * 60)
    query = f"""Process this return request:
- Order: {config['order_id']}
- Return Reason: {config['return_reason']}
- Days Since Purchase: {config['days_since_purchase']}
- Product: Wireless Mouse ($45.99)
- Customer History: Good standing, 8 previous orders

Evaluate and provide RMA decision."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ReturnDecision):
        print(f"\n📋 RMA: {result.rma_number}")
        print(f"✅ Decision: {result.decision.upper()}")
        print(f"💰 Refund: ${result.refund_amount:.2f} via {result.refund_method}")
        if result.restocking_fee > 0:
            print(f"📊 Restocking Fee: ${result.restocking_fee:.2f}")
        print(f"🚚 Return Shipping: {result.return_shipping}")
        print(f"\n📝 Category: {result.reason_category}")
        if result.quality_flag:
            print("⚠️ Flagged for Quality Review")
        if result.replacement_offered:
            print("🔄 Replacement Offered")
        print(f"\n💬 Customer Message:\n{result.customer_message[:200]}...")

def main():
    parser = argparse.ArgumentParser(description="Return Processor Agent")
    parser.add_argument("--order", "-o", default=DEFAULT_CONFIG["order_id"])
    parser.add_argument("--reason", "-r", default=DEFAULT_CONFIG["return_reason"])
    parser.add_argument("--days", "-d", type=int, default=DEFAULT_CONFIG["days_since_purchase"])
    args = parser.parse_args()
    config = {"order_id": args.order, "return_reason": args.reason, "days_since_purchase": args.days}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
