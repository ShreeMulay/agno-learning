"""
Example #112: Quiz Generator
Category: education/teaching
DESCRIPTION: Generates quizzes and tests with varied question types and answer keys
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"topic": "cell biology", "difficulty": "medium"}

class Question(BaseModel):
    number: int = Field(description="Question number")
    type: str = Field(description="multiple_choice, short_answer, essay, matching")
    question: str = Field(description="Question text")
    options: list[str] = Field(description="Options for MC questions")
    answer: str = Field(description="Correct answer")
    points: int = Field(description="Point value")
    explanation: str = Field(description="Answer explanation")

class Quiz(BaseModel):
    title: str = Field(description="Quiz title")
    topic: str = Field(description="Topic covered")
    difficulty: str = Field(description="easy, medium, hard")
    total_points: int = Field(description="Total points")
    time_limit: int = Field(description="Time limit in minutes")
    questions: list[Question] = Field(description="Quiz questions")
    instructions: str = Field(description="Student instructions")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Quiz Generator",
        instructions=[
            "Generate varied question types appropriate to content",
            "Create clear, unambiguous questions",
            "Include plausible distractors for multiple choice",
            "Align questions with learning objectives",
            "Provide detailed answer explanations"
        ],
        output_schema=Quiz, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Quiz Generator - Demo\n" + "=" * 60)
    query = f"""Generate a quiz:
Topic: {config['topic']}
Difficulty: {config['difficulty']}
Questions: 5 (mix of types)
Grade level: High school biology"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, Quiz):
        print(f"\n{result.title}")
        print(f"Topic: {result.topic} | Difficulty: {result.difficulty}")
        print(f"Total: {result.total_points} points | Time: {result.time_limit} min")
        print(f"\nQuestions ({len(result.questions)}):")
        for q in result.questions:
            print(f"  {q.number}. [{q.type}] {q.question[:60]}... ({q.points} pts)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", "-t", default=DEFAULT_CONFIG["topic"])
    parser.add_argument("--difficulty", "-d", default=DEFAULT_CONFIG["difficulty"])
    args = parser.parse_args()
    run_demo(get_agent(), {"topic": args.topic, "difficulty": args.difficulty})

if __name__ == "__main__": main()
