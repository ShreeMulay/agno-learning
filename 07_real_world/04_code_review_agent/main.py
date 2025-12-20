#!/usr/bin/env python3
"""Example 04: Code Review Agent - Automated code review.

An agent that reviews code and provides actionable feedback.

Run with:
    python main.py --file path/to/code.py
    python main.py "def add(a, b): return a + b"
"""

import argparse
import sys
from pathlib import Path
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agno.agent import Agent

from shared.model_config import get_model, add_model_args
from shared.utils import print_header, print_section


class CodeIssue(BaseModel):
    """A single code issue."""
    line: int = Field(description="Line number (0 if unknown)")
    severity: str = Field(description="critical, warning, or suggestion")
    category: str = Field(description="bug, style, security, performance")
    message: str = Field(description="Description of the issue")
    suggestion: str = Field(description="How to fix it")


class CodeReview(BaseModel):
    """Complete code review result."""
    summary: str = Field(description="Overall assessment")
    score: int = Field(description="Quality score 1-10")
    issues: list[CodeIssue] = Field(description="List of issues found")
    positives: list[str] = Field(description="Good practices observed")
    refactoring_suggestions: list[str] = Field(description="Optional improvements")


def create_code_review_agent(model):
    """Create a code review agent."""
    
    return Agent(
        name="CodeReviewer",
        model=model,
        instructions=[
            "You are an expert code reviewer.",
            "Analyze code for:",
            "- Bugs and logic errors",
            "- Security vulnerabilities",
            "- Performance issues",
            "- Style and readability",
            "- Best practices",
            "",
            "Be constructive and specific.",
            "Provide actionable suggestions.",
            "Acknowledge good practices too.",
        ],
        markdown=True,
    )



def get_agent(model=None):
    if model is None:
        from shared.model_config import get_model
        model = get_model()
    return create_code_review_agent(model)


def main():
    parser = argparse.ArgumentParser(description="Code Review Agent")
    add_model_args(parser)
    parser.add_argument(
        "--file", "-f", type=str, default=None,
        help="Path to code file to review"
    )
    parser.add_argument(
        "code", type=str, nargs="?", default=None,
        help="Inline code to review"
    )
    parser.add_argument(
        "--structured", action="store_true",
        help="Use structured output"
    )
    args = parser.parse_args()

    print_header("Code Review Agent")
    
    # Get code to review
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            return
        code = file_path.read_text()
        source = args.file
    elif args.code:
        code = args.code
        source = "inline"
    else:
        # Demo code
        code = '''
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    average = total / len(numbers)
    return average

def process_user_input(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

password = "admin123"
'''
        source = "demo"
    
    print_section("Reviewing")
    print(f"  Source: {source}")
    print(f"  Lines: {len(code.splitlines())}")
    print()
    
    model = get_model(args.provider, args.model, temperature=args.temperature)
    agent = create_code_review_agent(model)
    
    prompt = f"Review this code:\n\n```\n{code}\n```"
    
    if args.structured:
        response = agent.run(prompt, output_schema=CodeReview)
        review = response.content
        
        print_section(f"Review Score: {review.score}/10")
        print(f"  {review.summary}")
        
        if review.issues:
            print_section("Issues Found")
            for issue in review.issues:
                icon = "🔴" if issue.severity == "critical" else "🟡" if issue.severity == "warning" else "💡"
                print(f"\n  {icon} [{issue.category.upper()}] Line {issue.line}")
                print(f"     {issue.message}")
                print(f"     Fix: {issue.suggestion}")
        
        if review.positives:
            print_section("Positives")
            for positive in review.positives:
                print(f"  ✅ {positive}")
        
        if review.refactoring_suggestions:
            print_section("Suggestions")
            for suggestion in review.refactoring_suggestions:
                print(f"  → {suggestion}")
    else:
        response = agent.run(prompt)
        print_section("Review")
        print(response.content)


if __name__ == "__main__":
    main()
