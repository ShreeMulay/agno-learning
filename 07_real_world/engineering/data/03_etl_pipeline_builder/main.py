"""
Example #083: ETL Pipeline Builder
Category: engineering/data
DESCRIPTION: Generates ETL pipeline code and configurations from source to target specs
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"source": "postgres", "target": "snowflake"}

class TransformStep(BaseModel):
    name: str = Field(description="Step name")
    operation: str = Field(description="filter, map, join, aggregate, etc.")
    logic: str = Field(description="Transformation logic")

class ETLPipeline(BaseModel):
    name: str = Field(description="Pipeline name")
    source_system: str = Field(description="Source database/system")
    target_system: str = Field(description="Target database/system")
    extract_query: str = Field(description="SQL or API call for extraction")
    transforms: list[TransformStep] = Field(description="Transformation steps")
    load_strategy: str = Field(description="full, incremental, merge, etc.")
    schedule: str = Field(description="Cron expression or trigger")
    code_snippet: str = Field(description="Sample implementation code")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="ETL Pipeline Builder",
        instructions=[
            "Design ETL pipelines from source to target specifications",
            "Generate extraction queries optimized for the source system",
            "Define clear transformation steps with business logic",
            "Choose appropriate load strategies (full, incremental, CDC)",
            "Provide runnable code snippets (Python/SQL/dbt)"
        ],
        output_schema=ETLPipeline, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  ETL Pipeline Builder - Demo\n" + "=" * 60)
    query = f"""Build an ETL pipeline:
Source: {config['source']} (orders table with customer_id, product_id, amount, order_date)
Target: {config['target']} (fact_orders with denormalized customer and product info)

Requirements:
- Daily incremental loads based on order_date
- Join with customers and products tables
- Calculate running totals per customer
- Handle late-arriving data"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, ETLPipeline):
        print(f"\nPipeline: {result.name}")
        print(f"Source: {result.source_system} -> Target: {result.target_system}")
        print(f"Load Strategy: {result.load_strategy}")
        print(f"Schedule: {result.schedule}")
        print(f"\nTransform Steps ({len(result.transforms)}):")
        for step in result.transforms:
            print(f"  - {step.name}: {step.operation}")
        print(f"\nCode Preview:\n{result.code_snippet[:300]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", default=DEFAULT_CONFIG["source"])
    parser.add_argument("--target", "-t", default=DEFAULT_CONFIG["target"])
    args = parser.parse_args()
    run_demo(get_agent(), {"source": args.source, "target": args.target})

if __name__ == "__main__": main()
