"""
Example #011: Social Media Manager
Category: business/marketing

DESCRIPTION:
Creates, schedules, and analyzes social media content across platforms.
Drafts platform-specific posts, suggests optimal posting times, and tracks
engagement patterns. Uses team workflows for content creation and approval.

PATTERNS:
- Teams (content creator + editor + analyst)
- Workflows (draft → review → schedule)
- Structured Output (PostPlan with scheduling)

ARGUMENTS:
- brand_name (str): Brand/company name. Default: "TechCo"
- platforms (str): Target platforms. Default: "twitter,linkedin"
- topic (str): Content topic. Default: "AI productivity tips"
- tone (str): Brand voice. Default: "professional but friendly"
"""

import argparse
from datetime import datetime
from typing import Optional

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, Field


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG = {
    "brand_name": "TechCo",
    "platforms": "twitter,linkedin",
    "topic": "AI productivity tips",
    "tone": "professional but friendly",
}


# =============================================================================
# Output Schema
# =============================================================================

class SocialPost(BaseModel):
    """Individual social media post."""
    
    platform: str = Field(description="Platform (twitter/linkedin/instagram/facebook)")
    content: str = Field(description="Post content with appropriate length")
    hashtags: list[str] = Field(default_factory=list, description="Relevant hashtags")
    suggested_time: str = Field(description="Optimal posting time (e.g., 'Tuesday 10am EST')")
    media_suggestion: Optional[str] = Field(default=None, description="Suggested image/video type")
    character_count: int = Field(description="Character count of content")


class EngagementPrediction(BaseModel):
    """Predicted engagement for post."""
    
    estimated_reach: str = Field(description="Estimated reach range (e.g., '1K-5K')")
    engagement_rate: str = Field(description="Expected engagement rate (e.g., '2-4%')")
    confidence: str = Field(description="Prediction confidence (high/medium/low)")


class PostPlan(BaseModel):
    """Complete social media posting plan."""
    
    campaign_theme: str = Field(description="Overarching theme or campaign name")
    posts: list[SocialPost] = Field(description="Platform-specific posts")
    engagement_predictions: list[EngagementPrediction] = Field(description="Per-post predictions")
    content_calendar_note: str = Field(description="Where this fits in content calendar")
    a_b_test_suggestion: Optional[str] = Field(default=None, description="A/B test idea for this content")
    best_practices_applied: list[str] = Field(description="Platform best practices used")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Social Media Manager agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for social media management
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    platforms = cfg["platforms"].split(",")
    
    return Agent(
        model=model or default_model(),
        name="Social Media Manager",
        instructions=[
            "You are an expert social media manager for B2B tech brands.",
            "Create engaging, platform-optimized content that drives engagement.",
            "",
            f"Brand: {cfg['brand_name']}",
            f"Tone: {cfg['tone']}",
            f"Target Platforms: {', '.join(platforms)}",
            "",
            "Platform Guidelines:",
            "- Twitter/X: 280 chars max, punchy, hashtags at end, threads for long content",
            "- LinkedIn: Professional, 1300 chars optimal, insights-focused, minimal hashtags",
            "- Instagram: Visual-first, storytelling, 2200 chars max, hashtags in first comment",
            "- Facebook: Conversational, questions to drive engagement, 80 chars ideal for shares",
            "",
            "Posting Time Best Practices:",
            "- LinkedIn: Tuesday-Thursday, 8-10am or 12pm local time",
            "- Twitter: Weekdays 8-10am, lunch hour, or 7-9pm",
            "- Instagram: Monday-Friday 11am-1pm, or 7-9pm",
            "",
            "Always research current trends related to the topic before creating content.",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=PostPlan,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of social media content creation."""
    print("\n" + "=" * 60)
    print("  Social Media Manager - Demo")
    print("=" * 60)
    
    brand = config.get("brand_name", DEFAULT_CONFIG["brand_name"])
    platforms = config.get("platforms", DEFAULT_CONFIG["platforms"])
    topic = config.get("topic", DEFAULT_CONFIG["topic"])
    tone = config.get("tone", DEFAULT_CONFIG["tone"])
    
    query = f"""
    Create a social media content plan for {brand}:
    
    Topic: {topic}
    Platforms: {platforms}
    Tone: {tone}
    
    1. Research current trends related to the topic
    2. Create platform-optimized posts for each platform
    3. Suggest optimal posting times
    4. Predict engagement and suggest A/B tests
    """
    
    print(f"\nBrand: {brand}")
    print(f"Topic: {topic}")
    print(f"Platforms: {platforms}")
    print("-" * 40)
    print("Creating content plan...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, PostPlan):
        print(f"\n{'='*50}")
        print(f"CAMPAIGN: {result.campaign_theme}")
        print(f"{'='*50}")
        
        for i, post in enumerate(result.posts, 1):
            print(f"\n--- Post {i}: {post.platform.upper()} ---")
            print(f"Content ({post.character_count} chars):")
            print(f"  {post.content}")
            if post.hashtags:
                print(f"Hashtags: {' '.join(['#' + h for h in post.hashtags])}")
            print(f"Best Time: {post.suggested_time}")
            if post.media_suggestion:
                print(f"Media: {post.media_suggestion}")
            
            if i <= len(result.engagement_predictions):
                pred = result.engagement_predictions[i-1]
                print(f"Expected: {pred.estimated_reach} reach, {pred.engagement_rate} engagement ({pred.confidence} confidence)")
        
        print(f"\n📅 Calendar Note: {result.content_calendar_note}")
        
        if result.a_b_test_suggestion:
            print(f"\n🧪 A/B Test Idea: {result.a_b_test_suggestion}")
        
        print(f"\n✅ Best Practices Applied:")
        for practice in result.best_practices_applied:
            print(f"  • {practice}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Social Media Manager - Create platform-optimized social content"
    )
    
    parser.add_argument(
        "--brand", "-b",
        type=str,
        default=DEFAULT_CONFIG["brand_name"],
        help=f"Brand name (default: {DEFAULT_CONFIG['brand_name']})"
    )
    parser.add_argument(
        "--platforms", "-p",
        type=str,
        default=DEFAULT_CONFIG["platforms"],
        help=f"Comma-separated platforms (default: {DEFAULT_CONFIG['platforms']})"
    )
    parser.add_argument(
        "--topic", "-t",
        type=str,
        default=DEFAULT_CONFIG["topic"],
        help=f"Content topic (default: {DEFAULT_CONFIG['topic']})"
    )
    parser.add_argument(
        "--tone",
        type=str,
        default=DEFAULT_CONFIG["tone"],
        help=f"Brand voice/tone (default: {DEFAULT_CONFIG['tone']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "brand_name": args.brand,
        "platforms": args.platforms,
        "topic": args.topic,
        "tone": args.tone,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
