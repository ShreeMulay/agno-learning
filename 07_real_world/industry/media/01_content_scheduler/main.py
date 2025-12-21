"""
Example #161: Content Scheduler Agent
Category: industry/media
DESCRIPTION: Schedules content across multiple platforms with optimal timing
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"platforms": "twitter, linkedin, instagram", "content_type": "blog promotion", "timezone": "EST"}

class ScheduledPost(BaseModel):
    platform: str = Field(description="Social platform")
    post_time: str = Field(description="Optimal post time")
    content_variant: str = Field(description="Platform-specific content")
    hashtags: list[str] = Field(description="Relevant hashtags")
    engagement_prediction: str = Field(description="Expected engagement level")

class ContentSchedule(BaseModel):
    campaign_name: str = Field(description="Campaign identifier")
    content_type: str = Field(description="Type of content")
    schedule: list[ScheduledPost] = Field(description="Scheduled posts")
    best_days: list[str] = Field(description="Best days to post")
    audience_overlap: str = Field(description="Cross-platform audience notes")
    frequency_recommendation: str = Field(description="Posting frequency advice")
    automation_tips: list[str] = Field(description="Automation suggestions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Content Scheduler",
        instructions=[
            "You are an expert social media content scheduler.",
            f"Schedule content across: {cfg['platforms']}",
            f"Optimize for {cfg['timezone']} timezone audience",
            "Consider platform-specific best practices",
            "Adapt content format for each platform",
            "Maximize engagement through optimal timing",
        ],
        output_schema=ContentSchedule,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Content Scheduler Agent - Demo")
    print("=" * 60)
    query = f"""Create a content schedule:
- Platforms: {config['platforms']}
- Content Type: {config['content_type']}
- Timezone: {config['timezone']}

Optimize posting times for maximum engagement."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ContentSchedule):
        print(f"\n📅 Campaign: {result.campaign_name}")
        print(f"📝 Type: {result.content_type}")
        print(f"\n🗓️ Schedule:")
        for post in result.schedule[:4]:
            print(f"  • {post.platform}: {post.post_time}")
            print(f"    {post.content_variant[:60]}...")
        print(f"\n📊 Best Days: {', '.join(result.best_days)}")
        print(f"🔄 Frequency: {result.frequency_recommendation}")

def main():
    parser = argparse.ArgumentParser(description="Content Scheduler Agent")
    parser.add_argument("--platforms", "-p", default=DEFAULT_CONFIG["platforms"])
    parser.add_argument("--type", "-t", default=DEFAULT_CONFIG["content_type"])
    parser.add_argument("--tz", default=DEFAULT_CONFIG["timezone"])
    args = parser.parse_args()
    config = {"platforms": args.platforms, "content_type": args.type, "timezone": args.tz}
    run_demo(get_agent(config=config), config)

if __name__ == "__main__": main()
