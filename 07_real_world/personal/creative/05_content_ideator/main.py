"""
Example #205: Content Ideator Agent
Category: personal/creative
DESCRIPTION: Generates content ideas and topics based on niche, trends, and audience interests
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"niche": "technology"}

class ContentIdea(BaseModel):
    title: str = Field(description="Content title/headline")
    format: str = Field(description="blog, video, thread, carousel, etc")
    hook: str = Field(description="Attention-grabbing angle")
    target_audience: str = Field(description="Who this is for")
    potential_reach: str = Field(description="Estimated engagement potential")

class IdeationSession(BaseModel):
    theme: str = Field(description="Overarching theme for ideas")
    ideas: list[ContentIdea] = Field(description="Generated content ideas")
    trending_angles: list[str] = Field(description="Current trends to leverage")
    evergreen_topics: list[str] = Field(description="Timeless content opportunities")
    content_calendar: list[str] = Field(description="Suggested posting schedule")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Content Ideator",
        instructions=[
            f"You generate content ideas for the {cfg['niche']} niche.",
            "Mix trending topics with evergreen content.",
            "Consider multiple content formats.",
            "Focus on audience value and engagement.",
            "Suggest unique angles and hooks.",
        ],
        output_schema=IdeationSession,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Content Ideator - Demo")
    print("=" * 60)
    query = """Generate content ideas:
    Niche: Personal productivity and tech
    Platform: LinkedIn and Twitter
    Goal: Build thought leadership
    Audience: Tech professionals and entrepreneurs
    Generate 5 ideas with different formats"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, IdeationSession):
        print(f"\n🎯 Theme: {result.theme}")
        print(f"\n💡 Content Ideas:")
        for idea in result.ideas:
            print(f"\n  📌 {idea.title}")
            print(f"     Format: {idea.format} | Audience: {idea.target_audience}")
            print(f"     Hook: {idea.hook}")
        print(f"\n🔥 Trending Angles: {', '.join(result.trending_angles)}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", "-n", default=DEFAULT_CONFIG["niche"])
    args = parser.parse_args()
    run_demo(get_agent(config={"niche": args.niche}), {"niche": args.niche})

if __name__ == "__main__": main()
