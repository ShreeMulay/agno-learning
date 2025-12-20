"""
Example #006: Competitor Battle Cards
Category: business/sales

DESCRIPTION:
Generates real-time competitive intelligence battle cards by researching
competitors and creating comparison matrices, objection handlers, and
win strategies for sales teams.

PATTERNS:
- Tools (DuckDuckGo for competitor research)
- Structured Output (BattleCard schema)

ARGUMENTS:
- competitor (str): Competitor to analyze. Default: "Salesforce"
- your_product (str): Your product name. Default: "SalesBot CRM"
- focus_area (str): Key differentiator. Default: "AI automation"
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, Field


DEFAULT_CONFIG = {
    "competitor": "Salesforce",
    "your_product": "SalesBot CRM",
    "focus_area": "AI automation",
}


class ObjectionHandler(BaseModel):
    """How to handle a specific objection."""
    objection: str = Field(description="Common objection from prospect")
    response: str = Field(description="Recommended response")
    proof_point: str = Field(description="Evidence to support response")


class ComparisonPoint(BaseModel):
    """Feature comparison point."""
    category: str = Field(description="Feature category")
    us: str = Field(description="Our capability")
    them: str = Field(description="Competitor capability")
    advantage: str = Field(description="who_wins: us/them/tie")


class BattleCard(BaseModel):
    """Complete competitive battle card."""
    
    competitor_name: str = Field(description="Competitor being analyzed")
    competitor_summary: str = Field(description="Brief competitor overview")
    
    their_strengths: list[str] = Field(description="Where they're strong")
    their_weaknesses: list[str] = Field(description="Where they're weak")
    
    comparison_matrix: list[ComparisonPoint] = Field(description="Feature comparison")
    
    objection_handlers: list[ObjectionHandler] = Field(description="Common objections")
    
    win_strategies: list[str] = Field(description="How to win against them")
    loss_reasons: list[str] = Field(description="Why we might lose")
    
    key_differentiators: list[str] = Field(description="Our unique advantages")
    talking_points: list[str] = Field(description="Key messages for reps")
    
    recent_news: list[str] = Field(description="Recent competitor news")
    last_updated: str = Field(description="When this card was generated")


def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """Create the Competitor Battle Cards agent."""
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Battle Card Generator",
        instructions=[
            "You are a competitive intelligence analyst for sales teams.",
            f"Your product: {cfg['your_product']}",
            f"Key differentiator: {cfg['focus_area']}",
            "",
            "Research the competitor thoroughly and create a battle card that:",
            "- Is honest about competitor strengths (reps need truth)",
            "- Highlights genuine weaknesses we can exploit",
            "- Provides specific, usable objection handlers",
            "- Gives actionable win strategies",
            "",
            "Keep responses practical and sales-ready.",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=BattleCard,
        use_json_mode=True,
        markdown=True,
    )


def run_demo(agent: Agent, config: dict):
    """Generate a battle card demo."""
    print("\n" + "=" * 60)
    print("  Competitor Battle Cards - Demo")
    print("=" * 60)
    
    query = f"""
    Create a battle card for competing against {config['competitor']}.
    Our product is {config['your_product']} with focus on {config['focus_area']}.
    Research their latest news and positioning.
    """
    
    print(f"\nResearching: {config['competitor']}...")
    print("-" * 40)
    
    response = agent.run(query)
    result = response.content
    
    if isinstance(result, BattleCard):
        print(f"\n{'='*60}")
        print(f"  BATTLE CARD: vs {result.competitor_name}")
        print(f"  Updated: {result.last_updated}")
        print(f"{'='*60}")
        
        print(f"\n📋 OVERVIEW\n{result.competitor_summary}")
        
        print(f"\n💪 THEIR STRENGTHS")
        for s in result.their_strengths:
            print(f"  • {s}")
        
        print(f"\n🎯 THEIR WEAKNESSES")
        for w in result.their_weaknesses:
            print(f"  • {w}")
        
        print(f"\n📊 COMPARISON MATRIX")
        for c in result.comparison_matrix:
            icon = "✅" if c.advantage == "us" else "❌" if c.advantage == "them" else "➖"
            print(f"  {icon} {c.category}: Us={c.us} | Them={c.them}")
        
        print(f"\n🛡️ OBJECTION HANDLERS")
        for o in result.objection_handlers:
            print(f"  Q: \"{o.objection}\"")
            print(f"  A: {o.response}")
            print(f"  Proof: {o.proof_point}\n")
        
        print(f"\n🏆 WIN STRATEGIES")
        for i, s in enumerate(result.win_strategies, 1):
            print(f"  {i}. {s}")
        
        print(f"\n💬 TALKING POINTS")
        for t in result.talking_points:
            print(f"  • {t}")
    else:
        print("\n[Raw Response]")
        print(result if isinstance(result, str) else str(result))


def main():
    parser = argparse.ArgumentParser(description="Competitor Battle Cards")
    parser.add_argument("--competitor", "-c", type=str, default=DEFAULT_CONFIG["competitor"])
    parser.add_argument("--product", "-p", type=str, default=DEFAULT_CONFIG["your_product"])
    parser.add_argument("--focus", "-f", type=str, default=DEFAULT_CONFIG["focus_area"])
    args = parser.parse_args()
    
    config = {
        "competitor": args.competitor,
        "your_product": args.product,
        "focus_area": args.focus,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
