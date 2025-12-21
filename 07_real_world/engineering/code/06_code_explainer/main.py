"""
Example #066: Code Explainer
Category: engineering/code

DESCRIPTION:
Explains code in plain language for learning and onboarding.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
async def rate_limited_fetch(urls, max_concurrent=5, delay=0.1):
    semaphore = asyncio.Semaphore(max_concurrent)
    async def fetch_one(url):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    await asyncio.sleep(delay)
                    return await response.json()
    return await asyncio.gather(*[fetch_one(url) for url in urls])
''',
    "audience": "junior developer",
}

class CodeExplanation(BaseModel):
    summary: str = Field(description="One-sentence summary")
    purpose: str = Field(description="What problem it solves")
    step_by_step: list[str] = Field(description="Line-by-line explanation")
    concepts: list[str] = Field(description="Key concepts used")
    analogies: list[str] = Field(description="Real-world analogies")
    common_questions: list[str] = Field(description="FAQs about this code")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    cfg = {**DEFAULT_CONFIG, **(config or {})}
    return Agent(
        model=model or default_model(),
        name="Code Explainer",
        instructions=[
            f"Explain code to a {cfg['audience']}.",
            "Use simple language, analogies, and examples.",
            "Break down complex concepts step by step.",
        ],
        output_schema=CodeExplanation,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Code Explainer - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Explain:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, CodeExplanation):
        print(f"\n📝 {result.summary}")
        print(f"\n🎯 Purpose: {result.purpose}")
        print(f"\n📚 Key Concepts:")
        for c in result.concepts:
            print(f"  • {c}")
        print(f"\n💡 Analogies:")
        for a in result.analogies:
            print(f"  • {a}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Code Explainer")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
