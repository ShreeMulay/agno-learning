"""
Example #209: Dialogue Writer Agent
Category: personal/creative
DESCRIPTION: Creates natural, character-driven dialogue for fiction and scripts
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"style": "realistic"}

class DialogueExchange(BaseModel):
    speaker: str = Field(description="Who is speaking")
    line: str = Field(description="What they say")
    action: str = Field(description="Action/body language beat")
    subtext: str = Field(description="What they really mean")

class DialogueScene(BaseModel):
    scene_context: str = Field(description="Setup for the dialogue")
    exchanges: list[DialogueExchange] = Field(description="The dialogue lines")
    emotional_arc: str = Field(description="How emotions shift through scene")
    tension_level: str = Field(description="Conflict level: low, medium, high")
    purpose: str = Field(description="What this scene accomplishes")
    revision_notes: list[str] = Field(description="Tips to enhance the dialogue")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Dialogue Writer",
        instructions=[
            f"You write {cfg['style']} dialogue for fiction.",
            "Give each character a distinct voice.",
            "Include subtext - what's unsaid matters.",
            "Use action beats to break up dialogue.",
            "Make every line do double duty: reveal and advance.",
        ],
        output_schema=DialogueScene,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Dialogue Writer - Demo")
    print("=" * 60)
    query = """Write a dialogue scene:
    Characters: 
    - Alex (confident, hiding insecurity)
    - Jordan (suspicious, protective of a secret)
    Situation: Alex confronts Jordan about mysterious behavior
    Tension: Should build throughout
    Length: 6-8 exchanges"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DialogueScene):
        print(f"\n📍 {result.scene_context}")
        print(f"⚡ Tension: {result.tension_level}")
        print(f"\n🎭 Dialogue:")
        for ex in result.exchanges:
            print(f"\n  {ex.speaker}: \"{ex.line}\"")
            if ex.action:
                print(f"  ({ex.action})")
        print(f"\n📈 Emotional Arc: {result.emotional_arc}")
        print(f"🎯 Purpose: {result.purpose}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--style", "-s", default=DEFAULT_CONFIG["style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"style": args.style}), {"style": args.style})

if __name__ == "__main__": main()
