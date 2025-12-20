"""
Example #020: Hashtag Researcher
Category: business/marketing

DESCRIPTION:
Researches and recommends hashtags for social media posts. Analyzes trending
tags, relevance scores, competition levels, and suggests optimal hashtag
combinations for maximum reach and engagement.

PATTERNS:
- Tools (web search for trending hashtags)
- Structured Output (HashtagReport with recommendations)

ARGUMENTS:
- topic (str): Content topic. Default: "artificial intelligence"
- platform (str): Target platform. Default: "instagram"
- niche (str): Industry niche. Default: "tech startups"
- post_type (str): Type of post. Default: "educational"
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
    "topic": "artificial intelligence",
    "platform": "instagram",
    "niche": "tech startups",
    "post_type": "educational",
}


# =============================================================================
# Output Schema
# =============================================================================

class HashtagAnalysis(BaseModel):
    """Individual hashtag analysis."""
    
    hashtag: str = Field(description="The hashtag (without #)")
    post_volume: str = Field(description="Estimated posts using this tag")
    competition: str = Field(description="high/medium/low competition")
    relevance_score: int = Field(ge=0, le=100, description="Relevance to topic 0-100")
    trending: bool = Field(description="Currently trending")
    recommended_for: str = Field(description="Best use case for this hashtag")


class HashtagSet(BaseModel):
    """Curated hashtag combination."""
    
    set_name: str = Field(description="Name for this set")
    hashtags: list[str] = Field(description="Hashtags in this set")
    total_count: int = Field(description="Number of hashtags")
    strategy: str = Field(description="Mix strategy explanation")
    expected_reach: str = Field(description="Expected reach level")
    best_for: str = Field(description="Best post type for this set")


class TrendingInsight(BaseModel):
    """Trending hashtag insight."""
    
    hashtag: str = Field(description="Trending hashtag")
    trend_reason: str = Field(description="Why it's trending")
    relevance: str = Field(description="How relevant to your niche")
    timing: str = Field(description="When to use (now/soon/avoid)")


class HashtagReport(BaseModel):
    """Complete hashtag research report."""
    
    topic: str = Field(description="Research topic")
    platform: str = Field(description="Target platform")
    platform_limits: str = Field(description="Platform hashtag limits/best practices")
    primary_hashtags: list[HashtagAnalysis] = Field(description="Core topic hashtags")
    niche_hashtags: list[HashtagAnalysis] = Field(description="Niche-specific hashtags")
    community_hashtags: list[HashtagAnalysis] = Field(description="Community/engagement hashtags")
    trending_insights: list[TrendingInsight] = Field(description="Trending hashtag opportunities")
    recommended_sets: list[HashtagSet] = Field(description="Curated hashtag combinations")
    banned_hashtags: list[str] = Field(description="Hashtags to avoid")
    best_practices: list[str] = Field(description="Platform-specific tips")
    copy_paste_ready: str = Field(description="Ready-to-use hashtag string")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Hashtag Researcher agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for hashtag research
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    platform_guides = {
        "instagram": "30 max (optimal: 5-15), mix of big/medium/small, in caption or first comment",
        "twitter": "1-3 hashtags max, integrated in tweet, trending tags important",
        "linkedin": "3-5 hashtags, professional tags, industry-specific",
        "tiktok": "3-5 hashtags, trending sounds matter more, niche tags work well",
    }
    
    platform = cfg.get("platform", "instagram")
    
    return Agent(
        model=model or default_model(),
        name="Hashtag Researcher",
        instructions=[
            "You are an expert social media strategist specializing in hashtag optimization.",
            "Research and recommend hashtags for maximum reach and engagement.",
            "",
            f"Topic: {cfg['topic']}",
            f"Platform: {platform}",
            f"Niche: {cfg['niche']}",
            f"Post Type: {cfg['post_type']}",
            "",
            f"Platform Guide ({platform}):",
            platform_guides.get(platform, platform_guides["instagram"]),
            "",
            "Hashtag Strategy (30-30-30-10 rule for Instagram):",
            "- 30% High volume (1M+ posts) - broad reach",
            "- 30% Medium volume (100K-1M) - targeted reach",
            "- 30% Low volume (<100K) - niche, less competition",
            "- 10% Branded/community - engagement focused",
            "",
            "Research Approach:",
            "1. Search for trending hashtags in the topic/niche",
            "2. Analyze competition levels",
            "3. Find niche-specific community tags",
            "4. Identify banned or shadowbanned hashtags to avoid",
            "5. Create balanced hashtag sets",
            "",
            "Quality Indicators:",
            "- Relevant to content (not just popular)",
            "- Appropriate competition level",
            "- Active community engagement",
            "- Not overused or spammy",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=HashtagReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of hashtag research."""
    print("\n" + "=" * 60)
    print("  Hashtag Researcher - Demo")
    print("=" * 60)
    
    topic = config.get("topic", DEFAULT_CONFIG["topic"])
    platform = config.get("platform", DEFAULT_CONFIG["platform"])
    niche = config.get("niche", DEFAULT_CONFIG["niche"])
    post_type = config.get("post_type", DEFAULT_CONFIG["post_type"])
    
    query = f"""
    Research hashtags for:
    
    Topic: {topic}
    Platform: {platform}
    Niche: {niche}
    Post Type: {post_type}
    
    1. Search for trending and popular hashtags related to {topic}
    2. Find niche-specific tags for {niche}
    3. Identify community and engagement hashtags
    4. Check for any banned or problematic hashtags
    5. Create optimized hashtag sets with different strategies
    """
    
    print(f"\nTopic: {topic}")
    print(f"Platform: {platform}")
    print(f"Niche: {niche}")
    print("-" * 40)
    print("Researching hashtags...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, HashtagReport):
        print(f"\n{'='*50}")
        print(f"HASHTAG REPORT: {result.topic}")
        print(f"{'='*50}")
        
        print(f"\nPlatform: {result.platform}")
        print(f"Limits: {result.platform_limits}")
        
        print(f"\n🏷️  Primary Hashtags:")
        for h in result.primary_hashtags[:5]:
            trend = "🔥" if h.trending else ""
            print(f"  #{h.hashtag} {trend}")
            print(f"    Volume: {h.post_volume} | Competition: {h.competition} | Relevance: {h.relevance_score}/100")
        
        print(f"\n🎯 Niche Hashtags:")
        for h in result.niche_hashtags[:5]:
            print(f"  #{h.hashtag} - {h.recommended_for}")
        
        print(f"\n👥 Community Hashtags:")
        for h in result.community_hashtags[:5]:
            print(f"  #{h.hashtag}")
        
        if result.trending_insights:
            print(f"\n📈 Trending Insights:")
            for t in result.trending_insights[:3]:
                print(f"  #{t.hashtag} - {t.trend_reason}")
                print(f"    Relevance: {t.relevance} | Timing: {t.timing}")
        
        print(f"\n📦 Recommended Sets:")
        for s in result.recommended_sets:
            print(f"\n  {s.set_name} ({s.total_count} tags)")
            print(f"    Strategy: {s.strategy}")
            print(f"    Reach: {s.expected_reach}")
            print(f"    Best for: {s.best_for}")
            print(f"    Tags: {' '.join(['#' + h for h in s.hashtags[:8]])}...")
        
        if result.banned_hashtags:
            print(f"\n⚠️  Avoid These: {', '.join(['#' + h for h in result.banned_hashtags[:5]])}")
        
        print(f"\n💡 Best Practices:")
        for tip in result.best_practices[:3]:
            print(f"  • {tip}")
        
        print(f"\n📋 COPY-PASTE READY:")
        print("-" * 40)
        print(result.copy_paste_ready)
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Hashtag Researcher - Find optimal hashtags for reach"
    )
    
    parser.add_argument(
        "--topic", "-t",
        type=str,
        default=DEFAULT_CONFIG["topic"],
        help=f"Content topic (default: {DEFAULT_CONFIG['topic']})"
    )
    parser.add_argument(
        "--platform", "-p",
        type=str,
        choices=["instagram", "twitter", "linkedin", "tiktok"],
        default=DEFAULT_CONFIG["platform"],
        help=f"Target platform (default: {DEFAULT_CONFIG['platform']})"
    )
    parser.add_argument(
        "--niche", "-n",
        type=str,
        default=DEFAULT_CONFIG["niche"],
        help=f"Industry niche (default: {DEFAULT_CONFIG['niche']})"
    )
    parser.add_argument(
        "--post-type",
        type=str,
        default=DEFAULT_CONFIG["post_type"],
        help=f"Post type (default: {DEFAULT_CONFIG['post_type']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "topic": args.topic,
        "platform": args.platform,
        "niche": args.niche,
        "post_type": args.post_type,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
