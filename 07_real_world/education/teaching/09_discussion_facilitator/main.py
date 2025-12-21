"""
Example #119: Discussion Facilitator
Category: education/teaching
DESCRIPTION: Facilitates classroom discussions with prompts and responses
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"topic": "ethics_of_ai", "discussion_type": "socratic"}

class DiscussionPrompt(BaseModel):
    prompt: str = Field(description="Discussion prompt")
    type: str = Field(description="opening, probing, clarifying, extending")
    follow_ups: list[str] = Field(description="Potential follow-up questions")

class DiscussionPlan(BaseModel):
    topic: str = Field(description="Discussion topic")
    learning_goals: list[str] = Field(description="Discussion goals")
    opening_prompt: DiscussionPrompt = Field(description="Opening question")
    key_prompts: list[DiscussionPrompt] = Field(description="Key discussion prompts")
    anticipated_responses: list[str] = Field(description="Likely student responses")
    facilitation_tips: list[str] = Field(description="Tips for facilitator")
    summary_questions: list[str] = Field(description="Closing/summary questions")
    assessment_notes: str = Field(description="How to assess participation")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Discussion Facilitator",
        instructions=[
            "Design thought-provoking discussion questions",
            "Create prompts that encourage multiple perspectives",
            "Anticipate student responses and prepare follow-ups",
            "Include questions at various cognitive levels",
            "Plan for inclusive participation"
        ],
        output_schema=DiscussionPlan, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Discussion Facilitator - Demo\n" + "=" * 60)
    query = f"""Plan a discussion:
Topic: {config['topic']}
Type: {config['discussion_type']}
Class: 11th grade ethics
Duration: 30 minutes
Context: Students have read about AI bias in hiring algorithms"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, DiscussionPlan):
        print(f"\nTopic: {result.topic}")
        print(f"\nLearning Goals:")
        for g in result.learning_goals:
            print(f"  • {g}")
        print(f"\nOpening Prompt:\n  \"{result.opening_prompt.prompt}\"")
        print(f"\nKey Prompts ({len(result.key_prompts)}):")
        for p in result.key_prompts[:2]:
            print(f"  [{p.type}] {p.prompt}")
        print(f"\nFacilitation Tips:")
        for t in result.facilitation_tips[:2]:
            print(f"  💡 {t}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", "-t", default=DEFAULT_CONFIG["topic"])
    parser.add_argument("--discussion-type", "-d", default=DEFAULT_CONFIG["discussion_type"])
    args = parser.parse_args()
    run_demo(get_agent(), {"topic": args.topic, "discussion_type": args.discussion_type})

if __name__ == "__main__": main()
