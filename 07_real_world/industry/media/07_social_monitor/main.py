"""
Example #167: Social Monitor Agent
Category: industry/media
DESCRIPTION: Monitors social media mentions and sentiment
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"brand": "TechCorp", "platforms": "twitter, reddit", "timeframe": "24 hours"}

class Mention(BaseModel):
    platform: str = Field(description="Platform")
    content_preview: str = Field(description="Mention preview")
    sentiment: str = Field(description="positive/negative/neutral")
    reach: str = Field(description="Potential reach")
    requires_response: bool = Field(description="Needs response")
    urgency: str = Field(description="high/medium/low urgency")

class SocialMonitorReport(BaseModel):
    brand: str = Field(description="Brand monitored")
    timeframe: str = Field(description="Monitoring period")
    total_mentions: int = Field(description="Total mentions")
    sentiment_breakdown: dict = Field(description="Sentiment percentages")
    key_mentions: list[Mention] = Field(description="Important mentions")
    trending_topics: list[str] = Field(description="Related trending topics")
    competitor_mentions: list[str] = Field(description="Competitor comparisons")
    action_items: list[str] = Field(description="Recommended actions")
    alert_summary: str = Field(description="Alert summary")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Social Monitor",
        instructions=[
            "You are an expert social media monitoring specialist.",
            f"Monitor mentions of {cfg['brand']}",
            f"Focus on {cfg['platforms']} platforms",
            "Analyze sentiment and identify issues",
            "Flag mentions requiring immediate attention",
            "Track competitor comparisons",
        ],
        output_schema=SocialMonitorReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Social Monitor Agent - Demo")
    print("=" * 60)
    query = f"""Monitor social mentions:
- Brand: {config['brand']}
- Platforms: {config['platforms']}
- Timeframe: {config['timeframe']}

Provide sentiment analysis and action items."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SocialMonitorReport):
        print(f"\n🔍 {result.brand} - {result.timeframe}")
        print(f"📊 Total Mentions: {result.total_mentions}")
        sb = result.sentiment_breakdown
        print(f"😊 Sentiment: +{sb.get('positive', 0)}% | ={sb.get('neutral', 0)}% | -{sb.get('negative', 0)}%")
        print(f"\n⚠️ Alert: {result.alert_summary}")
        print(f"\n📌 Key Mentions:")
        for m in result.key_mentions[:3]:
            icon = "🟢" if m.sentiment == "positive" else "🔴" if m.sentiment == "negative" else "⚪"
            print(f"  {icon} [{m.platform}] {m.content_preview[:50]}...")
            if m.requires_response:
                print(f"    ⚡ NEEDS RESPONSE ({m.urgency})")
        print(f"\n✅ Actions:")
        for a in result.action_items[:3]:
            print(f"  • {a}")

def main():
    parser = argparse.ArgumentParser(description="Social Monitor Agent")
    parser.add_argument("--brand", "-b", default=DEFAULT_CONFIG["brand"])
    parser.add_argument("--platforms", "-p", default=DEFAULT_CONFIG["platforms"])
    parser.add_argument("--timeframe", "-t", default=DEFAULT_CONFIG["timeframe"])
    args = parser.parse_args()
    config = {"brand": args.brand, "platforms": args.platforms, "timeframe": args.timeframe}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
