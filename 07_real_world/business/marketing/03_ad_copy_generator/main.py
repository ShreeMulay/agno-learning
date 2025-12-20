"""
Example #013: Ad Copy Generator
Category: business/marketing

DESCRIPTION:
Creates high-converting ad copy for multiple platforms (Google Ads, Facebook,
LinkedIn). Generates A/B test variants, respects character limits, and applies
proven copywriting frameworks (AIDA, PAS, etc.).

PATTERNS:
- Structured Output (AdCopyPlan with variants)
- Memory (learn from past campaign performance)

ARGUMENTS:
- product (str): Product or service name. Default: "CloudSync Pro"
- value_prop (str): Main value proposition. Default: "Sync files 10x faster"
- platform (str): Ad platform. Default: "google"
- goal (str): Campaign goal. Default: "signups"
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
    "product": "CloudSync Pro",
    "value_prop": "Sync files 10x faster across all your devices",
    "platform": "google",
    "goal": "signups",
    "target_audience": "small business owners",
}


# =============================================================================
# Output Schema
# =============================================================================

class AdVariant(BaseModel):
    """Single ad copy variant."""
    
    variant_name: str = Field(description="Name for this variant (A, B, C, etc.)")
    headline: str = Field(description="Primary headline")
    headline_2: Optional[str] = Field(default=None, description="Secondary headline if applicable")
    description: str = Field(description="Ad description/body text")
    cta: str = Field(description="Call to action text")
    display_url: Optional[str] = Field(default=None, description="Display URL path")
    framework_used: str = Field(description="Copywriting framework (AIDA/PAS/BAB/etc.)")
    character_counts: dict = Field(description="Character count per element")


class TargetingRecommendation(BaseModel):
    """Ad targeting suggestions."""
    
    keywords: list[str] = Field(description="Target keywords (for search ads)")
    audiences: list[str] = Field(description="Audience targeting suggestions")
    negative_keywords: list[str] = Field(description="Keywords to exclude")


class AdCopyPlan(BaseModel):
    """Complete ad copy generation plan."""
    
    campaign_name: str = Field(description="Suggested campaign name")
    platform: str = Field(description="Target platform")
    goal: str = Field(description="Campaign objective")
    variants: list[AdVariant] = Field(description="Ad copy variants for A/B testing")
    targeting: TargetingRecommendation = Field(description="Targeting recommendations")
    testing_hypothesis: str = Field(description="What we're testing with these variants")
    landing_page_recommendations: list[str] = Field(description="Landing page suggestions")
    budget_allocation: str = Field(description="Suggested budget split for testing")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Ad Copy Generator agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for ad copy generation
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    platform_limits = {
        "google": "Headlines: 30 chars, Description: 90 chars each (up to 4)",
        "facebook": "Primary text: 125 chars, Headline: 40 chars, Description: 30 chars",
        "linkedin": "Intro text: 150 chars, Headline: 70 chars",
        "twitter": "280 chars total",
    }
    
    platform = cfg.get("platform", "google")
    
    return Agent(
        model=model or default_model(),
        name="Ad Copy Generator",
        instructions=[
            "You are an expert performance marketing copywriter.",
            "Create high-converting ad copy that drives action.",
            "",
            f"Product: {cfg['product']}",
            f"Value Proposition: {cfg['value_prop']}",
            f"Target Audience: {cfg['target_audience']}",
            f"Campaign Goal: {cfg['goal']}",
            f"Platform: {platform}",
            "",
            f"Character Limits ({platform}):",
            platform_limits.get(platform, platform_limits["google"]),
            "",
            "Copywriting Frameworks:",
            "- AIDA: Attention → Interest → Desire → Action",
            "- PAS: Problem → Agitation → Solution",
            "- BAB: Before → After → Bridge",
            "- 4Ps: Promise → Picture → Proof → Push",
            "",
            "Best Practices:",
            "- Lead with benefits, not features",
            "- Use power words: Free, New, Proven, Instant, Easy",
            "- Include numbers when possible (10x, 50%, 3 steps)",
            "- Create urgency without being pushy",
            "- Match ad copy to landing page",
            "",
            "Generate 3 distinct variants using different frameworks for A/B testing.",
        ],
        output_schema=AdCopyPlan,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of ad copy generation."""
    print("\n" + "=" * 60)
    print("  Ad Copy Generator - Demo")
    print("=" * 60)
    
    product = config.get("product", DEFAULT_CONFIG["product"])
    value_prop = config.get("value_prop", DEFAULT_CONFIG["value_prop"])
    platform = config.get("platform", DEFAULT_CONFIG["platform"])
    goal = config.get("goal", DEFAULT_CONFIG["goal"])
    audience = config.get("target_audience", DEFAULT_CONFIG["target_audience"])
    
    query = f"""
    Create ad copy for:
    
    Product: {product}
    Value Proposition: {value_prop}
    Platform: {platform}
    Goal: {goal}
    Target Audience: {audience}
    
    Generate 3 variants using different copywriting frameworks.
    Ensure all copy respects platform character limits.
    """
    
    print(f"\nProduct: {product}")
    print(f"Platform: {platform.upper()}")
    print(f"Goal: {goal}")
    print("-" * 40)
    print("Generating ad copy variants...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, AdCopyPlan):
        print(f"\n{'='*50}")
        print(f"CAMPAIGN: {result.campaign_name}")
        print(f"{'='*50}")
        
        for variant in result.variants:
            print(f"\n--- Variant {variant.variant_name} ({variant.framework_used}) ---")
            print(f"Headline: {variant.headline}")
            if variant.headline_2:
                print(f"Headline 2: {variant.headline_2}")
            print(f"Description: {variant.description}")
            print(f"CTA: {variant.cta}")
            if variant.display_url:
                print(f"Display URL: {variant.display_url}")
            print(f"Chars: {variant.character_counts}")
        
        print(f"\n🧪 Testing Hypothesis:")
        print(f"  {result.testing_hypothesis}")
        
        print(f"\n🎯 Targeting Recommendations:")
        print(f"  Keywords: {', '.join(result.targeting.keywords[:5])}")
        print(f"  Audiences: {', '.join(result.targeting.audiences[:3])}")
        if result.targeting.negative_keywords:
            print(f"  Negative Keywords: {', '.join(result.targeting.negative_keywords[:3])}")
        
        print(f"\n📄 Landing Page Tips:")
        for tip in result.landing_page_recommendations[:3]:
            print(f"  • {tip}")
        
        print(f"\n💰 Budget Split: {result.budget_allocation}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Ad Copy Generator - Create high-converting ad copy"
    )
    
    parser.add_argument(
        "--product", "-p",
        type=str,
        default=DEFAULT_CONFIG["product"],
        help=f"Product name (default: {DEFAULT_CONFIG['product']})"
    )
    parser.add_argument(
        "--value-prop", "-v",
        type=str,
        default=DEFAULT_CONFIG["value_prop"],
        help="Main value proposition"
    )
    parser.add_argument(
        "--platform",
        type=str,
        choices=["google", "facebook", "linkedin", "twitter"],
        default=DEFAULT_CONFIG["platform"],
        help=f"Ad platform (default: {DEFAULT_CONFIG['platform']})"
    )
    parser.add_argument(
        "--goal", "-g",
        type=str,
        default=DEFAULT_CONFIG["goal"],
        help=f"Campaign goal (default: {DEFAULT_CONFIG['goal']})"
    )
    parser.add_argument(
        "--audience", "-a",
        type=str,
        default=DEFAULT_CONFIG["target_audience"],
        help=f"Target audience (default: {DEFAULT_CONFIG['target_audience']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "product": args.product,
        "value_prop": args.value_prop,
        "platform": args.platform,
        "goal": args.goal,
        "target_audience": args.audience,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
