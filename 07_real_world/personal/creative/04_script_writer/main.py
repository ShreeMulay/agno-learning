"""
Example #204: Script Writer Agent
Category: personal/creative
DESCRIPTION: Writes scripts for videos, podcasts, or presentations with proper formatting
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"format": "youtube"}

class ScriptSection(BaseModel):
    section_name: str = Field(description="Section label: intro, main, outro, etc")
    content: str = Field(description="Script content for this section")
    duration_estimate: str = Field(description="Estimated duration")
    visual_notes: str = Field(description="Visual/B-roll suggestions")

class Script(BaseModel):
    title: str = Field(description="Script/video title")
    hook: str = Field(description="Opening hook to grab attention")
    sections: list[ScriptSection] = Field(description="Script sections")
    call_to_action: str = Field(description="CTA for viewers")
    total_duration: str = Field(description="Total estimated runtime")
    talking_points: list[str] = Field(description="Key points to emphasize")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Script Writer",
        instructions=[
            f"You write scripts optimized for {cfg['format']} format.",
            "Open with a strong hook to capture attention.",
            "Structure content for the platform's best practices.",
            "Include visual and timing cues.",
            "Write in natural, speakable language.",
        ],
        output_schema=Script,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Script Writer - Demo")
    print("=" * 60)
    query = """Write a YouTube script about:
    Topic: 5 Python tips for beginners
    Target length: 8-10 minutes
    Style: Educational but casual
    Include timestamps for each tip"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, Script):
        print(f"\n🎬 {result.title}")
        print(f"⏱️ Total Duration: {result.total_duration}")
        print(f"\n🎣 Hook: {result.hook}")
        print(f"\n📋 Sections:")
        for section in result.sections:
            print(f"  [{section.duration_estimate}] {section.section_name}")
        print(f"\n📢 CTA: {result.call_to_action}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", "-f", default=DEFAULT_CONFIG["format"])
    args = parser.parse_args()
    run_demo(get_agent(config={"format": args.format}), {"format": args.format})

if __name__ == "__main__": main()
