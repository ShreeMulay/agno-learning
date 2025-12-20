"""
Example #030: Win/Loss Analyst
Category: business/customer_success

DESCRIPTION:
Analyzes win/loss interview summaries to extract patterns, identify
competitive insights, and generate actionable recommendations for
improving win rates.

PATTERNS:
- Knowledge (competitive analysis)
- Structured Output (WinLossReport)

ARGUMENTS:
- interviews (str): Win/loss interview data. Default: sample
"""

import argparse
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "interviews": """
    Win/Loss Interviews (Q4):
    
    === WIN: TechStart Inc ($48K) ===
    Decision Factors:
    - "Your API was way easier to integrate than Competitor X"
    - "The trial support was exceptional - Sarah was very helpful"
    - "Pricing was competitive, especially the startup discount"
    Concerns Overcome:
    - "Initially worried about scalability, but the enterprise case studies helped"
    
    === LOSS: BigCorp Ltd ($120K) to Competitor X ===
    Decision Factors:
    - "Competitor X had SSO/SAML which is required for our security policy"
    - "Their enterprise support tier included dedicated CSM"
    - "Price was actually similar, features were the deciding factor"
    What Could Have Changed Outcome:
    - "If you had SSO, we would have chosen you for the better UX"
    
    === WIN: DataFlow Co ($36K) ===
    Decision Factors:
    - "Best documentation we've seen - our devs loved it"
    - "The ROI calculator on your website was really convincing"
    - "Founder's LinkedIn posts showed deep domain expertise"
    What Almost Lost It:
    - "Mobile app was weak, but not a dealbreaker for us"
    
    === LOSS: FinanceHub ($85K) to Competitor Y ===
    Decision Factors:
    - "They had deeper analytics and reporting dashboards"
    - "Compliance certifications (SOC2 Type II) were already done"
    - "Your sales process felt pushy and rushed"
    What Could Have Changed Outcome:
    - "More discovery upfront, we felt you didn't understand our needs"
    
    === LOSS: CloudNine ($65K) - No Decision ===
    Reason:
    - "Budget got cut, project delayed indefinitely"
    - "Champion left the company during evaluation"
    - "Would still consider you when project resumes"
    
    === WIN: RetailMax ($72K) ===
    Decision Factors:
    - "Switching from Competitor X - their support declined after acquisition"
    - "Your migration tool made it painless"
    - "Better value at our scale"
    """,
}


# =============================================================================
# Output Schema
# =============================================================================

class WinFactor(BaseModel):
    """Factor contributing to wins."""
    
    factor: str = Field(description="Win factor")
    frequency: int = Field(description="Times mentioned")
    revenue_impact: str = Field(description="Revenue from deals with this factor")
    quotes: list[str] = Field(description="Supporting quotes")
    leverage_advice: str = Field(description="How to leverage this more")


class LossFactor(BaseModel):
    """Factor contributing to losses."""
    
    factor: str = Field(description="Loss factor")
    frequency: int = Field(description="Times mentioned")
    revenue_lost: str = Field(description="Revenue lost to this factor")
    competitor: Optional[str] = Field(default=None, description="Competitor if relevant")
    fix_recommendation: str = Field(description="How to address this")
    priority: str = Field(description="critical/high/medium/low")


class CompetitorInsight(BaseModel):
    """Competitive intelligence."""
    
    competitor: str = Field(description="Competitor name")
    wins_against: int = Field(description="Deals won against them")
    losses_to: int = Field(description="Deals lost to them")
    their_strengths: list[str] = Field(description="Where they beat us")
    our_advantages: list[str] = Field(description="Where we beat them")
    battlecard_update: str = Field(description="Recommended battlecard update")


