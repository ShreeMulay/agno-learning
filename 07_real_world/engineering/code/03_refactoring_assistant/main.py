"""
Example #063: Refactoring Assistant
Category: engineering/code

DESCRIPTION:
Suggests and applies refactoring patterns to improve code quality.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
def process_order(order):
    if order['type'] == 'standard':
        price = order['quantity'] * order['unit_price']
        if order['quantity'] > 100:
            price = price * 0.9
        tax = price * 0.08
        shipping = 5.99
        total = price + tax + shipping
    elif order['type'] == 'express':
        price = order['quantity'] * order['unit_price']
        if order['quantity'] > 100:
            price = price * 0.85
        tax = price * 0.08
        shipping = 15.99
        total = price + tax + shipping
    elif order['type'] == 'premium':
        price = order['quantity'] * order['unit_price']
        if order['quantity'] > 100:
            price = price * 0.8
        tax = price * 0.08
        shipping = 0
        total = price + tax + shipping
    return total
''',
}

class Refactoring(BaseModel):
    pattern: str = Field(description="Refactoring pattern applied")
    before_lines: str = Field(description="Code before")
    after_lines: str = Field(description="Code after")
    benefit: str = Field(description="Why this improves the code")

class RefactoringPlan(BaseModel):
    code_smells: list[str] = Field(description="Issues identified")
    refactorings: list[Refactoring] = Field(description="Suggested refactorings")
    refactored_code: str = Field(description="Complete refactored code")
    improvement_summary: str = Field(description="Summary of improvements")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Refactoring Assistant",
        instructions=[
            "You are a refactoring expert applying clean code principles.",
            "Identify code smells: duplication, long methods, magic numbers,",
            "complex conditionals, poor naming, tight coupling.",
            "Apply patterns: Extract Method, Strategy, Factory, etc.",
        ],
        output_schema=RefactoringPlan,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Refactoring Assistant - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Refactor:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, RefactoringPlan):
        print(f"\n🔍 Code Smells:")
        for s in result.code_smells:
            print(f"  • {s}")
        print(f"\n🔧 Refactorings:")
        for r in result.refactorings:
            print(f"  • {r.pattern}: {r.benefit}")
        print(f"\n📝 {result.improvement_summary}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Refactoring Assistant")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
