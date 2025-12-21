"""
Example #065: Test Generator
Category: engineering/code

DESCRIPTION:
Generates unit tests for code with edge cases and mocking.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
def calculate_discount(price, quantity, customer_type):
    if price <= 0 or quantity <= 0:
        raise ValueError("Price and quantity must be positive")
    
    base_discount = 0
    if quantity >= 100:
        base_discount = 0.15
    elif quantity >= 50:
        base_discount = 0.10
    elif quantity >= 10:
        base_discount = 0.05
    
    type_discount = {"premium": 0.10, "gold": 0.05, "regular": 0}.get(customer_type, 0)
    
    total_discount = min(base_discount + type_discount, 0.25)
    return price * quantity * (1 - total_discount)
''',
    "framework": "pytest",
}

class TestCase(BaseModel):
    name: str = Field(description="Test function name")
    description: str = Field(description="What it tests")
    input_values: str = Field(description="Test inputs")
    expected: str = Field(description="Expected result")
    test_code: str = Field(description="Test code")

class TestSuite(BaseModel):
    setup_code: str = Field(description="Fixtures and setup")
    test_cases: list[TestCase] = Field(description="Test cases")
    edge_cases: list[TestCase] = Field(description="Edge case tests")
    full_test_file: str = Field(description="Complete test file")
    coverage_notes: str = Field(description="Coverage considerations")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Test Generator",
        instructions=[
            f"You are a QA engineer writing {cfg['framework']} tests.",
            "Generate comprehensive tests including happy path, edge cases,",
            "error conditions, and boundary values.",
            "Use parametrized tests where appropriate.",
        ],
        output_schema=TestSuite,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Test Generator - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Generate tests for:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, TestSuite):
        print(f"\n✅ Test Cases: {len(result.test_cases)}")
        for t in result.test_cases[:3]:
            print(f"  • {t.name}: {t.description}")
        print(f"\n⚠️ Edge Cases: {len(result.edge_cases)}")
        for e in result.edge_cases[:3]:
            print(f"  • {e.name}: {e.description}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Test Generator")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
