"""
Example #144: Order Processor Agent
Category: industry/ecommerce
DESCRIPTION: Processes and validates e-commerce orders
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"order_id": "ORD-2024-001234", "order_value": 299.99}

class OrderValidation(BaseModel):
    field: str = Field(description="Field validated")
    status: str = Field(description="pass/fail/warning")
    message: str = Field(description="Validation message")

class ProcessedOrder(BaseModel):
    order_id: str = Field(description="Order identifier")
    processing_status: str = Field(description="approved/pending/rejected")
    validations: list[OrderValidation] = Field(description="Validation results")
    fraud_score: int = Field(description="Fraud risk score 0-100")
    fraud_flags: list[str] = Field(description="Fraud warning flags")
    fulfillment_priority: str = Field(description="high/normal/low priority")
    estimated_ship_date: str = Field(description="Estimated shipping date")
    customer_notes: str = Field(description="Notes for customer service")
    next_steps: list[str] = Field(description="Processing next steps")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Order Processor",
        instructions=[
            "You are an expert e-commerce order processing specialist.",
            f"Process orders with IDs like {cfg['order_id']}",
            "Validate order data, payment, and shipping information",
            "Assess fraud risk using standard indicators",
            "Determine fulfillment priority and timeline",
            "Provide clear processing status and next steps",
        ],
        output_schema=ProcessedOrder,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Order Processor Agent - Demo")
    print("=" * 60)
    sample_order = f"""Order: {config['order_id']}
Value: ${config['order_value']:.2f}
Items: 2x Widget Pro, 1x Accessory Kit
Shipping: Standard Ground to California
Payment: Credit Card (Visa ending 4242)
Customer: Returning customer (5 previous orders)"""
    query = f"""Process this e-commerce order:

{sample_order}

Validate, check fraud, and provide processing status."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ProcessedOrder):
        print(f"\n📋 Order: {result.order_id}")
        print(f"✅ Status: {result.processing_status.upper()}")
        print(f"🛡️ Fraud Score: {result.fraud_score}/100")
        if result.fraud_flags:
            print(f"⚠️ Flags: {', '.join(result.fraud_flags[:3])}")
        print(f"📦 Priority: {result.fulfillment_priority}")
        print(f"🚚 Est. Ship: {result.estimated_ship_date}")
        print(f"\n✓ Validations:")
        for v in result.validations[:4]:
            icon = "✅" if v.status == "pass" else "⚠️" if v.status == "warning" else "❌"
            print(f"  {icon} {v.field}: {v.message}")

def main():
    parser = argparse.ArgumentParser(description="Order Processor Agent")
    parser.add_argument("--order", "-o", default=DEFAULT_CONFIG["order_id"])
    parser.add_argument("--value", "-v", type=float, default=DEFAULT_CONFIG["order_value"])
    args = parser.parse_args()
    config = {"order_id": args.order, "order_value": args.value}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
