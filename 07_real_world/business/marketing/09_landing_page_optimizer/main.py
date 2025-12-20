"""
Example #019: Landing Page Optimizer
Category: business/marketing

DESCRIPTION:
Analyzes and optimizes landing page copy for conversions. Reviews headlines,
CTAs, value propositions, and overall messaging. Provides specific
improvement suggestions based on conversion rate optimization best practices.

PATTERNS:
- Knowledge (CRO best practices)
- Structured Output (LandingPageAnalysis with improvements)

ARGUMENTS:
- page_content (str): Landing page copy. Default: sample page
- goal (str): Conversion goal. Default: "sign up for free trial"
- audience (str): Target audience. Default: "small business owners"
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
    "page_content": """
    # Transform Your Business with AI
    
    Our AI platform helps businesses automate repetitive tasks.
    
    ## Features
    - Easy to use
    - Affordable pricing
    - Great support
    
    ## Pricing
    Starting at $49/month
    
    [Start Free Trial]
    
    Join thousands of happy customers.
    """,
    "goal": "sign up for free trial",
    "audience": "small business owners",
}


# =============================================================================
# Output Schema
# =============================================================================

class ElementAnalysis(BaseModel):
    """Analysis of a page element."""
    
    element: str = Field(description="Element type (headline, CTA, etc.)")
    current_text: str = Field(description="Current text")
    score: int = Field(ge=0, le=100, description="Effectiveness score")
    issues: list[str] = Field(description="Problems identified")
    improvements: list[str] = Field(description="Specific improvements")
    rewrite: str = Field(description="Suggested rewrite")


class ValuePropositionAnalysis(BaseModel):
    """Value proposition assessment."""
    
    clarity_score: int = Field(description="How clear is the value prop")
    uniqueness_score: int = Field(description="How differentiated")
    relevance_score: int = Field(description="How relevant to audience")
    current_value_prop: str = Field(description="Identified value proposition")
    improved_value_prop: str = Field(description="Suggested improvement")


class ABTestSuggestion(BaseModel):
    """A/B test recommendation."""
    
    element: str = Field(description="Element to test")
    control: str = Field(description="Current version")
    variant: str = Field(description="Test version")
    hypothesis: str = Field(description="Expected impact")
    priority: str = Field(description="high/medium/low")


class LandingPageAnalysis(BaseModel):
    """Complete landing page optimization report."""
    
    overall_score: int = Field(ge=0, le=100, description="Overall effectiveness")
    conversion_goal: str = Field(description="Target conversion")
    target_audience: str = Field(description="Target audience")
    element_analysis: list[ElementAnalysis] = Field(description="Per-element analysis")
    value_proposition: ValuePropositionAnalysis = Field(description="Value prop assessment")
    messaging_gaps: list[str] = Field(description="Missing messaging elements")
    trust_elements: list[str] = Field(description="Trust signals present/missing")
    urgency_assessment: str = Field(description="Urgency/scarcity evaluation")
    ab_tests: list[ABTestSuggestion] = Field(description="A/B test recommendations")
    quick_wins: list[str] = Field(description="Easy high-impact changes")
    full_rewrite: str = Field(description="Optimized page copy")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Landing Page Optimizer agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for landing page optimization
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Landing Page Optimizer",
        instructions=[
            "You are an expert conversion rate optimizer specializing in landing pages.",
            "Analyze page copy and provide specific, actionable improvements.",
            "",
            f"Conversion Goal: {cfg['goal']}",
            f"Target Audience: {cfg['audience']}",
            "",
            "Key Landing Page Elements:",
            "1. Headline: Clear, benefit-focused, attention-grabbing",
            "2. Subheadline: Supports headline, adds context",
            "3. Value Proposition: Why should they care? What's unique?",
            "4. Benefits: How will their life improve?",
            "5. Social Proof: Testimonials, logos, numbers",
            "6. CTA: Clear, action-oriented, stands out",
            "7. Trust Signals: Security badges, guarantees",
            "",
            "Conversion Copywriting Principles:",
            "- Speak to pain points, then solutions",
            "- Use 'you' more than 'we'",
            "- Be specific (numbers, outcomes)",
            "- Create urgency without manipulation",
            "- Remove friction and objections",
            "- One goal per page",
            "",
            "Analysis Framework:",
            "- Clarity: Is it immediately clear what's offered?",
            "- Relevance: Does it speak to the audience?",
            "- Value: Is the benefit compelling?",
            "- Anxiety: What might make them hesitate?",
            "- Distraction: Is there unnecessary content?",
        ],
        output_schema=LandingPageAnalysis,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of landing page optimization."""
    print("\n" + "=" * 60)
    print("  Landing Page Optimizer - Demo")
    print("=" * 60)
    
    content = config.get("page_content", DEFAULT_CONFIG["page_content"])
    goal = config.get("goal", DEFAULT_CONFIG["goal"])
    audience = config.get("audience", DEFAULT_CONFIG["audience"])
    
    query = f"""
    Analyze this landing page for conversion optimization:
    
    Conversion Goal: {goal}
    Target Audience: {audience}
    
    Page Content:
    ---
    {content}
    ---
    
    Provide:
    1. Overall score and element-by-element analysis
    2. Value proposition assessment
    3. Missing elements and trust signals
    4. A/B test recommendations
    5. Complete optimized rewrite
    """
    
    print(f"\nGoal: {goal}")
    print(f"Audience: {audience}")
    print("-" * 40)
    print("Analyzing landing page...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, LandingPageAnalysis):
        print(f"\n{'='*50}")
        print(f"LANDING PAGE SCORE: {result.overall_score}/100")
        print(f"{'='*50}")
        
        print(f"\nGoal: {result.conversion_goal}")
        print(f"Audience: {result.target_audience}")
        
        print(f"\n📝 Element Analysis:")
        for elem in result.element_analysis:
            print(f"\n  {elem.element.upper()} (Score: {elem.score}/100)")
            print(f"    Current: \"{elem.current_text[:50]}...\"")
            if elem.issues:
                print(f"    Issues: {', '.join(elem.issues[:2])}")
            print(f"    Rewrite: \"{elem.rewrite[:60]}...\"")
        
        vp = result.value_proposition
        print(f"\n💡 Value Proposition:")
        print(f"  Clarity: {vp.clarity_score}/100 | Unique: {vp.uniqueness_score}/100 | Relevant: {vp.relevance_score}/100")
        print(f"  Current: {vp.current_value_prop}")
        print(f"  Improved: {vp.improved_value_prop}")
        
        print(f"\n⚠️  Messaging Gaps:")
        for gap in result.messaging_gaps[:3]:
            print(f"  • {gap}")
        
        print(f"\n🛡️  Trust Elements:")
        for trust in result.trust_elements[:3]:
            print(f"  • {trust}")
        
        print(f"\n⏰ Urgency: {result.urgency_assessment}")
        
        print(f"\n🧪 A/B Test Recommendations:")
        for test in result.ab_tests[:3]:
            print(f"\n  [{test.priority.upper()}] {test.element}")
            print(f"    Control: \"{test.control[:40]}...\"")
            print(f"    Variant: \"{test.variant[:40]}...\"")
            print(f"    Hypothesis: {test.hypothesis}")
        
        print(f"\n⚡ Quick Wins:")
        for win in result.quick_wins[:4]:
            print(f"  • {win}")
        
        print(f"\n📄 OPTIMIZED REWRITE:")
        print("-" * 40)
        print(result.full_rewrite)
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Landing Page Optimizer - Improve conversion copy"
    )
    
    parser.add_argument(
        "--content", "-c",
        type=str,
        default=DEFAULT_CONFIG["page_content"],
        help="Landing page content"
    )
    parser.add_argument(
        "--goal", "-g",
        type=str,
        default=DEFAULT_CONFIG["goal"],
        help=f"Conversion goal (default: {DEFAULT_CONFIG['goal']})"
    )
    parser.add_argument(
        "--audience", "-a",
        type=str,
        default=DEFAULT_CONFIG["audience"],
        help=f"Target audience (default: {DEFAULT_CONFIG['audience']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "page_content": args.content,
        "goal": args.goal,
        "audience": args.audience,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
