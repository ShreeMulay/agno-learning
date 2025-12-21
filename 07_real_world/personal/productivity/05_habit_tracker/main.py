"""
Example #185: Habit Tracker Agent
Category: personal/productivity
DESCRIPTION: Tracks habits, analyzes streaks, and provides motivation for behavior change
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"focus_area": "health"}

class HabitStatus(BaseModel):
    habit: str = Field(description="Habit name")
    current_streak: int = Field(description="Current streak in days")
    best_streak: int = Field(description="Best streak achieved")
    completion_rate: str = Field(description="Weekly completion percentage")
    trend: str = Field(description="improving, stable, declining")

class HabitAnalysis(BaseModel):
    habits: list[HabitStatus] = Field(description="Status of tracked habits")
    wins: list[str] = Field(description="Recent achievements to celebrate")
    challenges: list[str] = Field(description="Habits needing attention")
    suggestions: list[str] = Field(description="Tips to improve consistency")
    motivation: str = Field(description="Encouraging message")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Habit Tracker",
        instructions=[
            f"You track and coach habits focused on {cfg['focus_area']}.",
            "Celebrate wins and streaks to reinforce positive behavior.",
            "Identify patterns in habit completion or failure.",
            "Suggest habit stacking and cue-based strategies.",
            "Provide encouraging, non-judgmental feedback.",
        ],
        output_schema=HabitAnalysis,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Habit Tracker - Demo")
    print("=" * 60)
    query = """Analyze my habit tracking this week:
    - Morning exercise: Mon ✓, Tue ✓, Wed ✗, Thu ✓, Fri ✓
    - Meditation: Mon ✓, Tue ✓, Wed ✓, Thu ✓, Fri ✓
    - Reading 30 min: Mon ✗, Tue ✓, Wed ✗, Thu ✗, Fri ✓
    - No phone before bed: Mon ✓, Tue ✗, Wed ✗, Thu ✓, Fri ✓
    Previous week exercise streak was 7 days before this week."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, HabitAnalysis):
        print(f"\n🏆 Wins:")
        for w in result.wins:
            print(f"  • {w}")
        print(f"\n⚠️ Needs Attention:")
        for c in result.challenges:
            print(f"  • {c}")
        print(f"\n💪 {result.motivation}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--focus-area", "-f", default=DEFAULT_CONFIG["focus_area"])
    args = parser.parse_args()
    run_demo(get_agent(config={"focus_area": args.focus_area}), {"focus_area": args.focus_area})

if __name__ == "__main__": main()
