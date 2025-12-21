"""
Example #214: Content Pipeline Multi-Agent
Category: advanced/multi_agent
DESCRIPTION: Content creation pipeline with writer, editor, and SEO specialist agents
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"content_type": "blog"}

class ContentPiece(BaseModel):
    title: str = Field(description="Final title")
    meta_description: str = Field(description="SEO meta description")
    content: str = Field(description="Final content")
    keywords: list[str] = Field(description="Target keywords")
    readability_score: str = Field(description="Readability assessment")
    seo_score: int = Field(description="SEO optimization score 1-100")
    word_count: int = Field(description="Total word count")
    revision_notes: list[str] = Field(description="Changes made during editing")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_writer_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Content Writer",
        instructions=[
            "You write engaging, informative content.",
            "Focus on clarity and reader value.",
            "Create compelling narratives.",
        ],
        markdown=True,
    )

def get_editor_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Content Editor",
        instructions=[
            "You edit content for clarity, flow, and engagement.",
            "Fix grammar, improve sentence structure.",
            "Ensure consistent voice and tone.",
        ],
        markdown=True,
    )

def get_seo_agent(model=None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="SEO Specialist",
        instructions=[
            "You optimize content for search engines.",
            "Integrate keywords naturally.",
            "Improve meta descriptions and headings.",
        ],
        output_schema=ContentPiece,
        use_json_mode=True,
        markdown=True,
    )

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return get_seo_agent(model)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Content Pipeline - Demo")
    print("=" * 60)
    
    brief = "Write about the benefits of automated testing in software development"
    
    writer = get_writer_agent()
    editor = get_editor_agent()
    seo = agent
    
    print(f"\n📝 Brief: {brief}")
    print("\n⚙️ Running content pipeline...")
    
    draft = writer.run(f"Write a blog post about: {brief}")
    edited = editor.run(f"Edit and improve this content:\n{draft.content}")
    
    final_prompt = f"""
    Original brief: {brief}
    Edited content: {edited.content}
    
    Optimize for SEO and produce final content piece.
    Target keywords: automated testing, software quality, CI/CD, test automation"""
    
    result = seo.run(final_prompt)
    
    if isinstance(result.content, ContentPiece):
        r = result.content
        print(f"\n📰 Title: {r.title}")
        print(f"📊 SEO Score: {r.seo_score}/100 | Words: {r.word_count}")
        print(f"📋 Meta: {r.meta_description}")
        print(f"🔑 Keywords: {', '.join(r.keywords)}")
        print(f"\n📝 Content Preview:\n{r.content[:300]}...")
        print(f"\n✏️ Revisions Made:")
        for note in r.revision_notes[:3]:
            print(f"  • {note}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-type", "-c", default=DEFAULT_CONFIG["content_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"content_type": args.content_type})

if __name__ == "__main__": main()
