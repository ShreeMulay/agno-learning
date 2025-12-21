"""
Example #088: Data Lineage Tracker
Category: engineering/data
DESCRIPTION: Tracks data lineage - sources, transformations, dependencies across pipelines
"""
import argparse
from typing import Optional
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from pydantic import BaseModel, Field

DEFAULT_CONFIG = {"target_table": "fact_orders"}

class DataNode(BaseModel):
    name: str = Field(description="Table/view/file name")
    node_type: str = Field(description="source, transform, target")
    system: str = Field(description="Database/system name")

class Transformation(BaseModel):
    source: str = Field(description="Source node")
    target: str = Field(description="Target node")
    operation: str = Field(description="join, filter, aggregate, etc.")
    logic: str = Field(description="Transformation description")

class LineageGraph(BaseModel):
    target_asset: str = Field(description="Target being traced")
    nodes: list[DataNode] = Field(description="All nodes in lineage")
    transformations: list[Transformation] = Field(description="Transformation steps")
    source_systems: list[str] = Field(description="Origin systems")
    impact_analysis: str = Field(description="What depends on this asset")
    freshness: str = Field(description="Data freshness/latency")

def default_model(): return OpenRouter(id="anthropic/claude-sonnet-4")

def get_agent(model=None, config: Optional[dict] = None) -> Agent:
    return Agent(model=model or default_model(), name="Data Lineage Tracker",
        instructions=[
            "Map complete data lineage from source to target",
            "Identify all transformations and their logic",
            "Document upstream sources and downstream dependencies",
            "Analyze impact of changes on dependent assets",
            "Track data freshness and latency"
        ],
        output_schema=LineageGraph, use_json_mode=True, markdown=True)

def run_demo(agent: Agent, config: dict):
    print("\n" + "=" * 60 + "\n  Data Lineage Tracker - Demo\n" + "=" * 60)
    query = f"""Trace lineage for: {config['target_table']}

Known pipeline:
1. Raw orders from Postgres (orders table)
2. Customer data from Salesforce API
3. Product catalog from MongoDB
4. Staging tables in Snowflake
5. dbt models transform and join
6. Final fact_orders in analytics schema

Dependencies:
- dashboard_sales uses fact_orders
- report_daily_revenue uses fact_orders
- ml_churn_model reads fact_orders"""
    response = agent.run(query)
    result = response.content
    if isinstance(result, LineageGraph):
        print(f"\nTarget: {result.target_asset}")
        print(f"Freshness: {result.freshness}")
        print(f"\nSource Systems: {', '.join(result.source_systems)}")
        print(f"\nLineage Nodes ({len(result.nodes)}):")
        for node in result.nodes:
            print(f"  [{node.node_type}] {node.name} ({node.system})")
        print(f"\nTransformations ({len(result.transformations)}):")
        for t in result.transformations:
            print(f"  {t.source} -> {t.target}: {t.operation}")
        print(f"\nImpact Analysis: {result.impact_analysis[:200]}...")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-table", "-t", default=DEFAULT_CONFIG["target_table"])
    args = parser.parse_args()
    run_demo(get_agent(), {"target_table": args.target_table})

if __name__ == "__main__": main()
