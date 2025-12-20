"""
Example #014: Campaign Performance Analyst
Category: business/marketing

DESCRIPTION:
Analyzes marketing campaign performance across channels. Provides cross-channel
attribution insights, ROI calculations, and actionable recommendations for
budget optimization. Identifies trends and anomalies.

PATTERNS:
- Tools (for metric calculations)
- Structured Output (CampaignAnalysis with insights)

ARGUMENTS:
- campaign_data (str): Campaign metrics data. Default: sample data
- channels (str): Channels to analyze. Default: "google,facebook,email"
- budget (float): Total campaign budget. Default: 10000
- goal_metric (str): Primary success metric. Default: "conversions"
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
    "campaign_data": """
    Channel Performance (Last 30 days):
    
    Google Ads:
    - Spend: $4,000
    - Impressions: 500,000
    - Clicks: 15,000
    - Conversions: 450
    - Revenue: $22,500
    
    Facebook Ads:
    - Spend: $3,500
    - Impressions: 800,000
    - Clicks: 12,000
    - Conversions: 280
    - Revenue: $14,000
    
    Email Marketing:
    - Spend: $500 (tools + time)
    - Sent: 50,000
    - Opens: 12,500
    - Clicks: 2,500
    - Conversions: 200
    - Revenue: $10,000
    
    Organic Search:
    - Spend: $2,000 (content creation)
    - Sessions: 80,000
    - Conversions: 400
    - Revenue: $20,000
    """,
    "channels": "google,facebook,email,organic",
    "budget": 10000,
    "goal_metric": "conversions",
}


# =============================================================================
# Output Schema
# =============================================================================

class ChannelMetrics(BaseModel):
    """Metrics for a single channel."""
    
    channel: str = Field(description="Channel name")
    spend: float = Field(description="Total spend")
    conversions: int = Field(description="Number of conversions")
    revenue: float = Field(description="Revenue generated")
    cpa: float = Field(description="Cost per acquisition")
    roas: float = Field(description="Return on ad spend")
    ctr: Optional[float] = Field(default=None, description="Click-through rate")
    conversion_rate: float = Field(description="Conversion rate %")


class Attribution(BaseModel):
    """Attribution insights."""
    
    top_performing_channel: str = Field(description="Best performing channel")
    worst_performing_channel: str = Field(description="Lowest performing channel")
    attribution_model: str = Field(description="Attribution model used")
    cross_channel_effects: list[str] = Field(description="Cross-channel interaction insights")


class BudgetRecommendation(BaseModel):
    """Budget allocation recommendation."""
    
    channel: str = Field(description="Channel name")
    current_allocation: float = Field(description="Current budget %")
    recommended_allocation: float = Field(description="Recommended budget %")
    expected_impact: str = Field(description="Expected impact of change")


class CampaignAnalysis(BaseModel):
    """Complete campaign performance analysis."""
    
    overall_roi: float = Field(description="Overall campaign ROI %")
    total_revenue: float = Field(description="Total revenue")
    total_spend: float = Field(description="Total spend")
    total_conversions: int = Field(description="Total conversions")
    blended_cpa: float = Field(description="Blended cost per acquisition")
    channel_metrics: list[ChannelMetrics] = Field(description="Per-channel breakdown")
    attribution: Attribution = Field(description="Attribution insights")
    budget_recommendations: list[BudgetRecommendation] = Field(description="Budget optimization")
    anomalies: list[str] = Field(description="Unusual patterns or concerns")
    opportunities: list[str] = Field(description="Growth opportunities")
    next_steps: list[str] = Field(description="Recommended actions")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Campaign Performance Analyst agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for campaign analysis
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Campaign Performance Analyst",
        instructions=[
            "You are an expert marketing analyst specializing in campaign performance.",
            "Analyze marketing data to extract actionable insights and optimize ROI.",
            "",
            f"Goal Metric: {cfg['goal_metric']}",
            f"Budget: ${cfg['budget']:,.2f}",
            "",
            "Key Metrics to Calculate:",
            "- CPA (Cost Per Acquisition) = Spend / Conversions",
            "- ROAS (Return on Ad Spend) = Revenue / Spend",
            "- CTR (Click-Through Rate) = Clicks / Impressions * 100",
            "- Conversion Rate = Conversions / Clicks * 100",
            "- ROI = (Revenue - Spend) / Spend * 100",
            "",
            "Analysis Framework:",
            "1. Calculate key metrics for each channel",
            "2. Identify top and bottom performers",
            "3. Look for cross-channel effects",
            "4. Detect anomalies or concerning trends",
            "5. Recommend budget reallocation",
            "6. Suggest specific optimizations",
            "",
            "Be data-driven but also consider qualitative factors like brand building.",
        ],
        output_schema=CampaignAnalysis,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of campaign analysis."""
    print("\n" + "=" * 60)
    print("  Campaign Performance Analyst - Demo")
    print("=" * 60)
    
    data = config.get("campaign_data", DEFAULT_CONFIG["campaign_data"])
    goal = config.get("goal_metric", DEFAULT_CONFIG["goal_metric"])
    budget = config.get("budget", DEFAULT_CONFIG["budget"])
    
    query = f"""
    Analyze this campaign performance data:
    
    {data}
    
    Primary Goal: Maximize {goal}
    Total Budget: ${budget:,.2f}
    
    Provide:
    1. Complete metrics breakdown by channel
    2. Attribution insights
    3. Budget reallocation recommendations
    4. Anomalies or concerns
    5. Specific next steps
    """
    
    print(f"\nGoal Metric: {goal}")
    print(f"Budget: ${budget:,.2f}")
    print("-" * 40)
    print("Analyzing campaign data...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, CampaignAnalysis):
        print(f"\n{'='*50}")
        print(f"CAMPAIGN ROI: {result.overall_roi:.1f}%")
        print(f"{'='*50}")
        
        print(f"\n💰 Overall Performance:")
        print(f"  Revenue: ${result.total_revenue:,.2f}")
        print(f"  Spend: ${result.total_spend:,.2f}")
        print(f"  Conversions: {result.total_conversions:,}")
        print(f"  Blended CPA: ${result.blended_cpa:.2f}")
        
        print(f"\n📊 Channel Breakdown:")
        for cm in result.channel_metrics:
            print(f"\n  {cm.channel.upper()}")
            print(f"    Spend: ${cm.spend:,.2f} | Revenue: ${cm.revenue:,.2f}")
            print(f"    Conversions: {cm.conversions} | CPA: ${cm.cpa:.2f}")
            print(f"    ROAS: {cm.roas:.2f}x | Conv Rate: {cm.conversion_rate:.1f}%")
        
        print(f"\n🎯 Attribution Insights:")
        print(f"  Top Channel: {result.attribution.top_performing_channel}")
        print(f"  Worst Channel: {result.attribution.worst_performing_channel}")
        print(f"  Model: {result.attribution.attribution_model}")
        for effect in result.attribution.cross_channel_effects[:2]:
            print(f"  • {effect}")
        
        print(f"\n💡 Budget Recommendations:")
        for rec in result.budget_recommendations:
            change = rec.recommended_allocation - rec.current_allocation
            arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
            print(f"  {rec.channel}: {rec.current_allocation:.0f}% {arrow} {rec.recommended_allocation:.0f}%")
            print(f"    Impact: {rec.expected_impact}")
        
        if result.anomalies:
            print(f"\n⚠️  Anomalies:")
            for anomaly in result.anomalies:
                print(f"  • {anomaly}")
        
        print(f"\n🚀 Opportunities:")
        for opp in result.opportunities[:3]:
            print(f"  • {opp}")
        
        print(f"\n📋 Next Steps:")
        for i, step in enumerate(result.next_steps[:5], 1):
            print(f"  {i}. {step}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Campaign Performance Analyst - Analyze marketing campaign ROI"
    )
    
    parser.add_argument(
        "--data", "-d",
        type=str,
        default=DEFAULT_CONFIG["campaign_data"],
        help="Campaign metrics data"
    )
    parser.add_argument(
        "--budget", "-b",
        type=float,
        default=DEFAULT_CONFIG["budget"],
        help=f"Total budget (default: {DEFAULT_CONFIG['budget']})"
    )
    parser.add_argument(
        "--goal", "-g",
        type=str,
        default=DEFAULT_CONFIG["goal_metric"],
        help=f"Goal metric (default: {DEFAULT_CONFIG['goal_metric']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "campaign_data": args.data,
        "budget": args.budget,
        "goal_metric": args.goal,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
