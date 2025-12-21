"""
Example #160: Review Aggregator Agent
Category: industry/travel
DESCRIPTION: Aggregates and summarizes travel reviews from multiple sources
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"place_name": "Eiffel Tower", "place_type": "attraction", "city": "Paris"}

class ReviewSummary(BaseModel):
    source: str = Field(description="Review source")
    rating: float = Field(description="Average rating")
    review_count: int = Field(description="Number of reviews")
    sentiment: str = Field(description="Overall sentiment")

class AggregatedReview(BaseModel):
    place_name: str = Field(description="Place name")
    place_type: str = Field(description="Type of place")
    overall_rating: float = Field(description="Aggregated rating")
    total_reviews: int = Field(description="Total reviews analyzed")
    sources: list[ReviewSummary] = Field(description="By source breakdown")
    top_positives: list[str] = Field(description="Most praised aspects")
    top_negatives: list[str] = Field(description="Common complaints")
    best_time_to_visit: str = Field(description="Best time based on reviews")
    tips_from_reviewers: list[str] = Field(description="Tips from visitors")
    verdict: str = Field(description="Overall verdict")
    worth_it: str = Field(description="Is it worth visiting")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Review Aggregator",
        instructions=[
            "You are an expert travel review analyst.",
            f"Aggregate reviews for {cfg['place_name']} in {cfg['city']}",
            "Synthesize reviews from multiple platforms",
            "Identify patterns in positive and negative feedback",
            "Extract practical tips from reviewer experiences",
            "Provide balanced, honest assessment",
        ],
        output_schema=AggregatedReview,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Review Aggregator Agent - Demo")
    print("=" * 60)
    query = f"""Aggregate reviews for:
- Place: {config['place_name']}
- Type: {config['place_type']}
- City: {config['city']}

Synthesize reviews and provide verdict."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, AggregatedReview):
        print(f"\n📍 {result.place_name} ({result.place_type})")
        print(f"⭐ Overall: {result.overall_rating}/5 ({result.total_reviews:,} reviews)")
        print(f"\n📊 By Source:")
        for src in result.sources[:3]:
            print(f"  • {src.source}: {src.rating}/5 ({src.review_count} reviews) - {src.sentiment}")
        print(f"\n👍 Praised: {', '.join(result.top_positives[:3])}")
        print(f"👎 Complaints: {', '.join(result.top_negatives[:3])}")
        print(f"\n⏰ Best Time: {result.best_time_to_visit}")
        print(f"✅ Worth It? {result.worth_it}")
        print(f"\n🎯 Verdict: {result.verdict}")

def main():
    parser = argparse.ArgumentParser(description="Review Aggregator Agent")
    parser.add_argument("--place", "-p", default=DEFAULT_CONFIG["place_name"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["place_type"])
    parser.add_argument("--city", "-c", default=DEFAULT_CONFIG["city"])
    args = parser.parse_args()
    config = {"place_name": args.place, "place_type": args.type, "city": args.city}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
