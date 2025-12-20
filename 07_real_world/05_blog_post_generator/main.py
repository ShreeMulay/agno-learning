#!/usr/bin/env python3
"""Example 05: Blog Post Generator - Multi-step content workflow.

A workflow that generates blog posts through research, writing, and editing.

Run with:
    python main.py "The future of renewable energy"
"""

import argparse
import sys
from pathlib import Path
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


class BlogOutline(BaseModel):
    """Blog post outline."""
    title: str = Field(description="Catchy blog title")
    subtitle: str = Field(description="Subtitle or tagline")
    sections: list[str] = Field(description="Main section headings")
    key_points: list[str] = Field(description="Key points to cover")
    target_audience: str = Field(description="Who this post is for")
    seo_keywords: list[str] = Field(description="SEO keywords to target")


class BlogPost(BaseModel):
    """Final blog post."""
    title: str
    subtitle: str
    content: str = Field(description="Full markdown content")
    meta_description: str = Field(description="SEO meta description")
    tags: list[str]


def create_blog_workflow(model):
    """Create agents for the blog generation workflow."""
    
    # Research agent
    researcher = Agent(
        name="Researcher",
        model=model,
        tools=[DuckDuckGoTools()],
        instructions=[
            "Research the given topic thoroughly.",
            "Find current trends, statistics, and examples.",
            "Identify key points and angles.",
        ],
    )
    
    # Outline agent
    outliner = Agent(
        name="Outliner",
        model=model,
        instructions=[
            "Create a detailed blog post outline.",
            "Include catchy title and clear sections.",
            "Identify target audience and SEO keywords.",
        ],
    )
    
    # Writer agent
    writer = Agent(
        name="Writer",
        model=model,
        instructions=[
            "Write engaging, well-structured blog content.",
            "Use the outline as your guide.",
            "Include relevant examples and data.",
            "Write in a conversational but professional tone.",
        ],
    )
    
    # Editor agent
    editor = Agent(
        name="Editor",
        model=model,
        instructions=[
            "Review and polish the blog post.",
            "Improve clarity and flow.",
            "Fix any errors or awkward phrasing.",
            "Ensure SEO best practices.",
        ],
    )
    
    return researcher, outliner, writer, editor


def main():
    parser = argparse.ArgumentParser(description="Blog Post Generator")
    add_model_args(parser)
    parser.add_argument(
        "topic", type=str, nargs="?",
        default="The benefits of mindfulness in daily life",
        help="Blog post topic"
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output file for the blog post"
    )
    args = parser.parse_args()

    print_header("Blog Post Generator")
    print(f"\n  Topic: {args.topic}\n")
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    researcher, outliner, writer, editor = create_blog_workflow(model)
    
    # Step 1: Research
    print_section("Step 1: Research")
    research_result = researcher.run(
        f"Research this topic for a blog post: {args.topic}. "
        "Find current trends, statistics, and interesting angles."
    )
    print(f"  Research complete ({len(research_result.content)} chars)")
    
    # Step 2: Outline
    print_section("Step 2: Outline")
    outline_result = outliner.run(
        f"Create a blog post outline about: {args.topic}\n\n"
        f"Research findings:\n{research_result.content}",
        response_model=BlogOutline
    )
    outline = outline_result.content
    print(f"  Title: {outline.title}")
    print(f"  Sections: {len(outline.sections)}")
    print(f"  Keywords: {', '.join(outline.seo_keywords[:3])}")
    
    # Step 3: Write
    print_section("Step 3: Write")
    write_result = writer.run(
        f"Write a complete blog post based on this outline:\n\n"
        f"Title: {outline.title}\n"
        f"Subtitle: {outline.subtitle}\n"
        f"Sections: {', '.join(outline.sections)}\n"
        f"Key Points: {', '.join(outline.key_points)}\n\n"
        f"Research: {research_result.content}"
    )
    print(f"  Draft complete ({len(write_result.content)} chars)")
    
    # Step 4: Edit
    print_section("Step 4: Edit")
    edit_result = editor.run(
        f"Edit and polish this blog post. "
        f"Ensure it targets these keywords: {', '.join(outline.seo_keywords)}\n\n"
        f"{write_result.content}"
    )
    print("  Editing complete")
    
    # Output
    print_section("Final Blog Post")
    print(f"\n# {outline.title}\n")
    print(f"*{outline.subtitle}*\n")
    print(edit_result.content[:500] + "...\n")
    
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(f"# {outline.title}\n\n{edit_result.content}")
        print(f"\n  Saved to: {args.output}")


if __name__ == "__main__":
    main()
