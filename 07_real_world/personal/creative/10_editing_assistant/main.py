"""
Example #210: Editing Assistant Agent
Category: personal/creative
DESCRIPTION: Provides developmental and line editing suggestions for manuscripts
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"edit_level": "developmental"}

class EditSuggestion(BaseModel):
    location: str = Field(description="Where in the text")
    issue: str = Field(description="What the problem is")
    suggestion: str = Field(description="How to fix it")
    priority: str = Field(description="high, medium, low")

class EditingReport(BaseModel):
    overall_impression: str = Field(description="General assessment")
    structure_notes: str = Field(description="Comments on organization")
    pacing_notes: str = Field(description="Comments on rhythm and flow")
    voice_notes: str = Field(description="Comments on style and voice")
    suggestions: list[EditSuggestion] = Field(description="Specific edit suggestions")
    strengths_to_keep: list[str] = Field(description="What's working well")
    revision_priorities: list[str] = Field(description="What to tackle first")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Editing Assistant",
        instructions=[
            f"You provide {cfg['edit_level']} editing for manuscripts.",
            "Assess structure, pacing, and narrative flow.",
            "Identify both problems and what's working.",
            "Give specific, actionable suggestions.",
            "Prioritize edits by impact.",
        ],
        output_schema=EditingReport,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Editing Assistant - Demo")
    print("=" * 60)
    query = """Edit this passage:

    'The rain fell hard against the window. Sarah looked out. She was 
    thinking about him again. It had been three years since he left. 
    Three long years. She remembered everything. The way he smiled. 
    The way he laughed. The way he made her feel special. Now she 
    felt nothing. Just emptiness. The phone rang. She picked it up. 
    It was him.'
    
    This is from a literary fiction novel. Help me improve it."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, EditingReport):
        print(f"\n📝 Overall: {result.overall_impression}")
        print(f"\n📊 Structure: {result.structure_notes}")
        print(f"⏱️ Pacing: {result.pacing_notes}")
        print(f"\n✏️ Top Suggestions:")
        for sug in [s for s in result.suggestions if s.priority == "high"][:3]:
            print(f"\n  🔹 {sug.issue}")
            print(f"     → {sug.suggestion}")
        print(f"\n✅ Keep These Strengths:")
        for s in result.strengths_to_keep:
            print(f"  • {s}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--edit-level", "-e", default=DEFAULT_CONFIG["edit_level"])
    args = parser.parse_args()
    run_demo(get_agent(config={"edit_level": args.edit_level}), {"edit_level": args.edit_level})

if __name__ == "__main__": main()
