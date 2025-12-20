"""
Example #012: SEO Content Optimizer
Category: business/marketing

DESCRIPTION:
Analyzes and optimizes content for search engine rankings. Performs keyword
research, content scoring, and provides actionable suggestions to improve
organic visibility. Compares against top-ranking competitors.

PATTERNS:
- Knowledge (SEO best practices, algorithm updates)
- Tools (web search for competitor analysis)
- Structured Output (SEOAnalysis with improvement suggestions)

ARGUMENTS:
- content (str): Content to analyze. Default: sample article
- target_keyword (str): Primary keyword to rank for. Default: "AI agents"
- competitors (int): Number of competitors to analyze. Default: 3
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
    "content": """AI Agents: The Future of Automation

Artificial intelligence agents are transforming how businesses operate. 
These autonomous systems can handle complex tasks, learn from interactions, 
and make decisions without human intervention. From customer service to 
data analysis, AI agents are becoming essential tools for modern enterprises.

In this article, we explore how AI agents work, their key benefits, and 
how to implement them in your organization.""",
    "target_keyword": "AI agents",
    "competitors": 3,
}


# =============================================================================
# Output Schema
# =============================================================================

class KeywordAnalysis(BaseModel):
    """Analysis of keyword usage."""
    
    primary_keyword: str = Field(description="Target keyword")
    current_density: float = Field(description="Keyword density percentage")
    recommended_density: str = Field(description="Recommended density range")
    lsi_keywords: list[str] = Field(description="Related/LSI keywords to include")
    missing_variations: list[str] = Field(description="Keyword variations not used")


class ContentMetrics(BaseModel):
    """Content quality metrics."""
    
    word_count: int = Field(description="Total word count")
    readability_score: str = Field(description="Flesch-Kincaid or similar grade level")
    heading_structure: str = Field(description="Assessment of H1/H2/H3 usage")
    paragraph_length: str = Field(description="Average paragraph length assessment")
    internal_links_suggestion: int = Field(description="Recommended internal links")
    external_links_suggestion: int = Field(description="Recommended external authority links")


class CompetitorInsight(BaseModel):
    """Insights from competitor analysis."""
    
    source: str = Field(description="Competitor URL or source")
    strengths: list[str] = Field(description="What they do well")
    content_gaps: list[str] = Field(description="Topics they cover that you don't")


class SEOAnalysis(BaseModel):
    """Complete SEO analysis and recommendations."""
    
    overall_score: int = Field(ge=0, le=100, description="SEO score 0-100")
    keyword_analysis: KeywordAnalysis = Field(description="Keyword usage analysis")
    content_metrics: ContentMetrics = Field(description="Content quality metrics")
    competitor_insights: list[CompetitorInsight] = Field(description="Competitor analysis")
    title_suggestions: list[str] = Field(description="Optimized title variations")
    meta_description: str = Field(description="Suggested meta description (155 chars)")
    priority_improvements: list[str] = Field(description="Top 5 improvements by impact")
    quick_wins: list[str] = Field(description="Easy fixes for immediate gains")


# =============================================================================
# Agent Factory
# =============================================================================

def default_model():
    """Get the default model."""
    return OpenRouter(id="anthropic/claude-sonnet-4")


def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    """
    Create the SEO Content Optimizer agent.
    
    Args:
        model: Override default model
        config: Configuration options (see DEFAULT_CONFIG)
    
    Returns:
        Configured Agent for SEO optimization
    """
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    
    return Agent(
        model=model or default_model(),
        name="SEO Content Optimizer",
        instructions=[
            "You are an expert SEO specialist with deep knowledge of search algorithms.",
            "Analyze content for SEO effectiveness and provide actionable improvements.",
            "",
            "SEO Best Practices (2024):",
            "- E-E-A-T: Experience, Expertise, Authoritativeness, Trust",
            "- Keyword density: 1-2% for primary keyword",
            "- Content depth: comprehensive coverage beats thin content",
            "- User intent: match content to search intent (informational/transactional/navigational)",
            "- Mobile-first: content must work on mobile",
            "",
            "Analysis Process:",
            "1. Search for top-ranking pages for the target keyword",
            "2. Analyze competitor content structure and depth",
            "3. Identify content gaps and opportunities",
            "4. Score current content and provide specific improvements",
            "",
            "Focus on high-impact, actionable recommendations.",
        ],
        tools=[DuckDuckGoTools()],
        output_schema=SEOAnalysis,
        use_json_mode=True,
        markdown=True,
    )


# =============================================================================
# Demo / CLI
# =============================================================================

def run_demo(agent: Agent, config: dict):
    """Run a demonstration of SEO analysis."""
    print("\n" + "=" * 60)
    print("  SEO Content Optimizer - Demo")
    print("=" * 60)
    
    content = config.get("content", DEFAULT_CONFIG["content"])
    keyword = config.get("target_keyword", DEFAULT_CONFIG["target_keyword"])
    competitors = config.get("competitors", DEFAULT_CONFIG["competitors"])
    
    query = f"""
    Analyze this content for SEO optimization:
    
    Target Keyword: {keyword}
    Competitors to Analyze: {competitors}
    
    Content:
    ---
    {content}
    ---
    
    1. Search for top-ranking pages for "{keyword}"
    2. Analyze content structure, keyword usage, and readability
    3. Compare against competitors
    4. Provide prioritized improvement recommendations
    """
    
    print(f"\nTarget Keyword: {keyword}")
    print(f"Content Length: {len(content.split())} words")
    print("-" * 40)
    print("Analyzing content and researching competitors...")
    
    response = agent.run(query)
    
    # Handle structured output
    result = response.content
    if isinstance(result, SEOAnalysis):
        print(f"\n{'='*50}")
        print(f"SEO SCORE: {result.overall_score}/100")
        print(f"{'='*50}")
        
        # Keyword Analysis
        ka = result.keyword_analysis
        print(f"\n📊 Keyword Analysis: {ka.primary_keyword}")
        print(f"  Current Density: {ka.current_density}%")
        print(f"  Recommended: {ka.recommended_density}")
        print(f"  LSI Keywords: {', '.join(ka.lsi_keywords[:5])}")
        if ka.missing_variations:
            print(f"  Missing Variations: {', '.join(ka.missing_variations[:3])}")
        
        # Content Metrics
        cm = result.content_metrics
        print(f"\n📝 Content Metrics:")
        print(f"  Word Count: {cm.word_count}")
        print(f"  Readability: {cm.readability_score}")
        print(f"  Heading Structure: {cm.heading_structure}")
        print(f"  Suggested Links: {cm.internal_links_suggestion} internal, {cm.external_links_suggestion} external")
        
        # Competitor Insights
        print(f"\n🔍 Competitor Insights:")
        for ci in result.competitor_insights[:3]:
            print(f"\n  {ci.source}")
            print(f"    Strengths: {', '.join(ci.strengths[:2])}")
            if ci.content_gaps:
                print(f"    Gaps to Fill: {', '.join(ci.content_gaps[:2])}")
        
        # Title Suggestions
        print(f"\n📌 Title Suggestions:")
        for title in result.title_suggestions[:3]:
            print(f"  • {title}")
        
        print(f"\n📄 Meta Description:")
        print(f"  {result.meta_description}")
        
        # Priority Improvements
        print(f"\n🎯 Priority Improvements:")
        for i, imp in enumerate(result.priority_improvements[:5], 1):
            print(f"  {i}. {imp}")
        
        # Quick Wins
        print(f"\n⚡ Quick Wins:")
        for win in result.quick_wins[:3]:
            print(f"  • {win}")
    else:
        print("\n[Raw Response - structured parsing unavailable]")
        print(result if isinstance(result, str) else str(result))


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="SEO Content Optimizer - Analyze and improve content for search"
    )
    
    parser.add_argument(
        "--content", "-c",
        type=str,
        default=DEFAULT_CONFIG["content"],
        help="Content to analyze (or path to file)"
    )
    parser.add_argument(
        "--keyword", "-k",
        type=str,
        default=DEFAULT_CONFIG["target_keyword"],
        help=f"Target keyword (default: {DEFAULT_CONFIG['target_keyword']})"
    )
    parser.add_argument(
        "--competitors", "-n",
        type=int,
        default=DEFAULT_CONFIG["competitors"],
        help=f"Number of competitors to analyze (default: {DEFAULT_CONFIG['competitors']})"
    )
    
    args = parser.parse_args()
    
    config = {
        "content": args.content,
        "target_keyword": args.keyword,
        "competitors": args.competitors,
    }
    
    agent = get_agent(config=config)
    run_demo(agent, config)


if __name__ == "__main__":
    main()
