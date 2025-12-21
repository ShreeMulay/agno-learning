"""
Example #226: Self-Improving Agent
Category: advanced/patterns
DESCRIPTION: Agent that learns from feedback to improve future responses
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"learning_mode": "active"}

class Lesson(BaseModel):
    situation: str = Field(description="What happened")
    feedback: str = Field(description="Feedback received")
    learning: str = Field(description="What was learned")
    application: str = Field(description="How to apply in future")

class SelfImprovingResponse(BaseModel):
    response: str = Field(description="Current response")
    lessons_applied: list[str] = Field(description="Past lessons used")
    confidence: str = Field(description="Response confidence")
    areas_for_feedback: list[str] = Field(description="What to get feedback on")
    improvement_plan: str = Field(description="How to keep improving")

# Simulated learning store
class LearningStore:
    def __init__(self):
        self.lessons: list[Lesson] = [
            Lesson(
                situation="Technical explanation was too complex",
                feedback="User asked for simpler terms",
                learning="Match explanation complexity to audience",
                application="Ask about technical background first"
            )
        ]
    
    def get_lessons(self) -> str:
        return "\n".join([f"- {l.learning}: {l.application}" for l in self.lessons])

_store = LearningStore()

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Self-Improving Agent",
        instructions=[
            f"You operate in {cfg['learning_mode']} learning mode.",
            "Apply lessons from past interactions.",
            "Identify areas where you need feedback.",
            "Continuously improve based on learning.",
        ],
        output_schema=SelfImprovingResponse,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Self-Improving Agent - Demo")
    print("=" * 60)
    
    lessons = _store.get_lessons()
    query = "Explain how machine learning works"
    
    print(f"\n📚 Lessons Learned:\n{lessons}")
    print(f"\n❓ Query: {query}")
    
    response = agent.run(f"""
    Past lessons to apply:
    {lessons}
    
    Current query: {query}
    
    Apply your learnings and identify areas for improvement.""")
    
    if isinstance(response.content, SelfImprovingResponse):
        r = response.content
        print(f"\n✅ Response: {r.response[:200]}...")
        print(f"\n📖 Lessons Applied: {', '.join(r.lessons_applied)}")
        print(f"📊 Confidence: {r.confidence}")
        print(f"❓ Feedback Needed On: {', '.join(r.areas_for_feedback)}")
        print(f"📈 Improvement Plan: {r.improvement_plan}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning-mode", "-l", default=DEFAULT_CONFIG["learning_mode"])
    args = parser.parse_args()
    run_demo(get_agent(config={"learning_mode": args.learning_mode}), {"learning_mode": args.learning_mode})

if __name__ == "__main__": main()
