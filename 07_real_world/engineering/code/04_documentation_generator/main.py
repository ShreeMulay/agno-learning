"""
Example #064: Documentation Generator
Category: engineering/code

DESCRIPTION:
Generates comprehensive documentation from code including docstrings, README, and API docs.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "code": '''
class UserService:
    def __init__(self, db_connection, cache_client=None):
        self.db = db_connection
        self.cache = cache_client
    
    def get_user(self, user_id, include_profile=False):
        if self.cache:
            cached = self.cache.get(f"user:{user_id}")
            if cached:
                return cached
        user = self.db.query("SELECT * FROM users WHERE id = ?", user_id)
        if include_profile:
            user['profile'] = self.db.query("SELECT * FROM profiles WHERE user_id = ?", user_id)
        if self.cache:
            self.cache.set(f"user:{user_id}", user, ttl=300)
        return user
    
    def create_user(self, email, name, role='user'):
        user_id = self.db.insert("users", {"email": email, "name": name, "role": role})
        return {"id": user_id, "email": email, "name": name, "role": role}
''',
}

class FunctionDoc(BaseModel):
    name: str = Field(description="Function name")
    docstring: str = Field(description="Generated docstring")
    params: list[str] = Field(description="Parameter descriptions")
    returns: str = Field(description="Return value description")
    example: str = Field(description="Usage example")

class Documentation(BaseModel):
    module_description: str = Field(description="Module overview")
    class_docs: list[str] = Field(description="Class documentation")
    function_docs: list[FunctionDoc] = Field(description="Function docs")
    readme_section: str = Field(description="README content")
    api_reference: str = Field(description="API reference markdown")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="Documentation Generator",
        instructions=[
            "You are a technical writer generating documentation from code.",
            "Create clear, comprehensive docs following best practices.",
            "Include docstrings, parameter descriptions, examples, and type hints.",
        ],
        output_schema=Documentation,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  Documentation Generator - Demo")
    print("=" * 60)
    code = config.get("code", DEFAULT_CONFIG["code"])
    response = agent.run(f"Generate docs for:\n```\n{code}\n```")
    result = response.content
    if isinstance(result, Documentation):
        print(f"\n📖 {result.module_description}")
        print(f"\n📋 Functions:")
        for f in result.function_docs:
            print(f"\n  {f.name}")
            print(f"  {f.docstring[:100]}...")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="Documentation Generator")
    parser.add_argument("--code", "-c", type=str, default=DEFAULT_CONFIG["code"])
    args = parser.parse_args()
    agent = get_agent(config={"code": args.code})
    run_demo(agent, {"code": args.code})

if __name__ == "__main__":
    main()
