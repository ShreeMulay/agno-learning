"""
Example #067: API Designer
Category: engineering/code

DESCRIPTION:
Designs RESTful APIs with endpoints, schemas, and best practices.
"""

import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {
    "requirements": """
    Build an API for a task management system with:
    - Users can create, read, update, delete tasks
    - Tasks have title, description, status, due date, priority
    - Tasks can be assigned to users
    - Users can filter tasks by status and priority
    - Support pagination for task lists
    """,
}

class Endpoint(BaseModel):
    method: str = Field(description="HTTP method")
    path: str = Field(description="URL path")
    description: str = Field(description="What it does")
    request_body: Optional[str] = Field(default=None, description="Request schema")
    response: str = Field(description="Response schema")
    status_codes: list[str] = Field(description="Possible status codes")

class APIDesign(BaseModel):
    base_url: str = Field(description="API base URL")
    version: str = Field(description="API version")
    endpoints: list[Endpoint] = Field(description="API endpoints")
    schemas: list[str] = Field(description="Data schemas")
    auth_method: str = Field(description="Authentication approach")
    rate_limiting: str = Field(description="Rate limiting strategy")
    openapi_snippet: str = Field(description="OpenAPI spec excerpt")

def default_model():
    return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(
        model=model or default_model(),
        name="API Designer",
        instructions=[
            "You are a senior API architect designing RESTful APIs.",
            "Follow REST best practices: proper HTTP methods, status codes,",
            "resource naming, versioning, pagination, error handling.",
        ],
        output_schema=APIDesign,
        use_json_mode=True,
        markdown=True,
    )

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60)
    print("  API Designer - Demo")
    print("=" * 60)
    reqs = config.get("requirements", DEFAULT_CONFIG["requirements"])
    response = agent.run(f"Design API for:\n{reqs}")
    result = response.content
    if isinstance(result, APIDesign):
        print(f"\n🌐 {result.base_url}/{result.version}")
        print(f"🔐 Auth: {result.auth_method}")
        print(f"\n📋 Endpoints:")
        for e in result.endpoints[:5]:
            print(f"  {e.method:6} {e.path}")
            print(f"         {e.description}")
    else:
        print(result)

def main():
    parser = argparse.ArgumentParser(description="API Designer")
    parser.add_argument("--requirements", "-r", type=str, default=DEFAULT_CONFIG["requirements"])
    args = parser.parse_args()
    agent = get_agent(config={"requirements": args.requirements})
    run_demo(agent, {"requirements": args.requirements})

if __name__ == "__main__":
    main()
