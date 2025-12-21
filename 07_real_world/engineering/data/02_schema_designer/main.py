"""
Example #082: Schema Designer
Category: engineering/data
DESCRIPTION: Designs optimal database schemas from requirements - tables, relationships, indexes
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"domain": "e-commerce"}

class Column(BaseModel):
    name: str = Field(description="Column name")
    data_type: str = Field(description="SQL data type")
    nullable: bool = Field(description="Allow nulls")
    constraints: list[str] = Field(description="PK, FK, UNIQUE, CHECK, etc.")

class Table(BaseModel):
    name: str = Field(description="Table name")
    columns: list[Column] = Field(description="Table columns")
    indexes: list[str] = Field(description="Recommended indexes")

class SchemaDesign(BaseModel):
    domain: str = Field(description="Business domain")
    tables: list[Table] = Field(description="Designed tables")
    relationships: list[str] = Field(description="FK relationships")
    normalization_form: str = Field(description="3NF, BCNF, etc.")
    rationale: str = Field(description="Design decisions explained")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Schema Designer",
        instructions=[
            "Design normalized database schemas from business requirements",
            "Apply proper normalization (aim for 3NF minimum)",
            "Define appropriate data types, constraints, and indexes",
            "Consider query patterns for index design",
            "Document relationships and design rationale"
        ],
        output_schema=SchemaDesign, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Schema Designer - Demo\n" + "=" * 60)
    query = f"""Design a database schema for: {config['domain']}

Requirements:
- Track customers with profiles and addresses
- Products with categories and inventory
- Orders with line items and payments
- Support multiple addresses per customer
- Track order history and status changes"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, SchemaDesign):
        print(f"\nDomain: {result.domain}")
        print(f"Normalization: {result.normalization_form}")
        print(f"\nTables ({len(result.tables)}):")
        for table in result.tables:
            print(f"  {table.name}: {len(table.columns)} columns, {len(table.indexes)} indexes")
        print(f"\nRelationships: {len(result.relationships)}")
        print(f"\nRationale: {result.rationale[:200]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", "-d", default=DEFAULT_CONFIG["domain"])
    args = parser.parse_args()
    run_demo(get_agent(), {"domain": args.domain})

if __name__ == "__main__": main()