class WinLossReport(BaseModel):
    """Complete win/loss analysis."""
    
    period: str = Field(description="Analysis period")
    total_deals: int = Field(description="Total deals analyzed")
    win_count: int = Field(description="Number of wins")
    loss_count: int = Field(description="Number of losses")
    no_decision_count: int = Field(description="Stalled/no decision")
    win_rate: float = Field(description="Win rate percentage")
    win_factors: list[WinFactor] = Field(description="What's driving wins")
    loss_factors: list[LossFactor] = Field(description="What's causing losses")
    competitor_insights: list[CompetitorInsight] = Field(description="Competitive analysis")
    product_gaps: list[str] = Field(description="Product improvements needed")
    sales_process_improvements: list[str] = Field(description="Sales process fixes")
    marketing_recommendations: list[str] = Field(description="Messaging improvements")
    quick_wins: list[str] = Field(description="Immediate actions")
    strategic_priorities: list[str] = Field(description="Long-term focus areas")
    executive_summary: str = Field(description="Summary for leadership")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Win/Loss Analyst agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for win/loss analysis
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Win/Loss Analyst",
        instructions=[
            "You are a competitive intelligence analyst specializing in win/loss analysis.",
            "Extract actionable patterns from deal outcomes to improve win rates.",
            "",
            "Analysis Framework:",
            "1. Quantify: Count frequency and revenue impact",
            "2. Categorize: Product, Price, People, Process",
            "3. Compare: Us vs. specific competitors",
            "4. Prioritize: By revenue impact and fixability",
            "",
            "Key Categories to Analyze:",
            "- Product: Features, integrations, performance",
            "- Pricing: Cost, packaging, discounts",
            "- People: Sales, support, leadership",
            "- Process: Trial, demo, negotiation",
            "- Proof: Case studies, references, trust",
            "",
            "Output Focus:",
            "- What can Product fix?",
            "- What can Sales improve?",
            "- What should Marketing emphasize?",
            "- How do we beat each competitor?",
            "",
            "Be specific with recommendations. Vague advice isn't actionable.",
        ],
        output_schema=WinLossReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of win/loss analysis."""
    print("\n" + "=" * 60)
    print("  Win/Loss Analyst - Demo")
    print("=" * 60)
    
    interviews = config.get("interviews", DEFAULT_CONFIG["interviews"])
    
    query = f"""
    Analyze these win/loss interviews:
    
    {interviews}
    
    Extract patterns, competitive insights, and actionable recommendations.
    """
    
    print("\nAnalyzing win/loss data...")
    print("-" * 40)
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, WinLossReport):
        print(f"\n{'='*50}")
        print(f"WIN/LOSS ANALYSIS: {result.period}")
        print(f"{'='*50}")
        
        print(f"\n📊 Overview:")
        print(f"  Total Deals: {result.total_deals}")
        print(f"  Wins: {result.win_count} | Losses: {result.loss_count} | No Decision: {result.no_decision_count}")
        print(f"  Win Rate: {result.win_rate:.1f}%")
        
        print(f"\n✅ Win Factors:")
        for wf in result.win_factors[:3]:
            print(f"\n  {wf.factor} ({wf.frequency}x)")
            print(f"    Revenue: {wf.revenue_impact}")
            print(f"    Quote: \"{wf.quotes[0][:60]}...\"")
            print(f"    Leverage: {wf.leverage_advice}")
        
        print(f"\n❌ Loss Factors:")
        for lf in result.loss_factors[:3]:
            prio_icon = "🔴" if lf.priority == "critical" else "🟠" if lf.priority == "high" else "🟡"
            print(f"\n  {prio_icon} {lf.factor} ({lf.frequency}x) - {lf.priority}")
            print(f"    Revenue Lost: {lf.revenue_lost}")
            if lf.competitor:
                print(f"    Lost to: {lf.competitor}")
            print(f"    Fix: {lf.fix_recommendation}")
        
        print(f"\n🏁 Competitor Insights:")
        for ci in result.competitor_insights:
            print(f"\n  {ci.competitor}")
            print(f"    Record: {ci.wins_against}W - {ci.losses_to}L")
            print(f"    Their Edge: {', '.join(ci.their_strengths[:2])}")
            print(f"    Our Edge: {', '.join(ci.our_advantages[:2])}")
            print(f"    Battlecard: {ci.battlecard_update}")
        
        print(f"\n🔧 Product Gaps:")
        for gap in result.product_gaps[:3]:
            print(f"  • {gap}")
        
        print(f"\n📞 Sales Process Fixes:")
        for fix in result.sales_process_improvements[:3]:
            print(f"  • {fix}")
        
        print(f"\n📣 Marketing Recommendations:")
        for rec in result.marketing_recommendations[:3]:
            print(f"  • {rec}")
        
        print(f"\n⚡ Quick Wins:")
        for win in result.quick_wins[:3]:
            print(f"  • {win}")
        
        print(f"\n🎯 Strategic Priorities:")
        for prio in result.strategic_priorities[:3]:
            print(f"  • {prio}")
        
        print(f"\n📋 Executive Summary:")
        print(f"  {result.executive_summary}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Win/Loss Analyst - Extract patterns from deal outcomes"
    )
    
    parser.add_argument(
        "--interviews", "-i",
        type=str,
        default=DEFAULT_CONFIG["interviews"],
        help="Win/loss interview data"
    )
    
    args = parser.parse_args()
    
    config = {
        "interviews": args.interviews,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
