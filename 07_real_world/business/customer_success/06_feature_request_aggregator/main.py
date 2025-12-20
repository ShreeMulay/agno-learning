"""
Example #026: Feature Request Aggregator
Category: business/customer_success

DESCRIPTION:
Clusters and prioritizes feature requests from multiple sources. Identifies
trends, calculates business impact, and generates product roadmap
recommendations based on customer needs.

PATTERNS:
- Knowledge (product development best practices)
- Structured Output (FeatureRequestReport)

ARGUMENTS:
- requests (str): Feature requests data. Default: sample
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
    "requests": """
    Feature Requests (Last 90 Days):
    
    1. "Need dark mode" - 45 requests
       Sources: Support tickets (20), Feedback form (15), Social media (10)
       Customer tiers: Enterprise (5), Pro (25), Free (15)
       
    2. "API rate limit increase" - 38 requests
       Sources: Support tickets (30), Sales calls (8)
       Customer tiers: Enterprise (25), Pro (13)
       Lost deals: 3 mentioned this as blocker
       
    3. "Mobile app for iOS" - 35 requests
       Sources: Feedback form (20), NPS surveys (10), Social (5)
       Customer tiers: Pro (20), Free (15)
       
    4. "Slack integration" - 28 requests
       Sources: Support tickets (10), Sales calls (12), Feedback (6)
       Customer tiers: Enterprise (15), Pro (13)
       Competitor comparison: "Competitor X has this"
       
    5. "Export to Excel" - 25 requests
       Sources: Support tickets (20), Feedback (5)
       Customer tiers: Enterprise (10), Pro (10), Free (5)
       
    6. "SSO/SAML support" - 22 requests
       Sources: Sales calls (18), Support (4)
       Customer tiers: Enterprise (22)
       Lost deals: 5 blocked by this
       
    7. "Better reporting dashboard" - 20 requests
       Sources: NPS surveys (12), Support (8)
       Customer tiers: Enterprise (8), Pro (12)
       
    8. "Bulk import tool" - 15 requests
       Sources: Support tickets (15)
       Customer tiers: Enterprise (10), Pro (5)
    """,
}


# =============================================================================
# Output Schema
# =============================================================================

class FeatureCluster(BaseModel):
    """Grouped feature requests."""
    
    cluster_name: str = Field(description="Theme name")
    requests_count: int = Field(description="Total requests")
    sample_requests: list[str] = Field(description="Example request titles")
    customer_segments: list[str] = Field(description="Primary customer segments")
    revenue_impact: str = Field(description="Potential revenue impact")


class PrioritizedFeature(BaseModel):
    """Prioritized feature recommendation."""
    
    feature: str = Field(description="Feature name")
    priority_score: int = Field(ge=0, le=100, description="Priority score 0-100")
    request_count: int = Field(description="Number of requests")
    revenue_at_risk: str = Field(description="Revenue potentially lost")
    effort_estimate: str = Field(description="Development effort")
    rice_score: float = Field(description="RICE prioritization score")
    rationale: str = Field(description="Why this priority")


class TrendAnalysis(BaseModel):
    """Trend in feature requests."""
    
    trend: str = Field(description="What's trending")
    direction: str = Field(description="growing/stable/declining")
    driver: str = Field(description="What's causing this")
    competitive_pressure: bool = Field(description="Competitor-driven?")


class FeatureRequestReport(BaseModel):
    """Complete feature request analysis."""
    
    total_requests: int = Field(description="Total requests analyzed")
    analysis_period: str = Field(description="Time period")
    clusters: list[FeatureCluster] = Field(description="Themed clusters")
    prioritized_features: list[PrioritizedFeature] = Field(description="Priority ranked features")
    trends: list[TrendAnalysis] = Field(description="Emerging trends")
    competitive_gaps: list[str] = Field(description="Features competitors have")
    churn_risk_features: list[str] = Field(description="Features causing churn")
    quick_wins: list[str] = Field(description="Low effort, high impact")
    roadmap_recommendations: list[str] = Field(description="Strategic recommendations")
    executive_summary: str = Field(description="Summary for leadership")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Feature Request Aggregator agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for feature request analysis
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Feature Request Aggregator",
        instructions=[
            "You are a product manager specializing in customer feedback analysis.",
            "Aggregate and prioritize feature requests for product roadmap planning.",
            "",
            "Prioritization Framework (RICE):",
            "- Reach: How many customers affected",
            "- Impact: How much it helps (3=massive, 2=high, 1=medium, 0.5=low)",
            "- Confidence: How sure are we (100%/80%/50%)",
            "- Effort: Person-months required",
            "- RICE Score = (Reach × Impact × Confidence) / Effort",
            "",
            "Priority Factors:",
            "- Request volume (raw count)",
            "- Customer tier weight (Enterprise > Pro > Free)",
            "- Revenue impact (lost deals, churn risk)",
            "- Competitive pressure",
            "- Strategic alignment",
            "",
            "Clustering Approach:",
            "- Group similar requests by theme",
            "- Identify underlying needs vs. specific solutions",
            "- Look for patterns across segments",
            "",
            "Focus on actionable roadmap recommendations.",
        ],
        output_schema=FeatureRequestReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of feature request analysis."""
    print("\n" + "=" * 60)
    print("  Feature Request Aggregator - Demo")
    print("=" * 60)
    
    requests = config.get("requests", DEFAULT_CONFIG["requests"])
    
    query = f"""
    Analyze these feature requests:
    
    {requests}
    
    Cluster similar requests, prioritize using RICE framework,
    and provide roadmap recommendations.
    """
    
    print("\nAnalyzing feature requests...")
    print("-" * 40)
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, FeatureRequestReport):
        print(f"\n{'='*50}")
        print(f"FEATURE REQUEST ANALYSIS")
        print(f"{'='*50}")
        
        print(f"\n📊 Overview:")
        print(f"  Period: {result.analysis_period}")
        print(f"  Total Requests: {result.total_requests}")
        
        print(f"\n📦 Clusters:")
        for cluster in result.clusters[:4]:
            print(f"\n  {cluster.cluster_name} ({cluster.requests_count} requests)")
            print(f"    Segments: {', '.join(cluster.customer_segments)}")
            print(f"    Revenue Impact: {cluster.revenue_impact}")
        
        print(f"\n🎯 Priority Ranking:")
        for i, feat in enumerate(result.prioritized_features[:5], 1):
            print(f"\n  {i}. {feat.feature}")
            print(f"     Score: {feat.priority_score}/100 | RICE: {feat.rice_score:.1f}")
            print(f"     Requests: {feat.request_count} | Revenue Risk: {feat.revenue_at_risk}")
            print(f"     Effort: {feat.effort_estimate}")
            print(f"     Rationale: {feat.rationale}")
        
        print(f"\n📈 Trends:")
        for trend in result.trends[:3]:
            arrow = "↑" if trend.direction == "growing" else "↓" if trend.direction == "declining" else "→"
            comp = " 🏁" if trend.competitive_pressure else ""
            print(f"  {arrow} {trend.trend} ({trend.direction}){comp}")
            print(f"    Driver: {trend.driver}")
        
        if result.competitive_gaps:
            print(f"\n🏁 Competitive Gaps:")
            for gap in result.competitive_gaps[:3]:
                print(f"  • {gap}")
        
        if result.churn_risk_features:
            print(f"\n⚠️ Churn Risk Features:")
            for feat in result.churn_risk_features[:3]:
                print(f"  • {feat}")
        
        print(f"\n⚡ Quick Wins:")
        for win in result.quick_wins[:3]:
            print(f"  • {win}")
        
        print(f"\n🗺️ Roadmap Recommendations:")
        for rec in result.roadmap_recommendations[:4]:
            print(f"  • {rec}")
        
        print(f"\n📋 Executive Summary:")
        print(f"  {result.executive_summary}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Feature Request Aggregator - Prioritize product backlog"
    )
    
    parser.add_argument(
        "--requests", "-r",
        type=str,
        default=DEFAULT_CONFIG["requests"],
        help="Feature requests data"
    )
    
    args = parser.parse_args()
    
    config = {
        "requests": args.requests,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
