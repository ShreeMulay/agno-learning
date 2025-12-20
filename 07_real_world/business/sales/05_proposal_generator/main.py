"""
Example #005: Proposal Generator
Category: business/sales

DESCRIPTION:
Generates customized sales proposals from templates and prospect data.
Researches the prospect's company to personalize value propositions
and creates executive summaries, pricing sections, and next steps.

PATTERNS:
- Tools (DuckDuckGo for company research)
- Knowledge (proposal templates)
- Structured Output (Proposal schema)

ARGUMENTS:
- prospect_company (str): Target company. Default: "TechCorp"
- prospect_name (str): Decision maker. Default: "Jane Smith"
- product (str): Product being proposed. Default: "Enterprise Platform"
- price (int): Proposed price. Default: 50000
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "prospect_company": "TechCorp",
    "prospect_name": "Jane Smith",
    "product": "Enterprise Platform",
    "price": 50000,
    "your_company": "SalesBot Inc",
}


# =============================================================================
# Output Schema
# =============================================================================

class PricingItem(BaseModel):
    """Line item in pricing."""
    item: str = Field(description="What's included")
    price: int = Field(description="Price in USD")
    notes: str = Field(default="", description="Additional notes")


class Proposal(BaseModel):
    """Complete sales proposal."""
    
    title: str = Field(description="Proposal title")
    executive_summary: str = Field(description="2-3 paragraph executive summary")
    
    # Prospect-specific
    prospect_challenges: list[str] = Field(description="Identified challenges")
    value_propositions: list[str] = Field(description="How we solve their problems")
    
    # Solution
    solution_overview: str = Field(description="Overview of proposed solution")
    key_features: list[str] = Field(description="Key features relevant to prospect")
    
    # Pricing
    pricing_items: list[PricingItem] = Field(description="Itemized pricing")
    total_price: int = Field(description="Total proposal value")
    payment_terms: str = Field(description="Payment structure")
    
    # Next steps
    implementation_timeline: str = Field(description="Expected timeline")
    next_steps: list[str] = Field(description="Immediate next actions")
    
    # Personalization
    personalization_notes: list[str] = Field(
        description="How this proposal was customized for the prospect"
    )


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Create the Proposal Generator agent."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Proposal Generator",
        instructions=[
            "You are a sales proposal expert who creates compelling, customized proposals.",
            f"You work for {cfg['your_company']}.",
            "",
            "Proposal Guidelines:",
            "- Research the prospect company before writing",
            "- Lead with value, not features",
            "- Connect each feature to a specific prospect challenge",
            "- Be specific about ROI and outcomes",
            "- Create urgency without being pushy",
            "",
            "Structure:",
            "1. Executive Summary (grab attention, state value)",
            "2. Understanding Their Challenges (show you did homework)",
            "3. Proposed Solution (how you solve their problems)",
            "4. Pricing (clear, transparent)",
            "5. Next Steps (make it easy to say yes)",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=Proposal,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Generate a sample proposal."""
    print("\n" + "=" * 60)
    print("  Proposal Generator - Demo")
    print("=" * 60)
    
    query = f"""
    Create a proposal for:
    - Company: {config['prospect_company']}
    - Decision Maker: {config['prospect_name']}
    - Product: {config['product']}
    - Target Price: ${config['price']:,}
    
    Research the company and create a personalized proposal.
    """
    
    print(f"\nGenerating proposal for {config['prospect_company']}...")
    print("-" * 40)
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, Proposal):
        print(f"\n{'='*60}")
        print(f"  {result.title}")
        print(f"{'='*60}")
        
        print(f"\n📋 EXECUTIVE SUMMARY")
        print(f"{result.executive_summary}")
        
        print(f"\n🎯 THEIR CHALLENGES")
        for challenge in result.prospect_challenges:
            print(f"  • {challenge}")
        
        print(f"\n✅ OUR VALUE")
        for value in result.value_propositions:
            print(f"  • {value}")
        
        print(f"\n💡 SOLUTION OVERVIEW")
        print(f"{result.solution_overview}")
        
        print(f"\n🔑 KEY FEATURES")
        for feature in result.key_features:
            print(f"  • {feature}")
        
        print(f"\n💰 PRICING")
        for item in result.pricing_items:
            print(f"  • {item.item}: ${item.price:,}")
            if item.notes:
                print(f"    ({item.notes})")
        print(f"\n  TOTAL: ${result.total_price:,}")
        print(f"  Terms: {result.payment_terms}")
        
        print(f"\n📅 TIMELINE")
        print(f"  {result.implementation_timeline}")
        
        print(f"\n📌 NEXT STEPS")
        for i, step in enumerate(result.next_steps, 1):
            print(f"  {i}. {step}")
        
        print(f"\n🎨 PERSONALIZATION")
        for note in result.personalization_notes:
            print(f"  • {note}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    parser = argparse.ArgumentParser(description="Proposal Generator")
    parser.add_argument("--company", type=str, default=DEFAULT_CONFIG["prospect_company"])
    parser.add_argument("--contact", type=str, default=DEFAULT_CONFIG["prospect_name"])
    parser.add_argument("--product", type=str, default=DEFAULT_CONFIG["product"])
    parser.add_argument("--price", type=int, default=DEFAULT_CONFIG["price"])
    args = parser.parse_args()
    
    config = {
        **DEFAULT_CONFIG,
        "prospect_company": args.company,
        "prospect_name": args.contact,
        "product": args.product,
        "price": args.price,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
