"""
Example #118: Feedback Writer
Category: education/teaching
DESCRIPTION: Writes constructive, personalized feedback on student work
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"feedback_style": "growth_mindset"}

class FeedbackResponse(BaseModel):
    student_name: str = Field(description="Student name")
    assignment: str = Field(description="Assignment name")
    praise: list[str] = Field(description="Specific praise points")
    suggestions: list[str] = Field(description="Improvement suggestions")
    questions: list[str] = Field(description="Questions to prompt reflection")
    next_steps: list[str] = Field(description="Concrete next steps")
    written_feedback: str = Field(description="Full written feedback")
    tone: str = Field(description="Feedback tone used")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Feedback Writer",
        instructions=[
            "Write specific, actionable feedback",
            "Balance praise with constructive suggestions",
            "Use growth mindset language",
            "Reference specific examples from student work",
            "Encourage student reflection and self-assessment"
        ],
        output_schema=FeedbackResponse, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Feedback Writer - Demo\n" + "=" * 60)
    query = f"""Write feedback ({config['feedback_style']} style):
Student: Emma
Assignment: Research paper on renewable energy
Observations:
- Strong thesis statement
- Good use of sources (5 cited)
- Some paragraphs lack topic sentences
- Conclusion restates thesis but doesn't extend thinking
- Minor citation format errors
- Shows genuine interest in topic"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, FeedbackResponse):
        print(f"\nStudent: {result.student_name}")
        print(f"Assignment: {result.assignment}")
        print(f"Tone: {result.tone}")
        print(f"\n✓ Praise:")
        for p in result.praise[:2]:
            print(f"  {p}")
        print(f"\n→ Suggestions:")
        for s in result.suggestions[:2]:
            print(f"  {s}")
        print(f"\nWritten Feedback:\n{result.written_feedback[:300]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feedback-style", "-s", default=DEFAULT_CONFIG["feedback_style"])
    args = parser.parse_args()
    run_demo(get_agent(), {"feedback_style": args.feedback_style})

if __name__ == "__main__": main()
