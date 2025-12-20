"""
Example #016: Brand Sentiment Monitor
Category: business/marketing

DESCRIPTION:
Monitors brand mentions and sentiment across social media and web. Detects
trends, identifies potential PR issues, and provides real-time brand health
insights. Alerts on significant sentiment shifts.

PATTERNS:
- Tools (web search for brand mentions)
- Knowledge (sentiment analysis best practices)
- Structured Output (SentimentReport with alerts)

ARGUMENTS:
- brand_name (str): Brand to monitor. Default: "TechCorp"
- competitors (str): Competitor brands. Default: "CompA,CompB"
- keywords (str): Additional keywords. Default: "product,service"
- alert_threshold (int): Sentiment drop alert threshold. Default: 20
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
    "brand_name": "TechCorp",
    "competitors": "CompA,CompB",
    "keywords": "product,service,customer support",
    "alert_threshold": 20,
}


# =============================================================================
# Output Schema
# =============================================================================

class SentimentBreakdown(BaseModel):
    """Sentiment distribution."""
    
    positive_pct: float = Field(description="Percentage positive")
    neutral_pct: float = Field(description="Percentage neutral")
    negative_pct: float = Field(description="Percentage negative")
    overall_score: int = Field(ge=-100, le=100, description="Overall sentiment score")


class MentionSample(BaseModel):
    """Sample brand mention."""
    
    source: str = Field(description="Source (Twitter, Reddit, news, etc.)")
    text: str = Field(description="Mention text or summary")
    sentiment: str = Field(description="positive/neutral/negative")
    reach: str = Field(description="Estimated reach")
    urgency: str = Field(description="high/medium/low - needs response?")


class TrendAnalysis(BaseModel):
    """Trend in mentions or sentiment."""
    
    trend_name: str = Field(description="What's trending")
    direction: str = Field(description="increasing/decreasing/stable")
    driver: str = Field(description="What's causing this trend")
    impact: str = Field(description="Business impact assessment")


class CompetitorComparison(BaseModel):
    """Competitor sentiment comparison."""
    
    competitor: str = Field(description="Competitor name")
    sentiment_score: int = Field(description="Their sentiment score")
    share_of_voice: str = Field(description="Share of voice percentage")
    key_themes: list[str] = Field(description="What people say about them")


class Alert(BaseModel):
    """Urgent alert for attention."""
    
    severity: str = Field(description="critical/warning/info")
    title: str = Field(description="Alert title")
    description: str = Field(description="What's happening")
    recommended_action: str = Field(description="What to do")


class SentimentReport(BaseModel):
    """Complete brand sentiment analysis."""
    
    brand: str = Field(description="Brand analyzed")
    analysis_period: str = Field(description="Time period analyzed")
    sentiment: SentimentBreakdown = Field(description="Sentiment breakdown")
    mention_volume: str = Field(description="Total mentions found")
    key_mentions: list[MentionSample] = Field(description="Notable mentions")
    trends: list[TrendAnalysis] = Field(description="Identified trends")
    competitor_comparison: list[CompetitorComparison] = Field(description="Competitor analysis")
    top_themes: list[str] = Field(description="Most discussed topics")
    alerts: list[Alert] = Field(description="Items needing attention")
    recommendations: list[str] = Field(description="Action recommendations")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Brand Sentiment Monitor agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for sentiment monitoring
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Brand Sentiment Monitor",
        instructions=[
            "You are an expert brand monitoring and sentiment analysis specialist.",
            "Monitor brand mentions and provide actionable sentiment insights.",
            "",
            f"Brand: {cfg['brand_name']}",
            f"Competitors: {cfg['competitors']}",
            f"Keywords: {cfg['keywords']}",
            f"Alert Threshold: {cfg['alert_threshold']}% drop triggers alert",
            "",
            "Sentiment Analysis Approach:",
            "- Positive: Praise, recommendations, satisfaction",
            "- Neutral: Informational, objective mentions",
            "- Negative: Complaints, criticism, frustration",
            "",
            "Monitoring Sources:",
            "- Social media (Twitter/X, LinkedIn, Reddit)",
            "- News articles and blogs",
            "- Review sites",
            "- Forums and communities",
            "",
            "Priority Assessment:",
            "- High urgency: Viral negative content, influencer complaints",
            "- Medium urgency: Multiple complaints on same issue",
            "- Low urgency: Isolated negative mentions",
            "",
            "Search for recent brand mentions and analyze sentiment patterns.",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=SentimentReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of sentiment monitoring."""
    print("\n" + "=" * 60)
    print("  Brand Sentiment Monitor - Demo")
    print("=" * 60)
    
    brand = config.get("brand_name", DEFAULT_CONFIG["brand_name"])
    competitors = config.get("competitors", DEFAULT_CONFIG["competitors"])
    keywords = config.get("keywords", DEFAULT_CONFIG["keywords"])
    
    query = f"""
    Monitor brand sentiment for: {brand}
    
    Additional keywords: {keywords}
    Competitors to compare: {competitors}
    
    1. Search for recent mentions of {brand}
    2. Analyze sentiment distribution
    3. Identify key themes and trends
    4. Compare against competitors
    5. Flag any urgent issues requiring attention
    """
    
    print(f"\nBrand: {brand}")
    print(f"Competitors: {competitors}")
    print("-" * 40)
    print("Scanning for brand mentions...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, SentimentReport):
        print(f"\n{'='*50}")
        print(f"SENTIMENT REPORT: {result.brand}")
        print(f"{'='*50}")
        
        print(f"\n📊 Period: {result.analysis_period}")
        print(f"📢 Mentions: {result.mention_volume}")
        
        s = result.sentiment
        print(f"\n😊 Sentiment Breakdown:")
        print(f"  Positive: {s.positive_pct:.1f}%")
        print(f"  Neutral: {s.neutral_pct:.1f}%")
        print(f"  Negative: {s.negative_pct:.1f}%")
        print(f"  Overall Score: {s.overall_score}/100")
        
        if result.alerts:
            print(f"\n🚨 ALERTS:")
            for alert in result.alerts:
                icon = "🔴" if alert.severity == "critical" else "🟡" if alert.severity == "warning" else "🔵"
                print(f"  {icon} [{alert.severity.upper()}] {alert.title}")
                print(f"     {alert.description}")
                print(f"     → {alert.recommended_action}")
        
        print(f"\n📝 Key Mentions:")
        for mention in result.key_mentions[:3]:
            emoji = "👍" if mention.sentiment == "positive" else "👎" if mention.sentiment == "negative" else "➖"
            print(f"  {emoji} [{mention.source}] {mention.text[:80]}...")
            print(f"     Reach: {mention.reach} | Urgency: {mention.urgency}")
        
        print(f"\n📈 Trends:")
        for trend in result.trends[:3]:
            arrow = "↑" if trend.direction == "increasing" else "↓" if trend.direction == "decreasing" else "→"
            print(f"  {arrow} {trend.trend_name}")
            print(f"    Driver: {trend.driver}")
            print(f"    Impact: {trend.impact}")
        
        print(f"\n🏆 Competitor Comparison:")
        for comp in result.competitor_comparison:
            print(f"  {comp.competitor}: Score {comp.sentiment_score}, SOV {comp.share_of_voice}")
            print(f"    Themes: {', '.join(comp.key_themes[:2])}")
        
        print(f"\n🏷️  Top Themes: {', '.join(result.top_themes[:5])}")
        
        print(f"\n✅ Recommendations:")
        for i, rec in enumerate(result.recommendations[:4], 1):
            print(f"  {i}. {rec}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Brand Sentiment Monitor - Track brand mentions and sentiment"
    )
    
    parser.add_argument(
        "--brand", "-b",
        type=str,
        default=DEFAULT_CONFIG["brand_name"],
        help=f"Brand to monitor (default: {DEFAULT_CONFIG['brand_name']})"
    )
    parser.add_argument(
        "--competitors", "-c",
        type=str,
        default=DEFAULT_CONFIG["competitors"],
        help="Comma-separated competitor names"
    )
    parser.add_argument(
        "--keywords", "-k",
        type=str,
        default=DEFAULT_CONFIG["keywords"],
        help="Additional keywords to track"
    )
    
    args = parser.parse_args()
    
    config = {
        "brand_name": args.brand,
        "competitors": args.competitors,
        "keywords": args.keywords,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
