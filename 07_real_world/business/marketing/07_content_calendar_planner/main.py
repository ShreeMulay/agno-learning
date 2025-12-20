"""
Example #017: Content Calendar Planner
Category: business/marketing

DESCRIPTION:
Creates comprehensive content calendars with themes, topics, and scheduling
across multiple platforms. Balances content types, maintains posting frequency,
and aligns with marketing campaigns and seasonal events.

PATTERNS:
- Memory (track content history to avoid repetition)
- Workflows (planning → drafting → scheduling)
- Structured Output (ContentCalendar with posts)

ARGUMENTS:
- brand (str): Brand name. Default: "TechStartup"
- duration (str): Planning period. Default: "1 month"
- platforms (str): Target platforms. Default: "blog,linkedin,twitter"
- themes (str): Content themes. Default: "product,thought leadership,community"
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
    "brand": "TechStartup",
    "duration": "1 month",
    "platforms": "blog,linkedin,twitter",
    "themes": "product updates,thought leadership,community stories",
    "posting_frequency": "blog: 2x/week, linkedin: 3x/week, twitter: daily",
}


# =============================================================================
# Output Schema
# =============================================================================

class ContentPiece(BaseModel):
    """Individual content piece in the calendar."""
    
    date: str = Field(description="Scheduled date (e.g., 'Week 1 Monday')")
    platform: str = Field(description="Target platform")
    content_type: str = Field(description="Type (blog, post, thread, video, etc.)")
    theme: str = Field(description="Content theme/pillar")
    title: str = Field(description="Working title")
    key_points: list[str] = Field(description="Main points to cover")
    cta: str = Field(description="Call to action")
    assets_needed: list[str] = Field(description="Required images, videos, etc.")
    status: str = Field(default="planned", description="planned/drafted/scheduled/published")


class WeeklyTheme(BaseModel):
    """Weekly content theme."""
    
    week: str = Field(description="Week identifier")
    theme: str = Field(description="Focus theme for the week")
    key_message: str = Field(description="Core message to reinforce")
    tie_in: Optional[str] = Field(default=None, description="Campaign or event tie-in")


class ContentMix(BaseModel):
    """Content type distribution."""
    
    content_type: str = Field(description="Content type")
    percentage: int = Field(description="Percentage of total content")
    purpose: str = Field(description="Why this content type")


class ContentCalendar(BaseModel):
    """Complete content calendar."""
    
    brand: str = Field(description="Brand name")
    period: str = Field(description="Calendar period")
    weekly_themes: list[WeeklyTheme] = Field(description="Theme for each week")
    content_pieces: list[ContentPiece] = Field(description="All scheduled content")
    content_mix: list[ContentMix] = Field(description="Content type distribution")
    key_dates: list[str] = Field(description="Important dates to leverage")
    repurposing_opportunities: list[str] = Field(description="Content repurposing ideas")
    resource_requirements: list[str] = Field(description="Resources needed")
    success_metrics: list[str] = Field(description="KPIs to track")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Content Calendar Planner agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for content calendar planning
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Content Calendar Planner",
        instructions=[
            "You are an expert content strategist who creates comprehensive content calendars.",
            "Plan diverse, engaging content that supports business goals.",
            "",
            f"Brand: {cfg['brand']}",
            f"Duration: {cfg['duration']}",
            f"Platforms: {cfg['platforms']}",
            f"Themes: {cfg['themes']}",
            f"Posting Frequency: {cfg['posting_frequency']}",
            "",
            "Content Planning Principles:",
            "- Balance educational, promotional, and engagement content",
            "- Maintain consistent brand voice across platforms",
            "- Align with audience behavior patterns per platform",
            "- Leave room for reactive/timely content",
            "",
            "Content Mix Guidelines (80/20 rule):",
            "- 80% value-adding content (educational, entertaining, inspiring)",
            "- 20% promotional content (product, sales, CTAs)",
            "",
            "Platform-Specific Notes:",
            "- Blog: Long-form, SEO-focused, evergreen",
            "- LinkedIn: Professional insights, industry trends, thought leadership",
            "- Twitter: Real-time, conversational, thread-worthy insights",
            "- Instagram: Visual storytelling, behind-the-scenes, community",
            "",
            "Create a cohesive calendar with clear themes and actionable content ideas.",
        ],
        output_schema=ContentCalendar,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of content calendar planning."""
    print("\n" + "=" * 60)
    print("  Content Calendar Planner - Demo")
    print("=" * 60)
    
    brand = config.get("brand", DEFAULT_CONFIG["brand"])
    duration = config.get("duration", DEFAULT_CONFIG["duration"])
    platforms = config.get("platforms", DEFAULT_CONFIG["platforms"])
    themes = config.get("themes", DEFAULT_CONFIG["themes"])
    
    query = f"""
    Create a content calendar for:
    
    Brand: {brand}
    Duration: {duration}
    Platforms: {platforms}
    Content Themes: {themes}
    
    Create a comprehensive calendar with:
    1. Weekly themes that build on each other
    2. Specific content pieces for each platform
    3. Balanced content mix
    4. Key dates to leverage
    5. Repurposing opportunities
    """
    
    print(f"\nBrand: {brand}")
    print(f"Duration: {duration}")
    print(f"Platforms: {platforms}")
    print("-" * 40)
    print("Planning content calendar...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, ContentCalendar):
        print(f"\n{'='*50}")
        print(f"CONTENT CALENDAR: {result.brand}")
        print(f"Period: {result.period}")
        print(f"{'='*50}")
        
        print(f"\n📅 Weekly Themes:")
        for wt in result.weekly_themes:
            print(f"\n  {wt.week}: {wt.theme}")
            print(f"    Message: {wt.key_message}")
            if wt.tie_in:
                print(f"    Tie-in: {wt.tie_in}")
        
        print(f"\n📊 Content Mix:")
        for cm in result.content_mix:
            print(f"  {cm.content_type}: {cm.percentage}% - {cm.purpose}")
        
        print(f"\n📝 Content Pieces ({len(result.content_pieces)} total):")
        # Group by week
        for piece in result.content_pieces[:8]:  # Show first 8
            print(f"\n  {piece.date} | {piece.platform.upper()}")
            print(f"    [{piece.content_type}] {piece.title}")
            print(f"    Theme: {piece.theme}")
            print(f"    CTA: {piece.cta}")
            if piece.assets_needed:
                print(f"    Assets: {', '.join(piece.assets_needed[:2])}")
        
        if len(result.content_pieces) > 8:
            print(f"\n  ... and {len(result.content_pieces) - 8} more pieces")
        
        print(f"\n🗓️  Key Dates:")
        for date in result.key_dates[:5]:
            print(f"  • {date}")
        
        print(f"\n♻️  Repurposing Opportunities:")
        for opp in result.repurposing_opportunities[:3]:
            print(f"  • {opp}")
        
        print(f"\n📦 Resources Needed:")
        for res in result.resource_requirements[:4]:
            print(f"  • {res}")
        
        print(f"\n📈 Success Metrics:")
        for metric in result.success_metrics[:4]:
            print(f"  • {metric}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Content Calendar Planner - Create comprehensive content schedules"
    )
    
    parser.add_argument(
        "--brand", "-b",
        type=str,
        default=DEFAULT_CONFIG["brand"],
        help=f"Brand name (default: {DEFAULT_CONFIG['brand']})"
    )
    parser.add_argument(
        "--duration", "-d",
        type=str,
        default=DEFAULT_CONFIG["duration"],
        help=f"Planning period (default: {DEFAULT_CONFIG['duration']})"
    )
    parser.add_argument(
        "--platforms", "-p",
        type=str,
        default=DEFAULT_CONFIG["platforms"],
        help="Comma-separated platforms"
    )
    parser.add_argument(
        "--themes", "-t",
        type=str,
        default=DEFAULT_CONFIG["themes"],
        help="Content themes"
    )
    
    args = parser.parse_args()
    
    config = {
        "brand": args.brand,
        "duration": args.duration,
        "platforms": args.platforms,
        "themes": args.themes,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
