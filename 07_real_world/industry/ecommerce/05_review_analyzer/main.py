"""
Example #145: Review Analyzer Agent
Category: industry/ecommerce
DESCRIPTION: Analyzes customer reviews for insights and sentiment
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"product": "Wireless Earbuds", "review_count": 150}

class ReviewTheme(BaseModel):
    theme: str = Field(description="Review theme or topic")
    sentiment: str = Field(description="positive/negative/neutral")
    frequency: int = Field(description="How often mentioned")
    sample_quotes: list[str] = Field(description="Example quotes")

class ReviewAnalysis(BaseModel):
    overall_sentiment: str = Field(description="Overall sentiment")
    average_rating: float = Field(description="Average star rating")
    total_reviews: int = Field(description="Total reviews analyzed")
    themes: list[ReviewTheme] = Field(description="Key themes identified")
    top_praise_points: list[str] = Field(description="Most praised aspects")
    top_complaints: list[str] = Field(description="Most common complaints")
    fake_review_risk: str = Field(description="Risk of fake reviews")
    competitive_insights: str = Field(description="Competitive positioning insights")
    improvement_suggestions: list[str] = Field(description="Product improvement ideas")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Review Analyzer",
        instructions=[
            "You are an expert e-commerce review analyst.",
            f"Analyze reviews for products like {cfg['product']}",
            "Identify themes, sentiment patterns, and actionable insights",
            "Detect potential fake or incentivized reviews",
            "Provide competitive and improvement recommendations",
            "Use NLP-style analysis for comprehensive insights",
        ],
        output_schema=ReviewAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Review Analyzer Agent - Demo")
    print("=" * 60)
    sample_reviews = """Sample reviews:
- "Great sound quality! Battery lasts forever." (5 stars)
- "Comfortable but connection drops sometimes." (3 stars)
- "Best purchase ever, using daily for workouts." (5 stars)
- "Took a while to arrive but worth the wait." (4 stars)
- "Cheap feeling case, but earbuds are solid." (4 stars)"""
    query = f"""Analyze customer reviews for: {config['product']}
Reviews analyzed: {config['review_count']}

{sample_reviews}

Provide sentiment analysis and actionable insights."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ReviewAnalysis):
        print(f"\n📊 Overall: {result.overall_sentiment}")
        print(f"⭐ Average Rating: {result.average_rating}/5 ({result.total_reviews} reviews)")
        print(f"\n👍 Top Praise:")
        for p in result.top_praise_points[:3]:
            print(f"  • {p}")
        print(f"\n👎 Top Complaints:")
        for c in result.top_complaints[:3]:
            print(f"  • {c}")
        print(f"\n🔍 Fake Review Risk: {result.fake_review_risk}")
        print(f"\n💡 Improvements:")
        for i in result.improvement_suggestions[:3]:
            print(f"  • {i}")

def main():
    parser = argparse.ArgumentParser(description="Review Analyzer Agent")
    parser.add_argument("--product", "-p", default=DEFAULT_CONFIG["product"])
    parser.add_argument("--count", "-c", type=int, default=DEFAULT_CONFIG["review_count"])
    args = parser.parse_args()
    config = {"product": args.product, "review_count": args.count}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
