"""
Example #190: Weekly Reviewer Agent
Category: personal/productivity
DESCRIPTION: Conducts weekly reviews analyzing accomplishments, lessons, and planning ahead
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"review_style": "comprehensive"}

class WeeklyReview(BaseModel):
    accomplishments: list[str] = Field(description="What was achieved this week")
    incomplete_items: list[str] = Field(description="What didn't get done")
    lessons_learned: list[str] = Field(description="Key insights from the week")
    energy_patterns: str = Field(description="When you were most/least productive")
    next_week_priorities: list[str] = Field(description="Top priorities for next week")
    carry_forward: list[str] = Field(description="Items to reschedule")
    celebration: str = Field(description="Something to celebrate")
    one_improvement: str = Field(description="One thing to do differently")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Weekly Reviewer",
        instructions=[
            f"You conduct {cfg['review_style']} weekly reviews.",
            "Help reflect on accomplishments without judgment.",
            "Identify patterns in productivity and energy.",
            "Extract actionable lessons from the week.",
            "Set up next week for success.",
        ],
        output_schema=WeeklyReview,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Weekly Reviewer - Demo")
    print("=" * 60)
    query = """Review my week:
    Done:
    - Shipped new feature to production
    - Had productive 1:1s with team
    - Exercised 3 times (goal was 4)
    - Finished online course module
    
    Didn't finish:
    - Documentation updates
    - Expense reports
    
    Notes: Tuesday was super productive, Thursday was a struggle.
    Had unexpected meetings on Wednesday."""
    response = agent.run(query)
    result = response.content
    if isinstance(result, WeeklyReview):
        print(f"\n🏆 Accomplishments:")
        for a in result.accomplishments:
            print(f"  ✓ {a}")
        print(f"\n📚 Lessons Learned:")
        for l in result.lessons_learned:
            print(f"  • {l}")
        print(f"\n📅 Next Week Priorities:")
        for p in result.next_week_priorities:
            print(f"  → {p}")
        print(f"\n🎉 Celebrate: {result.celebration}")
        print(f"💡 Improve: {result.one_improvement}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-style", "-r", default=DEFAULT_CONFIG["review_style"])
    args = parser.parse_args()
    run_demo(get_agent(config={"review_style": args.review_style}), {"review_style": args.review_style})

if __name__ == "__main__": main()
