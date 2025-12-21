"""
Example #202: Blog Writer Agent
Category: personal/creative
DESCRIPTION: Creates engaging blog posts with SEO optimization and audience targeting
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"tone": "conversational"}

class BlogPost(BaseModel):
    title: str = Field(description="Catchy blog title")
    meta_description: str = Field(description="SEO meta description")
    introduction: str = Field(description="Engaging opening paragraph")
    sections: list[str] = Field(description="Main content sections")
    conclusion: str = Field(description="Closing with call-to-action")
    keywords: list[str] = Field(description="Target SEO keywords")
    suggested_images: list[str] = Field(description="Image placement suggestions")
    estimated_read_time: str = Field(description="Reading time estimate")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Blog Writer",
        instructions=[
            f"You write blog posts with a {cfg['tone']} tone.",
            "Create attention-grabbing headlines.",
            "Structure content for easy scanning.",
            "Include relevant SEO keywords naturally.",
            "End with clear calls-to-action.",
        ],
        output_schema=BlogPost,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Blog Writer - Demo")
    print("=" * 60)
    query = """Write a blog post about:
    Topic: The benefits of morning routines
    Audience: Busy professionals
    Length: ~800 words
    Include: Practical tips, personal productivity angle"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, BlogPost):
        print(f"\n📝 {result.title}")
        print(f"⏱️ {result.estimated_read_time}")
        print(f"\n📋 Meta: {result.meta_description}")
        print(f"\n🎯 Keywords: {', '.join(result.keywords)}")
        print(f"\n📖 Introduction:\n{result.introduction}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tone", "-t", default=DEFAULT_CONFIG["tone"])
    args = parser.parse_args()
    run_demo(get_agent(config={"tone": args.tone}), {"tone": args.tone})

if __name__ == "__main__": main()
