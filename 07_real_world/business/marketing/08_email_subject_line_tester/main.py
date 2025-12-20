"""
Example #018: Email Subject Line Tester
Category: business/marketing

DESCRIPTION:
Generates and evaluates email subject lines for maximum open rates.
Creates A/B test variants, predicts performance, and applies proven
psychological triggers. Analyzes against email marketing best practices.

PATTERNS:
- Structured Output (SubjectLineReport with variants)

ARGUMENTS:
- email_topic (str): Email content topic. Default: "product launch"
- audience (str): Target audience. Default: "B2B tech buyers"
- tone (str): Desired tone. Default: "professional"
- variants (int): Number of variants to generate. Default: 5
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
    "email_topic": "new product launch announcement",
    "audience": "B2B tech decision makers",
    "tone": "professional but engaging",
    "variants": 5,
    "brand": "TechCo",
}


# =============================================================================
# Output Schema
# =============================================================================

class SubjectLineVariant(BaseModel):
    """Individual subject line variant."""
    
    subject_line: str = Field(description="The subject line text")
    preview_text: str = Field(description="Suggested preview text")
    character_count: int = Field(description="Character count")
    word_count: int = Field(description="Word count")
    psychological_trigger: str = Field(description="Primary trigger used")
    predicted_open_rate: str = Field(description="Predicted open rate range")
    best_for: str = Field(description="Best use case for this variant")
    spam_risk: str = Field(description="Spam risk assessment (low/medium/high)")


class SubjectLineAnalysis(BaseModel):
    """Analysis of subject line effectiveness."""
    
    power_words: list[str] = Field(description="Power words used")
    personalization_options: list[str] = Field(description="Personalization suggestions")
    emoji_recommendation: str = Field(description="Emoji usage advice")
    length_assessment: str = Field(description="Length optimization notes")
    mobile_preview: str = Field(description="How it appears on mobile (~40 chars)")


class ABTestPlan(BaseModel):
    """A/B testing plan."""
    
    variant_a: str = Field(description="Control variant")
    variant_b: str = Field(description="Test variant")
    hypothesis: str = Field(description="What we're testing")
    sample_size: str = Field(description="Recommended sample size")
    duration: str = Field(description="Recommended test duration")
    success_metric: str = Field(description="Primary metric to track")


class SubjectLineReport(BaseModel):
    """Complete subject line testing report."""
    
    email_topic: str = Field(description="Email topic")
    target_audience: str = Field(description="Target audience")
    variants: list[SubjectLineVariant] = Field(description="Generated variants")
    top_pick: str = Field(description="Recommended best performer")
    top_pick_reasoning: str = Field(description="Why this is the top pick")
    analysis: SubjectLineAnalysis = Field(description="Detailed analysis")
    ab_test_plan: ABTestPlan = Field(description="Testing plan")
    avoid_list: list[str] = Field(description="Words/phrases to avoid")
    industry_benchmarks: str = Field(description="Industry open rate context")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the Email Subject Line Tester agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for subject line testing
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="Email Subject Line Tester",
        instructions=[
            "You are an expert email marketing specialist focused on open rates.",
            "Create and analyze email subject lines for maximum engagement.",
            "",
            f"Topic: {cfg['email_topic']}",
            f"Audience: {cfg['audience']}",
            f"Tone: {cfg['tone']}",
            f"Brand: {cfg['brand']}",
            "",
            "Subject Line Best Practices:",
            "- Optimal length: 30-50 characters (under 40 for mobile)",
            "- Front-load important words",
            "- Use numbers when relevant (odd numbers perform better)",
            "- Create urgency without being spammy",
            "- Personalization increases opens by 26%",
            "",
            "Psychological Triggers:",
            "- Curiosity: Open loops, questions, teasers",
            "- Urgency: Time-sensitive, limited availability",
            "- Value: Clear benefit statement",
            "- Social Proof: Popularity, testimonials",
            "- Exclusivity: VIP, early access, insider",
            "- Fear of Missing Out (FOMO)",
            "",
            "Spam Triggers to Avoid:",
            "- ALL CAPS, excessive punctuation (!!!)",
            "- Words: free, guarantee, act now, limited time",
            "- Misleading claims or clickbait",
            "",
            "Generate diverse variants using different psychological triggers.",
        ],
        output_schema=SubjectLineReport,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of subject line testing."""
    print("\n" + "=" * 60)
    print("  Email Subject Line Tester - Demo")
    print("=" * 60)
    
    topic = config.get("email_topic", DEFAULT_CONFIG["email_topic"])
    audience = config.get("audience", DEFAULT_CONFIG["audience"])
    tone = config.get("tone", DEFAULT_CONFIG["tone"])
    variants = config.get("variants", DEFAULT_CONFIG["variants"])
    
    query = f"""
    Generate and analyze email subject lines:
    
    Email Topic: {topic}
    Target Audience: {audience}
    Tone: {tone}
    Number of Variants: {variants}
    
    For each variant:
    1. Create the subject line using a different psychological trigger
    2. Suggest preview text
    3. Predict open rate
    4. Assess spam risk
    
    Also provide:
    - Top pick recommendation with reasoning
    - A/B test plan
    - Words to avoid
    """
    
    print(f"\nTopic: {topic}")
    print(f"Audience: {audience}")
    print(f"Tone: {tone}")
    print("-" * 40)
    print("Generating subject line variants...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, SubjectLineReport):
        print(f"\n{'='*50}")
        print(f"SUBJECT LINE REPORT")
        print(f"{'='*50}")
        
        print(f"\nTopic: {result.email_topic}")
        print(f"Audience: {result.target_audience}")
        print(f"Benchmark: {result.industry_benchmarks}")
        
        print(f"\n📧 Generated Variants:")
        for i, v in enumerate(result.variants, 1):
            print(f"\n  {i}. \"{v.subject_line}\"")
            print(f"     Preview: {v.preview_text[:50]}...")
            print(f"     {v.character_count} chars | Trigger: {v.psychological_trigger}")
            print(f"     Predicted: {v.predicted_open_rate} | Spam Risk: {v.spam_risk}")
            print(f"     Best for: {v.best_for}")
        
        print(f"\n⭐ TOP PICK:")
        print(f"   \"{result.top_pick}\"")
        print(f"   {result.top_pick_reasoning}")
        
        a = result.analysis
        print(f"\n📊 Analysis:")
        print(f"  Power Words: {', '.join(a.power_words[:5])}")
        print(f"  Personalization: {', '.join(a.personalization_options[:2])}")
        print(f"  Emoji: {a.emoji_recommendation}")
        print(f"  Length: {a.length_assessment}")
        print(f"  Mobile Preview: \"{a.mobile_preview}\"")
        
        ab = result.ab_test_plan
        print(f"\n🧪 A/B Test Plan:")
        print(f"  A: \"{ab.variant_a}\"")
        print(f"  B: \"{ab.variant_b}\"")
        print(f"  Hypothesis: {ab.hypothesis}")
        print(f"  Sample: {ab.sample_size} | Duration: {ab.duration}")
        
        print(f"\n⚠️  Avoid: {', '.join(result.avoid_list[:5])}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Email Subject Line Tester - Generate and test subject lines"
    )
    
    parser.add_argument(
        "--topic", "-t",
        type=str,
        default=DEFAULT_CONFIG["email_topic"],
        help="Email topic"
    )
    parser.add_argument(
        "--audience", "-a",
        type=str,
        default=DEFAULT_CONFIG["audience"],
        help="Target audience"
    )
    parser.add_argument(
        "--tone",
        type=str,
        default=DEFAULT_CONFIG["tone"],
        help="Desired tone"
    )
    parser.add_argument(
        "--variants", "-n",
        type=int,
        default=DEFAULT_CONFIG["variants"],
        help=f"Number of variants (default: {DEFAULT_CONFIG['variants']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "email_topic": args.topic,
        "audience": args.audience,
        "tone": args.tone,
        "variants": args.variants,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
