"""
Example #147: Cart Abandonment Agent
Category: industry/ecommerce
DESCRIPTION: Analyzes cart abandonment and generates recovery strategies
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"cart_value": 149.99, "items_count": 3, "customer_type": "returning"}

class RecoveryEmail(BaseModel):
    subject_line: str = Field(description="Email subject line")
    preview_text: str = Field(description="Email preview text")
    key_message: str = Field(description="Main message theme")
    incentive: str = Field(description="Incentive offered if any")

class CartRecoveryPlan(BaseModel):
    abandonment_reason_guess: str = Field(description="Likely reason for abandonment")
    recovery_priority: str = Field(description="high/medium/low priority")
    recommended_approach: str = Field(description="Recovery approach")
    email_sequence: list[RecoveryEmail] = Field(description="Recovery email sequence")
    sms_message: str = Field(description="SMS recovery message if applicable")
    discount_recommendation: str = Field(description="Discount strategy")
    urgency_tactics: list[str] = Field(description="Urgency tactics to use")
    expected_recovery_rate: int = Field(description="Expected recovery percentage")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Cart Abandonment Recovery",
        instructions=[
            "You are an expert e-commerce cart recovery specialist.",
            f"Develop recovery strategies for {cfg['customer_type']} customers",
            "Create compelling recovery email sequences",
            "Balance urgency with customer experience",
            "Optimize discount offers for margin preservation",
            "Use psychological triggers appropriately",
        ],
        output_schema=CartRecoveryPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Cart Abandonment Recovery Agent - Demo")
    print("=" * 60)
    query = f"""Create cart recovery strategy:
- Cart Value: ${config['cart_value']:.2f}
- Items in Cart: {config['items_count']}
- Customer Type: {config['customer_type']}
- Abandoned: 2 hours ago
- Cart: Electronics items

Generate recovery emails and strategy."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, CartRecoveryPlan):
        print(f"\n🛒 Likely Reason: {result.abandonment_reason_guess}")
        print(f"📊 Priority: {result.recovery_priority}")
        print(f"🎯 Approach: {result.recommended_approach}")
        print(f"\n📧 Email Sequence:")
        for i, email in enumerate(result.email_sequence[:3], 1):
            print(f"  Email {i}: {email.subject_line}")
            print(f"    Message: {email.key_message}")
            if email.incentive:
                print(f"    Incentive: {email.incentive}")
        print(f"\n💰 Discount Strategy: {result.discount_recommendation}")
        print(f"📈 Expected Recovery: {result.expected_recovery_rate}%")

def main():
    parser = argparse.ArgumentParser(description="Cart Abandonment Agent")
    parser.add_argument("--value", "-v", type=float, default=DEFAULT_CONFIG["cart_value"])
    parser.add_argument("--items", "-i", type=int, default=DEFAULT_CONFIG["items_count"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["customer_type"])
    args = parser.parse_args()
    config = {"cart_value": args.value, "items_count": args.items, "customer_type": args.type}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
